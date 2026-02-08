from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['utils.models']}
    )
    await Tortoise.generate_schemas()
    conn = Tortoise.get_connection("default")
    # Check table names
    res = await conn.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables in DB:", [r['name'] for r in res[1]])
    
    try:
        # Try to find the correct table name for 'Tests' model usually it is 'tests' or 'models_tests'
        await conn.execute_script("ALTER TABLE tests ADD COLUMN test_code VARCHAR(20)")
        print("Column 'test_code' added successfully.")
    except Exception as e:
        print(e)