from datetime import datetime
from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
import aiohttp_jinja2
from uuid import uuid4
from json import dumps
from app.database import users
from app.database import chats
import configparser


config = configparser.RawConfigParser()
config.read('config.ini')

server = dict(config['SERVER'])
ip = server.get('ip')


async def create_chat(request: Request):
    data = await request.post()
    chat_id = str(data.get('chat_id', ''))

    if not chat_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id did not send'}))
    if not chat_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id must be integer'}))
    else:
        chat_id = int(chat_id)

    status = await chats.create_chat(chat_id)
    if status:
        return web.Response(text=dumps({'status': 'SUCCESS', 'message': 'chat was created'}))
    else:
        return web.Response(text=dumps({'status': 'WARNING', 'message': 'chat already in system'}))


async def get_chats(request: Request):
    chat_list = await chats.get_chats()
    chat_list = [dict(x) for x in chat_list]
    for cht in chat_list:
        cht['photo'] = f'http://{ip}/static/images/{cht.get("photo")}'
        if cht.get('last_message'):
            last_message = dict(cht.get('last_message'))
            last_message['insert_date'] = last_message.get('insert_date').isoformat()
        else:
            last_message = {'content': 'Пусто', 'message_type': 'text'}
        cht['last_message'] = last_message
    return web.Response(text=dumps(chat_list), content_type='application/json')


async def get_chat(request: Request):
    chat_id = request.query.get('chat_id')

    if not chat_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id did not send'}))
    if not chat_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id must be integer'}))
    else:
        chat_id = int(chat_id)

    data = await chats.get_chat(chat_id)
    chat = list()
    if data:
        for i in data:
            cht = dict(i)
            cht['time'] = cht.get('insert_date').strftime('%H:%M')
            cht['time_st'] = cht.get('insert_date').timestamp()
            cht['insert_date'] = cht.get('insert_date').strftime('%d.%m.%Y - %H:%M:%S')
            chat.append(cht)
        
        i = 0
        while i < len(chat) - 1:
            if datetime.fromtimestamp(chat[i].get('time_st')).date() != datetime.fromtimestamp(chat[i+1].get('time_st')).date():
                mess = {
                    'message_type': 'time_splitter',
                    'content': datetime.fromtimestamp(chat[i+1].get('time_st')).strftime('%d.%m.%Y')
                }
                chat.insert(i+1, mess)
                i += 2
            else:
                i += 1

    # print(chat)
    return web.Response(text=dumps(chat), content_type='application/json')


async def set_chat_status(request: Request):
    data = await request.post()
    chat_id = str(data.get('chat_id', ''))
    status = str(data.get('status', ''))

    if not chat_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id did not send'}))
    if not chat_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'chat_id must be integer'}))
    else:
        chat_id = int(chat_id)

    if not status:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'status did not send'}))

    await chats.set_chat_status(chat_id, status)

    return web.Response(text=dumps({'status': 'SUCCESS', 'message': 'status was changed'}))



