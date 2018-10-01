#!/usr/bin/env python3
#-*- encoding"utf-8 -*-

'''refer to Michael Liao'''

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

import orm
from coroweb import add_route,add_routes

# initial jinja2
def init_jinja2(app,**kw):
    logging.info('initialling jinja2...')
    #初始化参数
    options=dict(
        autoescape=kw.get('autoescape',True),
        #代码块开始结束标志
        block_start_string=kw.get('block_start_string','{%'),
        block_end_string=kw.get('block_end_string','%}'),
        #变量起始标志
        variable_start_string=kw.get('variable_start_string','{{'),
        variable_end_string=kw.get('variable_end_string','}}'),
        #自动加载修改后的文件模板
        auto_reload=kw.get('auto_reload',True)
    )

    #写入路径
    path=kw.get('path',None)
    if path is None:
        #当前运行脚本的绝对路径拼接上 'templates'
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
    logging.info('set jinja2 template path: %s' %path)
    # Environment类是jinja2的核心类，用来保存配置、全局对象以及模板文件的路径
	# FileSystemLoader类加载path路径中的模板文件
    #将 options&path 载入env
    env=Environment(loader=FileSystemLoader(path),**options)
    #扫描过滤器
    filters=kw.get('filters',None)
    if filters is not None:
        for name,fil in filters:
            env.filters[name]=fil
    app['__templating__']=env

#编写一个过滤器
def datetime_filter(t):
    delta=int(datetime.time()-t)
    if delta<60:
        return u'1分钟前'
    if delta<3600:
        return u'%s分钟前' %(delta//60)
    if delta<86400:
        return u'%s小时前' %(delta//3600)
    if delta<604800:
        return u'%s天前' %(delta//86400)
    dt=datetime.fromtimestamp(t)
    return u'%s年%s月%s日' %(dt.year, dt.month, dt.day)


#middleware 编写，对handler返回的response进行重新包装以加入新的功能

#用于输出日志的middleware
async def logger_factory(app,handler):
    async def logger(request):
        logging.info('Request: %s %s' %(request.method, request.path))
        return (await handler(handler))
    return logger

#将handler处理后得到的返回数据重新包装得到web.Response
async def response_factory(app,handler):
    async def response(request):
        logging.info('Response handler...')
        r= await handler(request)
        logging.info('Response result= %s' %str(r))
        #根据r的数据类型进行分类处理
        #web.StreamResponse 是所有Response的父类，可以直接返回
        if isinstance(r,web.StreamResponse):
            return r
        if isinstance(r,bytes):
            resp=web.Response(body=r) #构造http响应内容
            resp.content_type='application/octet-stream'
            return resp
        if isinstance(r,str):
            if r.startswith('redirect'):
                #重定向字符
                return web.HTTPFound(r[9:]) #重定向
            resp=web.Response(body=r.encode('utf-8'))
            resp.content_type='text/html;charset=utf-8'
            return resp
        #dict 类型有可能是 json或者 template
        if isinstance(r,dict):
            template=r.get('__template__',None)
            if template is None:#json
                resp=web.Response(body=json.dump(r,ensure_ascii=False,default=lambda obj: obj.__dict__).encode('utf-8'))
                resp.content_type='application/json;charset=utf-8'
                return resp
            else:
                #非json则是template,返回模板
                resp=web.Response(body=app['__template__'].get_template(template).render(**r))
                resp.content_type='text/html;charset=utf-8'
                return resp
        #int类型为http响应码
        if isinstance(r,int):
            resp=web.Response(status=r)
            return resp
        # tuple 包含响应码和描述
        if isinstance(r,tuple) and len(r)==2:
            (status_code,msg)=r
            # 100~600的响应码有意义
            if isinstance(status_code,int) and (100<=status_code<600):
                resp=web.Response(status=status_code,text=str(msg))
                return resp
        #不满足以上条件则默认返回
        resp=web.Response(body=str(r).encode('utf-8'))
        resp.content_type='text/plain;charset=utf-8'
        return resp
    return response

