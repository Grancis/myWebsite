#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

@get('/')
async def index():
    return{
        '__template__':'index.html'
    }

@get('/blog')
async def blog_page():
    return{
        '__template__':'blog.html'
    }

@get('/coding')
async def coding_page():
    return{
        '__template__':'Coding.html'
    }

@get('/photography')
async def photography_page():
    return{
        '__template__':'photography.html'
    }

@get('/about')
async def about_page():
    return{
        '__template__':'about.html'
    }

@get('/api/get_coding_list')
async def get_coding_list(limit='7'):
    limit=int(limit)
    blogs= await Blog.findColumn(("`caption`","`summary`","`belong_to`","`subdivide`"), where = "`belong_to`='coding'", orderBy='create_at desc',limit = limit)
    return dict(blogs=blogs)

@get('/api/users')
async def api_get_users():
    users = await User.findAllOrMany(orderBy='create_at desc',limit=7,where="`name`='test'")
    for u in users:
        u.passwd = '******'
    return dict(users=users)
