#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

@get('/')
async def index(request):
    return '<h1>Grancis</h1>'

@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='create_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)