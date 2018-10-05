#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
logging.basicConfig(level=logging.INFO)

from coroweb import get, post

from aiohttp import web

from filters import datetime_filter
from models import User, Comment, Blog, next_id
from config import configs

from apis import APIError,APIValueError,APIPermissionError,APIResourceNotFound

COOKIE_NAME='Grancis_session'
_COOKIE_KEY=configs.session.secret

def user2cookie(user,max_age):
    '''
    generate cookie string by user
    '''
    #build cookie string by : id-expires-sha1
    #sha1 build by : uid-upwd-expires-_COOKIE_KEY
    expires=str(int(time.time()+max_age))
    s='%s-%s-%s-%s' %(user.id,user.passwrd,expires,_COOKIE_KEY)
    L=[user.id,expires,hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    '''
    parse cookie and load user if cookie is valid
    '''
    #先判断是否存在cookie
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3 :
            return None
        uid,expires,sha1=L
        if int(expires)<time.time():
            return None#过期
        user= await User.find(uid)
        if user is None:
            return None
        s='%s-%s-%s-%s' % (uid,user.passwrd,expires,_COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            return None
        user.passwrd='********'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/login_or_signin')
async def login_or_signin():
    return {
        '__template__' : 'login_or_signin.html'
        
    }

def set_user(request):
    if request.__user__ is not None:
        name=request.__user__.name
        a_link_to='/user_page'
    else:
        name='/*login*/'
        a_link_to='/login_or_signin'
    return (name,a_link_to)

@get('/')
async def index(request):
    name,a_link_to=set_user(request)
    return{
        '__template__' : 'index.html',
        'name' : name,
        'href' : a_link_to
    }


@get('/blog')
async def blog_page(request):
    name,a_link_to=set_user(request)
    return{
        '__template__':'blog.html',
        'name' : name,
        'href' : a_link_to
    }

@get('/coding')
async def coding_page(request):
    name,a_link_to=set_user(request)
    return{
        '__template__':'Coding.html',
        'name' : name,
        'href' : a_link_to
    }

@get('/photography')
async def photography_page(request):
    name,a_link_to=set_user(request)
    return{
        '__template__':'photography.html',
        'name' : name,
        'href' : a_link_to
    }

@get('/about')
async def about_page(request):
    name,a_link_to=set_user(request)
    return{
        '__template__':'about.html',
        'name' : name,
        'href' : a_link_to
    }

@get('/user_page')
async def user_page(request):
    if request.__user__ is not None:
        user=request.__user__
        user.create_at=datetime_filter(user.create_at)
    else:
        user=User(name='未登录',email="未登录",passwrd="******")
    return{
        '__template__':'user_page.html',
        'user':user
    }

@get('/manage/push_blog_page')
async def push_blog_page(request):
    name,a_link_to=set_user(request)
    return{
        '__template__':'push_blog.html',
        'name' : name,
        'href' : a_link_to
    }

@post('/api/get_blog_list')
async def get_coding_list(*,belong_to,page,num):
    page=int(page)
    num=int(num)
    cnt= await Blog.findNumber('count(id)',where="belong_to='"+belong_to+"'")
    page_max=cnt//num +1
    if page>page_max:
        page=page_max
    top=(page-1)*num
    limit=(int(top),int(num))
    blogs= await Blog.findColumn(("`id`,`caption`","`summary`","`belong_to`","`subdivide`","`summary`","`create_at`"), where = "`belong_to`='coding'", orderBy='create_at desc',limit = limit)
    for d in blogs:
        for k,v in d.items():
            if k=='create_at':
                d[k]=datetime_filter(v)
    return dict(blogs=blogs,max_page=page_max,page=page)

# @get('/api/users')
# async def api_get_users():
#     users = await User.findAllOrMany(orderBy='create_at desc',limit=7,where="`name`='test'")
#     for u in users:
#         u.passwd = '******'
#     return dict(users=users)

@post('/api/authenticate')
async def authenticate(*,email,passwrd):
    if not email:
        raise APIValueError('email','Invalid email')
    if not passwrd:
        raise APIValueError('passwrd','Invalid password')
    users= await User.findAllOrMany('email=?',[email])
    if len(users)==0:
        raise APIValueError('email','email is not exist')
    user=users[0]
    #check password
    #password was build by uid:row_passwrd
    sha1=hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwrd.encode('utf-8'))
    if user.passwrd != sha1.hexdigest():
        raise APIValueError('passwrd','Invalid password')
    #authenticate ok, set cookie
    r=web.Response()
    r.set_cookie(COOKIE_NAME,user2cookie(user,86400),max_age=86400,httponly=True)
    user.passwrd='********'
    r.content_type='application/json'
    r.body = json.dumps(user,ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
async def signout(request):
    referer=request.headers.get('Referer')
    r=web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME,'-deleted-',max_age=0,httponly=True)
    logging.info('user signed out')
    return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
# _RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
#去掉了密码的sha1验证 并不知道这是啥 为什么只能 0-9 a-f

@post('/api/register_user')
async def register_user(*,email,name,passwrd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwrd:
        raise APIValueError('passwrd')
    users= await User.findAllOrMany('email=?',[email])
    if len(users)>0:
        raise APIValueError('register:failed','email','email is already in case.')
    uid=next_id()
    sha1_passwrd='%s:%s' % (uid,passwrd)
    user = User(id=uid, name=name.strip(), email=email, passwrd=hashlib.sha1(sha1_passwrd.encode('utf-8')).hexdigest(),image='about:blank')
    await user.save()
    logging.debug('保存用户...')
    #make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME,user2cookie(user,86400),max_age=86400,httponly=True)
    user.passwrd='********'
    r.content_type='application/json'
    r.body = json.dumps(user,ensure_ascii=False).encode('utf-8')
    return r


@post('/manage/api/push_blog')
async def push_blog(request,*,caption,summary,content,belong_to,subdivide):
    if not caption or not caption.strip():
        raise APIError('caption')
    if not summary or not summary.strip():
        raise APIError('summary')
    if not content or not content.strip():
        raise APIError('content')
    if not belong_to or not belong_to.strip():
        raise APIError('belong_to')
    if not subdivide or not subdivide.strip():
        raise APIError('subdivide')
    user=None
    if request.__user__ is not None:
        user=request.__user__
    else:
        raise APIError('user')
    blog=Blog(caption=caption,summary=summary,content=content,belong_to=belong_to,subdivide=subdivide,user_id=user.id,user_name=user.name,user_image=user.image)
    affected = await blog.save()
    if affected != 1:
        error='affected rows : %s' %affected
    else:
        error='none'
    blog.content='*****'
    blog.create_at=datetime_filter(blog.create_at)
    return dict(blog=blog,error=error)

