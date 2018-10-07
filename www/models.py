#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
Models for User, Blog, Comment
'''
__auther__='refer to Micheal Liao'

import time,uuid
from orm import Model,StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__='users'

    #定义类属性
    id=StringField(default=next_id,primary_key=True,ddl='varchar(50)')
    email=StringField(ddl='varchar(50)')
    passwrd=StringField(ddl='varchar(50)')
    admin=BooleanField()
    name=StringField(ddl='varchar(50)')
    image=StringField(ddl='varchar(500)')
    create_at=FloatField(default=time.time)


class Blog(Model):
    __table__='blogs'

    #定义类属性
    id=StringField(primary_key=True,default=next_id,ddl='varchar(50)')
    user_id=StringField(ddl='varchar(50)')
    user_name=StringField(ddl='varchar(50)')
    user_image=StringField(ddl='varchar(500)')
    caption=StringField(ddl='varchar(50)')
    summary=StringField(ddl='varchar(200)')
    content=TextField()
    belong_to=StringField(ddl='varchar(50)')#分类
    subdivide=StringField(ddl='varchar(50)')
    create_at=FloatField(default=time.time)

class Comment(Model):
    __table__='comments'

    #类属性
    id=StringField(primary_key=True,ddl='varchar(50)', default=next_id)
    blog_id=StringField(ddl='varchar(50)')
    user_id=StringField(ddl='varchar(50)')
    user_name=StringField(ddl='varchar(50)')
    user_image=StringField(ddl='varchar(50)')
    content=TextField()
    create_at=FloatField(default=time.time)

class PageNews(Model):
    __table__='page_news'

    id=StringField(primary_key=True,ddl='varchar(50)', default=next_id)
    home=StringField(ddl='varchar(50)')
    booking=StringField(ddl='varchar(100)')
    it=StringField(ddl='varchar(100)')
    news=StringField(ddl='varchar(100)')
    thinking=StringField(ddl='varchar(100)')
    coding=StringField(ddl='varchar(200)')
    photography=StringField(ddl='varchar(200)')
    create_at=FloatField(default=time.time)
