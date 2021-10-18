import asyncio
from app import database

loop = asyncio.get_event_loop()
loop.create_task(database.test.task())
loop.run_forever()
