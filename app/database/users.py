from .core import connection
from typing import Union
from asyncpg.connection import Connection


@connection
async def add_user(user_id: int,
                   user_name: str,
                   name: str,
                   photo: Union[str, None] = None,
                   conn: Connection = None) -> int:
    """
    :return 0 - already in database
    :return 1 - new user
    """

    if not photo:
        photo = 'default.png'

    q = '''INSERT INTO admin_data_webusers(user_id, user_name, name, photo, comment)
           VALUES($1, $2, $3, $4, '')
           ON CONFLICT(user_id) DO 
           UPDATE SET
               user_name = EXCLUDED.user_name,
               name = EXCLUDED.name,
               photo = EXCLUDED.photo

           RETURNING (CASE 
                        WHEN (SELECT user_id FROM admin_data_webusers WHERE user_id=$1) > 0 THEN 0
                        ELSE 1
                      END) AS status
           '''

    return await conn.fetchval(q, user_id, user_name, name, photo)


@connection
async def get_data(user_id, conn: Connection = None):
    q = '''SELECT * 
           FROM admin_data_webusers
           INNER JOIN admin_data_chats ON admin_data_chats.chat_id = admin_data_webusers.user_id
           WHERE admin_data_webusers.user_id = $1'''

    return await conn.fetchrow(q, user_id)


@connection
async def update_comment(user_id, comment, conn: Connection = None):
    q = '''UPDATE admin_data_webusers
           SET comment = $2
           WHERE user_id = $1'''

    await conn.fetch(q, user_id, comment)
