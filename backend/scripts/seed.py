import asyncio

from sqlalchemy import select

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash


async def seed_user() -> None:
    async with AsyncSessionLocal() as db:
        try:
            # Check if user already exists
            result = await db.execute(
                select(UserORM).where(UserORM.email == "m@example.com")
            )

            user = result.scalar_one_or_none()
            if not user:
                new_user = UserORM(
                    name="Test User",
                    email="m@example.com",
                    hashed_password=get_password_hash("password"),
                )
                db.add(new_user)
                await db.commit()
                print("User seeded successfully.")
            else:
                print("User already exists.")
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(seed_user())
