from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
import aiohttp_jinja2
from uuid import uuid4
from json import dumps
from app.database import users


async def add_user(request: Request):
    data = await request.post()

    print(data)
    user_id = str(data.get('user_id', ''))
    user_name = data.get('user_name', 'none')
    name = data.get('name')
    photo = data.get('photo')
    if not user_id:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id did not send'}))
    if not name:
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'name did not send'}))
    if not user_id.isdigit():
        return web.Response(text=dumps({'status': 'ERROR', 'message': 'user_id must be integer'}))
    else:
        user_id = int(user_id)

    if not photo:
        file_name = 'default.png'
    else:
        file_name = f'{uuid4()}-{photo.filename}'

    status = await users.add_user(user_id=user_id, user_name=user_name, name=name, photo=file_name)

    if status:
        if photo:
            file = photo.file.read()
            with open(f'static/images/{file_name}', 'wb') as f:
                f.write(file)

        return web.Response(text=dumps({'status': 'SUCCESS', 'message': 'user was created'}))
    else:
        return web.Response(text=dumps({'status': 'WARNING', 'message': 'user already in system'}))


async def get_user_info(request: Request):
    user_id = int(request.query.get('user_id'))
    data = dict(await users.get_data(user_id))
    data['insert_date'] = data.get('insert_date').isoformat()
    return web.Response(text=dumps(data))


async def set_user_comment(request: Request):
    data = await request.post()
    user_id = int(data.get('user_id'))
    comment = data.get('comment')
    await users.update_comment(user_id, comment)
    return web.Response(text='OK')