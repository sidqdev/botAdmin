from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
import aiohttp_jinja2
from uuid import uuid4
from json import dumps
from app.database import users
from app.database import chats


async def get_updates(request: Request):
    data = await chats.get_updates()
    chat = list()
    if data:
        for i in data:
            cht = dict(i)
            cht['insert_date'] = cht.get('insert_date').isoformat()
            chat.append(cht)

    return web.Response(text=dumps(chat), content_type='application/json')
