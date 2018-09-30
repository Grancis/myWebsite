import asyncio
import orm
import random
from models import User,Blog,Comment

async def test(loop):
    await orm.create_pool(loop,user='root',password='Grancis.',db='mywebsite')
    # u =User(name='test4',email='test%s@example.com' % random.randint(0,10000000),passwrd='abc123456',image='about:blank')
    # await u.save()
    u2=User.find('00000153829608582ece01d044b4a67ace4b6195156c0c000')
    print(u2('name'))


#要运行协程，需要使用事件循环 
if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test(loop))
        print('Test finished.')
        loop.close()