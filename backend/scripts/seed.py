from app.infrastructure.database import SessionLocal
from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash

def seed_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(UserORM).filter(UserORM.email == "m@example.com").first()
        if not user:
            new_user = UserORM(
                name="Test User",
                email="m@example.com",
                hashed_password=get_password_hash("password")
            )
            db.add(new_user)
            db.commit()
            print("User seeded successfully.")
        else:
            print("User already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()
