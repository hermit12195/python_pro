import os

import asyncpg

async def db_conn():
    return await asyncpg.connect(
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DB'),
        host=os.getenv('POSTGRES_HOST'))

async def user_list(tg_id):
    conn = await db_conn()
    u_list = await conn.fetch('SELECT tg_id, tg_name, email, phone FROM app_monuser WHERE tg_id=$1', tg_id)
    await conn.close()
    return u_list

async def update_user(tg_id, name, email, phone):
    conn = await db_conn()
    await conn.execute(
        "UPDATE app_monuser SET tg_id=$1, tg_name=$2, phone=$3 WHERE email=$4",
        tg_id, name, phone, email)
    await conn.close()

async def email_check(email):
    conn = await db_conn()
    u_list=await conn.fetchrow('SELECT * FROM app_monuser WHERE email=$1', email)
    await conn.close()
    return u_list

async def server_list(tg_id):
    conn = await db_conn()
    user=await conn.fetchrow('SELECT id FROM app_monuser WHERE tg_id=$1', tg_id)
    s_list=await conn.fetch('SELECT server_name, server_ip, os_name, status FROM app_server WHERE owner_id=$1', user["id"])
    await conn.close()
    return s_list





