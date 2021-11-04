from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
import aiohttp_jinja2
from uuid import uuid4
from json import dumps
from app.database import users, chats, harvested


async def add_message(request: Request):
    data = await request.post()

    chat_id = str(data.get('chat_id', ''))
    user_id = str(data.get('user_id', ''))
    message_type = data.get('message_type', '')
    content = data.get('content', '')
    ignore = int(data.get('ignore', '0'))

    file = data.get('file')

    if not chat_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id did not send'}))
    if not chat_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id must be integer'}))
    else:
        chat_id = int(chat_id)

    if not user_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id did not send'}))
    if not user_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id must be integer'}))
    else:
        user_id = int(user_id)

    if message_type != 'text':
        file_bytes = file.file.read()
        file_name = f'files/{uuid4()}-{file.filename}'
        with open(f'static/{file_name}', 'wb') as f:
            f.write(file_bytes)
        content = file_name

    if content:
        await chats.add_message(chat_id, user_id, message_type, content, ignore=ignore)
    else:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'content did not send'}))

    return web.Response(text=dumps({'status': 'SUCCESS', 'message': 'message was sent'}))


async def get_harvested_messages(request: Request):
    data = await harvested.get_harvested_messages()
    return web.Response(text=dumps(data))


async def send_harvested_message(request: Request):
    data = await request.post()

    chat_id = str(data.get('chat_id', ''))
    user_id = str(data.get('user_id', ''))
    harvested_id = data.get('harvested_id', '')

    if not chat_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id did not send'}))
    if not chat_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id must be integer'}))
    else:
        chat_id = int(chat_id)

    if not user_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id did not send'}))
    if not user_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id must be integer'}))
    else:
        user_id = int(user_id)

    message_data = await harvested.get_harvested_message(harvested_id)
    await chats.add_message(chat_id, user_id, message_data.get('message_type_id'), message_data.get('content'))

    return web.Response(text=dumps({'status': 'SUCCESS', 'message': 'message was sent'}))
