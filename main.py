import asyncio
from sqlalchemy import select
from database import async_session
from models import User
async def test_database():
    async with async_session() as session:
        new_user = User(name='backend_dev')
        session.add(new_user)
        await session.commit()
        print(f'User was created by id: {new_user.id}')
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        print('\nUser list in database:')
        for user in users:
            print(f"- ID: {user.id}  |  Username: {user.name}")
if __name__ == '__main__':
    asyncio.run(test_database())