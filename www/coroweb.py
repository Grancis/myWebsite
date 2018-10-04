#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

__author__='refer to Michael Liao'
#啊啊啊 看不懂啊
#RequestHandler的部分很难懂 web的请求掌握得不好

import aiohttp, os, inspect, logging, functools,asyncio

from urllib import parse
from aiohttp import web
from apis import APIError

#高阶函数get，用于路由GET的装饰器
# @get('path')
def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='GET'
        wrapper.__route__=path
        return wrapper
    return decorator

# for 'POST', the same as 'GET'
# @post('path')
def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='POST'
        wrapper.__route__=path
        return wrapper
    return decorator

#啥 如其名
# 获取 无默认值的 命名关键词参数
#(a,b,*,key_1,key_2) 即key_1&key_2
def get_required_kw_args(fn):
    agrs=[]
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        #若为关键字参数，并且默认值为空，则获取参数名并组装成为tuple返回
        if param.kind==inspect.Parameter.KEYWORD_ONLY and param.default==inspect.Parameter.empty:
            agrs.append(name)
    return tuple(agrs)

#获取命名关键字参数
#(a,b,*,key_1=v1,key_2) 即key_1&key_2
def get_named_kw_args(fn):
    args=[]
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        #只要求有关键字参数
        if param.kind==inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

#判断是否有命名关键字参数
def has_named_kw_args(fn):
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind==inspect.Parameter.KEYWORD_ONLY:
            return True

#判断是否有（可变）关键字参数
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

#判断是否有 参数名为'request'的参数，并且要求其位置在最后
def has_request_arg(fn):
    sig=inspect.signature(fn)
    params=sig.parameters
    found=False
    for name,param in params.items():
        if name=='request':
            found=True
            continue
        #如果已经找到了'request'参数，其后仍有参数且这些参数不是 可变参数&命名关键字参数&关键字参数 则说明其后仍有位置参数，'request'非最后的位置参数，则报错
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found

#重新封装Handler，让它能够自动识别提取参数并成为一个RequestHandler对象
class RequestHandler(object):

    def __init__(self,app,fn):
        self._app=app
        self._func=fn#handler 视图函数
        #判定视图函数具有的参数类型
        self._has_request_arg=has_request_arg(fn)
        self._has_var_kw_arg=has_var_kw_arg(fn)
        self._has_named_kw_args=has_named_kw_args(fn)
        self._named_kw_args=get_named_kw_args(fn)
        self._required_kw_args=get_required_kw_args(fn)

    #提取request中的参数，若Handler有关键字函数、命名关键字函数则需要查询request中是否提供了相应的参数，无则报错
    async def __call__(self, request):
        kw = None#所有参数的集合
        #若是Handler里有关键字参数or命名关键字参数，则Handler处理的request不止包含path，需要根据Content-type提取参数值
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            #request为POST时
            if request.method == 'POST':
                #无content-type报错
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                #同意 content-type 格式为小写，方便以下判断
                ct = request.content_type.lower()
                #json格式则获取json，request会自动将json转换为dict，判断params不为dict则json数据不规范，报错
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                #若为表单数据 用 request.post()获取
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                #其他类型不支持
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            #For 'GET' method， 从string中提取参数
            if request.method == 'GET':
                qs = request.query_string#得到URL查询语句
                if qs:
                    # 解析url?后面的内容
                    # qs='first=v1,v2&second=v3'
                    # parse.parse_qs(qs,True),items()
                    # >>>dict([('first',['v1','v2']),('second',['v3'])])
                    kw = dict()
                    #True 表示不忽略空格
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        #若request中无参数
        #request.match_info 返回dict对象。
        #若存在可变路由 /a/{name}, 可匹配path为 /a/jack/c 的request
        #则request.match_info返回{name:jack}
        if kw is None:
            kw = dict(**request.match_info)
        #若是已从request中提取到一些参数
        else:
            #检索Handler中需要的参数，过滤掉不需要的parmas
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        #若是Handler需要 request ，则将其作为参数传递
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        #尝试用包装好的params调用Handler
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

#app 为一个web.application 对象，通过 app.router.add_static 添加 static 资源，
# app.router.add_route 添加被封装成 RequestHandler 的 handler 函数


def add_static(app):
    # 拼接static文件目录
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))

#检查 handler 具有 __method__ & __path__ 属性，无则报错，有则用RequestHandler封装并添加到路由
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

#自动扫描Handler函数，并将它们注册到router中
def add_routes(app, module_name):
    n = module_name.rfind('.')# ??? 从左侧开始检索，返回索引 若无则返回 1
    if n == (-1):
        # __import__('os',globals(),locals(),['path','pip'], 0) ,等价于from os import path, pip
        #相当于 import module 
        mod = __import__(module_name, globals(), locals()) 
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    # dir(mod) 获取mod的属性列表
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        #获取函数
        fn = getattr(mod, attr)
        #验证函数及其 method&route属性
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)