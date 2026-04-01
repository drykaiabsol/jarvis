import aiosqlite
from logger import setup_logger

log = setup_logger("database")

DATABASE_PATH = "jarvis.db"

async def get_db():
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    return db