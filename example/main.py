import asyncio
from requests import get, post
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InputFile, ContentTypes
from os import system, remove
import io


bot = Bot(token='1797143384:AAGwfSZteFJe9nokZ1dM7HG3E802xeUM11o')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start(message: Message):
    '''curl -X POST -F 'user_id=13131323322133' -F 'name=sdadadasd' -F photo=@default.png http://0.0.0.0:9999/addUser'''
    user_id = message.from_user.id
    name = message.from_user.first_name
    user_name = message.from_user.username
    photo = await message.from_user.get_user_profile_photos(limit=1)
    if photo.total_count:
        p = await bot.download_file_by_id(photo['photos'][0][0].file_id)
        with open('aaa.png', 'wb') as f:
            f.write(p.read())
        system(f"curl -X POST -F 'user_id={user_id}' -F 'name={name}' -F 'user_name={user_name}' -F photo=@aaa.png http://0.0.0.0:9999/addUser")
    else:
        post('http://0.0.0.0:9999/addUser', data={"user_id": user_id, "name": name, 'user_name': user_name})
    print(post('http://0.0.0.0:9999/createChat', data={"chat_id": user_id}).text)
    await message.answer('Чат открыт')


@dp.message_handler()
async def message_handler(message: Message):
    content = message.text
    user_id = message.from_user.id
    chat_id = user_id
    message_type = 'text'

    post('http://0.0.0.0:9999/sendMessage', data={'content': content,
                                                  'user_id': user_id,
                                                  'chat_id': chat_id,
                                                  'message_type': message_type})


@dp.message_handler(content_types=ContentTypes.PHOTO)
async def any_handler(message: Message):
    user_id = message.from_user.id
    print(message.photo)
    file = await message.photo[-1].download()
    filename = file.name
    message_type = 'image'
    system(f"curl -X POST -F 'chat_id={user_id}' -F 'user_id={user_id}' -F 'message_type={message_type}' -F file=@{filename} http://0.0.0.0:9999/sendMessage")
    remove(filename)
    if message.caption:
        post('http://0.0.0.0:9999/sendMessage', data={'content': message.caption,
                                                      'user_id': user_id,
                                                      'chat_id': user_id,
                                                      'message_type': 'text'})


@dp.message_handler(content_types=ContentTypes.VIDEO)
async def video_handler(message: Message):
    user_id = message.from_user.id
    print(message.video)
    file = await message.video.download()
    filename = file.name
    message_type = 'video'
    system(f"curl -X POST -F 'chat_id={user_id}' -F 'user_id={user_id}' -F 'message_type={message_type}' -F file=@{filename} http://0.0.0.0:9999/sendMessage")
    remove(filename)
    if message.caption:
        post('http://0.0.0.0:9999/sendMessage', data={'content': message.caption,
                                                      'user_id': user_id,
                                                      'chat_id': user_id,
                                                      'message_type': 'text'})


@dp.message_handler(content_types=ContentTypes.VOICE)
async def audio_handler(message: Message):
    print(1)
    user_id = message.from_user.id
    data = message.voice or message.audio[0]
    file = await data.download()
    filename = file.name
    message_type = 'audio'
    system(f"curl -X POST -F 'chat_id={user_id}' -F 'user_id={user_id}' -F 'message_type={message_type}' -F file=@{filename} http://0.0.0.0:9999/sendMessage")
    remove(filename)
    if message.caption:
        post('http://0.0.0.0:9999/sendMessage', data={'content': message.caption,
                                                      'user_id': user_id,
                                                      'chat_id': user_id,
                                                      'message_type': 'text'})


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def any_handler(message: Message):
    user_id = message.from_user.id
    print(message.document)
    file = await message.document.download()
    filename = file.name
    message_type = 'document'
    system(f"curl -X POST -F 'chat_id={user_id}' -F 'user_id={user_id}' -F 'message_type={message_type}' -F file=@{filename} http://0.0.0.0:9999/sendMessage")
    remove(filename)
    if message.caption:
        post('http://0.0.0.0:9999/sendMessage', data={'content': message.caption,
                                                      'user_id': user_id,
                                                      'chat_id': user_id,
                                                      'message_type': 'text'})


async def update():
    try:
        data = get('http://0.0.0.0:9999/getUpdates').json()
        if data:
            print(data)
        for msg in data:
            user_id = msg.get('chat_id')
            if msg.get('message_type_id') == 'text':
                text = msg.get('content')
                await bot.send_message(user_id, text)
            else:
                file = msg.get('content')
                file_bytes = get('http://0.0.0.0:9999/static/' + file).content
                with open(file.split('/')[-1], 'wb') as f:
                    f.write(file_bytes)
                if msg.get('message_type_id') == 'image':
                    await bot.send_photo(user_id, InputFile(file.split('/')[-1]))
                elif msg.get('message_type_id') == 'video':
                    await bot.send_video(user_id, InputFile(file.split('/')[-1]))
                elif msg.get('message_type_id') == 'audio':
                    await bot.send_audio(user_id, InputFile(file.split('/')[-1]))
                elif msg.get('message_type_id') in ('document', 'application'):
                    await bot.send_document(user_id, InputFile(file.split('/')[-1]))
                remove(file.split('/')[-1])

    except Exception as e:
        print(e)

    await asyncio.sleep(0.2)
    asyncio.get_event_loop().create_task(update())


loop = asyncio.get_event_loop()
loop.create_task(update())
loop.create_task(dp.start_polling())
loop.run_forever()




