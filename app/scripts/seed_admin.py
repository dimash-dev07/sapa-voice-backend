import asyncio

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole


async def main() -> None:
    async with SessionLocal() as s:
        exists = await s.scalar(select(User).where(User.email == "admin@example.com"))
        if exists:
            print("Admin already exists")
            return
        s.add(
            User(
                email="admin@example.com",
                hashed_password=hash_password("admin12345"),
                role=UserRole.ADMIN,
            )
        )
        await s.commit()
        print("Created admin@example.com / admin12345")


if __name__ == "__main__":
    asyncio.run(main())