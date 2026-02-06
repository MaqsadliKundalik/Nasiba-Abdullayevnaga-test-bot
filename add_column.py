from tortoise import Tortoise, run_async
from utils.models import *

async def init():
    await Tortoise.init(
        db_url="sqlite:///db.sqlite3",
        modules={"models": ["utils.models"]}
    )
    conn = Tortoise.get_connection("default")
    await conn.execute_script("ALTER TABLE tests ADD COLUMN test_code VARCHAR(20)")
    print("Column 'test_code' added successfully.")

if __name__ == "__main__":
    run_async(init())