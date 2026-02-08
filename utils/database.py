from tortoise import Tortoise
from utils.models import Tests

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['utils.models']}
    )
    await Tortoise.generate_schemas()
    conn = Tortoise.get_connection("default")
    # Check table names
    all_tests = await Tests.all()
    for test in all_tests:
        if not test.test_code:
            test.test_code = str(test.id)
            await test.save()