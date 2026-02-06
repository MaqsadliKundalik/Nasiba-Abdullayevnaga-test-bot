from tortoise import Tortoise, run_async
from utils.models import *

async def init():
    await Tortoise.init(
        db_url="sqlite:///db.sqlite3",
        modules={"models": ["utils.models"]}
    )
    cursor = Tortoise.get_connection("default").cursor()
    await cursor.execute("ALTER TABLE tests ADD COLUMN test_code VARCHAR(20)")

if __name__ == "__main__":
    run_async(init())