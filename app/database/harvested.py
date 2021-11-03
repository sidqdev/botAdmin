from .core import connection
from asyncpg.connection import Connection


@connection
async def get_harvested_messages(conn: Connection):
    q = '''SELECT id, preview
           FROM admin_data_harvestedmessages'''
    return [dict(x) for x in await conn.fetch(q) or []]


@connection
async def get_harvested_message(id, conn: Connection):
    q = '''SELECT message_type_id, content
           FROM admin_data_harvestedmessages
           WHERE id = $1'''
    return await conn.fetchrow(q, id) or {}
