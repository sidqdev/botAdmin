from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
import aiohttp_jinja2
from uuid import uuid4
from json import dumps
from app.database import users
from app.database import chats


async def index(request: Request):
    with open('static/templates/index.html', 'r') as file:
        text = file.read()
    return web.Response(text=text, content_type='text/html')



