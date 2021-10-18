from app.web.dumper import web_task
import asyncio


loop = asyncio.get_event_loop()
loop.create_task(web_task())
loop.run_forever()
