import base64
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import jinja2
# import aiohttp_jinja2


web_app = web.Application(client_max_size=1024 ** 3)

secret_key = base64.urlsafe_b64decode('Dcak6aZCayNHSzFXgsaXEiWF8_j0ujroHPp0b8_pyKo='.encode())
setup(web_app, EncryptedCookieStorage(secret_key))

# aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('static/templates'))

