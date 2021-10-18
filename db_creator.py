import os
from uuid import uuid4
dbname = input('Database name:' )
username = input('Username:' ) or dbname
password = input('Password: ') or uuid4().hex

create_db = f"sudo -u postgres psql -c 'create database {dbname}'" 
create_user = f"sudo -u postgres psql -c \"create user {username} with encrypted password '{password}'\""
grand_role = f"sudo -u postgres psql -c 'grant all privileges on database {dbname} to {username}'"

os.system(create_db)
os.system(create_user)
os.system(grand_role)
print(f'''dbname: {dbname}
username: {username}
password: {password}''')
