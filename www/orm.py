#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import logging
import aiomysql
import asyncio

#日志
def log(sql,args=()):
    logging.info('SQL: %s', sql)

#异步创建连接池函数
#para:
#loop: 异步loop
#**kw: mysql数据库连接信息，无则用默认值连接
async def create_pool(loop,**kw):
    logging.info('creating mysql connection pool...')
    global __pool
    __pool= await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )

#异步select语句，使用SQL参数格式，函数内转换我Mysql格式
async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    #从pool中异步获取一个连接
    async with __pool.get() as conn:
        #从conn中异步获取一个指针
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?','%s'), args or ())
            if size:
                rs= await cur.fetchmany(size)
            else:
                rs= await cur.fetchall()
            logging.info('rows returned: %s' % len(rs))
            return rs

#异步execute, insert delete 都为execute
async def execute(sql, args, autocommit=True):
    log(sql)
    global __pool
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

#用于构造SQL语句的参数
#创建n个 ?,?,?
def create_args_string(num):
    L=[]
    for i in range(num):
        L.append('?')
    return ','.join(L)

#Field 基类,StringField等都继承此类
#一列数据具有的基本属性 name column_type primary_key default
class Field(object):
    def __init__(self,name, column_type, primary_key, default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default
    def __str__(self):
        return ('%s,%s,%s' %(self.__class__.__name__,self.column_type,self.name))

#继承Field类得到各个Field
class StringField(Field):
    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
    def __init__(self,name=None,default=False):
        super().__init__(name,'boolean', False, default)

class IntegerField(Field):
    def __init__(self,name=None,primary_key=False,default=0):
        super().__init__(name,'bigint',primary_key, default)

class FloatField(Field):
    def __init__(self,name=None,primary_key=False,default=0.0):
        super().__init__(name, 'real',primary_key, default)

class TextField(Field):
    def __init__(self,name=None,default=None):
        super().__init__(name,'text',False,default)

#Model类的父类
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        #排除Model类本身
        if name=='Model':
            return type.__new__(cls,name,bases,attrs)
        else:
            #先拿到table的name
            table_name=attrs.get('__table__',None) or name
            logging.info('found Model:%s (table:%s)' % (name, table_name))
            #获取所有的Field 和主键名
            mappings=dict() #保存表中Field及其对应的值
            fields=[]
            primaryKey=None
            for k,v in attrs.items():
                if isinstance(v,Field) :
                    logging.info('found mapping:  %s==>%s ' %(k,v))
                    mappings[k]=v
                    #寻找主键，不是主键的appen到fields中
                    if v.primary_key:
                        #找到主键
                        logging.info('found primary_key: %s' %name)
                        if primaryKey:
                            #若之前已经找到过主键，则出现主键重复错误
                            raise RuntimeError('Duplicate primary key for field: %s' % k)
                        primaryKey=k
                    else:
                        fields.append(k)
            if not primaryKey:
                raise RuntimeError('Primary key not found')
            for k in mappings.keys():
                attrs.pop(k)
            escaped_fields=list(map(lambda f: '`%s`' %f, fields)) #除了主键以外的Field格式化为`field` 利用__str__ 
            attrs['__mappings__']=mappings#保存属性与列的对应关系
            attrs['__table__']=table_name
            attrs['__primary_key__']=primaryKey#主键属性名
            attrs['__fields__']=fields#除了主键以外的属性名
            #构造默认的SELECT INSERT UPDATE和DELETE语句
            attrs['__select__']='SELECT `%s`, %s FROM `%s`' %(primaryKey,','.join(escaped_fields),table_name)
            attrs['__insert__']='INSERT INTO `%s` (%s, `%s`) VALUES (%s)' %(table_name,','.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields)+1))
            attrs['__update__']='UPDATE `%s` SET %s WHERE `%s`=?' %(table_name, ','.join(map(lambda f:'`%s=?' %(mappings.get(f).name or f),fields)),primaryKey)
            attrs['__delete__']='DELETE FROM `%s` WHERE `%s`=?' %(table_name,primaryKey)
            return type.__new__(cls,name,bases,attrs)


#定义Model类，所有类都需要有的操作
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)