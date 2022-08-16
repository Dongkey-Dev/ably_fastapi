from sqlalchemy_database import AsyncDatabase

# postgresql
async_db = AsyncDatabase.create(
    'postgresql+asyncpg://postgres:root@127.0.0.1:5432/admin')
