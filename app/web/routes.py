from app.web.loader import web_app
from aiohttp import web
from app.web.handlers import users, chats, renders, messages, updates


web_app.router.add_route('get', '/', renders.index, name='IndexRender')

web_app.router.add_route('post', '/addUser', users.add_user, name='AddUser')
web_app.router.add_route('post', '/createChat', chats.create_chat, name='CreateChat')
web_app.router.add_route('get', '/getUserInfo', users.get_user_info, name='GetUserInfo')

web_app.router.add_route('get', '/getChats', chats.get_chats, name='GetChats')
web_app.router.add_route('get', '/getChat', chats.get_chat, name='GetChat')

web_app.router.add_route('post', '/sendMessage', messages.add_message, name='AddMessage')
web_app.router.add_route('post', '/setChatStatus', chats.set_chat_status, name='SetChatStatus')

web_app.router.add_route('get', '/getUpdates', updates.get_updates, name='GetUpdates')

web_app.router.add_static('/static/', 'static', name='static')
