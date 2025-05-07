import aiosqlite


async def init_db():
    async with aiosqlite.connect("montoolbot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone INTEGER)""")
        await db.commit()


async def create_user(id, name, phone):
    async with aiosqlite.connect("montoolbot.db") as session:
        await session.execute("INSERT INTO users (id, name, phone) VALUES(?, ?, ?)", (id, name, phone))
        await session.commit()

async def user_list(user_id):
    async with aiosqlite.connect("montoolbot.db") as session:
        cursor = await session.execute("SELECT id, name, phone FROM users WHERE id=?", (user_id,))
        return await cursor.fetchone()
