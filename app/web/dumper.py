from app.web.routes import web_app
from aiohttp import web


async def web_task():
    print('webtask')
    runner = web.AppRunner(web_app)
    await runner.setup()
    print('runner')
    site = web.TCPSite(runner, '0.0.0.0', 4321)
    await site.start()
