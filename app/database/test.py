import asyncio
from . import users
from . import chats


async def task():
    print(await users.add_user(user_id=13, user_name='Ivan2', name='ivan2'))
    print(await chats.get_chats())
    print(await chats.get_chat(12))
    print(await chats.get_updates())
    await chats.add_message(12, 12, 'text', 'Привет')

loop = asyncio.get_event_loop()
