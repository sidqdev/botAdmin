from .core import connection
from asyncpg.connection import Connection


@connection
async def get_chats(conn: Connection = None) -> list:
    q = '''SELECT admin_data_webusers.name AS name, 
                  admin_data_webusers.photo AS photo,
                  admin_data_chats.chat_id AS chat_id,
                  admin_data_chats.status AS status,
                  (SELECT msg
                   FROM admin_data_webmessages AS msg
                   INNER JOIN admin_data_chats AS cht ON 
                              msg.chat_id = cht.chat_id
                   WHERE cht.chat_id = admin_data_chats.chat_id
                   ORDER BY msg.insert_date DESC
                   LIMIT 1) AS last_message
                   
          FROM admin_data_chats
          INNER JOIN admin_data_webusers ON admin_data_webusers.user_id = admin_data_chats.chat_id 
          ORDER BY (CASE 
                        WHEN 
                            (SELECT msg.id
                            FROM admin_data_webmessages AS msg
                            INNER JOIN admin_data_chats AS cht ON 
                                       msg.chat_id = cht.chat_id
                            WHERE cht.chat_id = admin_data_chats.chat_id
                            ORDER BY msg.insert_date DESC
                            LIMIT 1) > 0 
                        THEN 
                            (SELECT msg.insert_date
                            FROM admin_data_webmessages AS msg
                            INNER JOIN admin_data_chats AS cht ON 
                                       msg.chat_id = cht.chat_id
                            WHERE cht.chat_id = admin_data_chats.chat_id
                            ORDER BY msg.insert_date DESC
                            LIMIT 1) 
                        ELSE admin_data_chats.create_date
                     END) DESC  
            '''

    return await conn.fetch(q)


@connection
async def create_chat(chat_id, conn: Connection = None) -> int:
    q = '''INSERT INTO admin_data_chats(chat_id, create_date, status)
           VALUES($1, NOW(), 'opened')
           ON CONFLICT(chat_id) DO NOTHING
           RETURNING (CASE 
                        WHEN (SELECT chat_id FROM admin_data_chats WHERE chat_id=$1) > 0 THEN 0
                        ELSE 1
                      END) AS status'''

    return await conn.fetchval(q, chat_id)


@connection
async def get_chat(chat_id, conn: Connection = None) -> list:
    q = '''SELECT chat_.chat_id AS chat_id,
                  chat_.status AS status,
                  message_.message_type_id AS message_type,
                  message_.content AS content,
                  message_.insert_date AS insert_date,
                  
                  user_.user_id AS user_id,
                  user_.name AS name,
                  user_.photo AS photo
                  
           FROM admin_data_chats AS chat_
           INNER JOIN admin_data_webmessages AS message_ ON message_.chat_id = chat_.chat_id
           INNER JOIN admin_data_webusers AS user_ ON user_.user_id = message_.from_user_id
           WHERE chat_.chat_id = $1
           ORDER BY message_.insert_date'''

    return await conn.fetch(q, chat_id)


@connection
async def add_message(chat_id, user_id, message_type, content, conn: Connection = None):
    q = '''INSERT INTO admin_data_webmessages(insert_date, chat_id, from_user_id, message_type_id, content)
           VALUES(NOW(), $1, $2, $3, $4)
           RETURNING id'''

    id = await conn.fetchval(q, chat_id, user_id, message_type, content)
    if user_id == 0:
        q = '''INSERT INTO admin_data_messageupdates(message_id, status)
               VALUES($1, false)'''
        await conn.fetch(q, id)
        q = '''UPDATE admin_data_chats
               SET status='opened'
               WHERE chat_id=$1'''
        await conn.fetch(q, chat_id)


@connection
async def get_updates(conn: Connection = None):
    q = '''UPDATE admin_data_messageupdates AS upd_
           SET status = true
           FROM admin_data_webmessages AS msg_ 
           WHERE upd_.status = false AND msg_.id = upd_.message_id
           RETURNING *'''
    return await conn.fetch(q)


@connection
async def set_chat_status(chat_id, status, conn: Connection = None):
    q = '''UPDATE admin_data_chats
           SET status = $2
           WHERE chat_id = $1'''
    await conn.fetch(q, chat_id, status)
