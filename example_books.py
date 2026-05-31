# example_books.py
# Adds a demo user and example books for local testing.

from passlib.context import CryptContext

from database.database_engine import SessionLocal
from database.database_models import Books, Users


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


example_books = [
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "description": "A beginner-friendly introduction to Python programming.",
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "A practical guide to writing readable and maintainable code.",
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "description": "A deep dive into scalable data systems and distributed applications.",
    },
    {
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "description": "Advanced Python concepts for writing idiomatic Python code.",
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt and David Thomas",
        "description": "Classic software engineering practices for professional developers.",
    },
]


def get_or_create_demo_user(db):
    demo_user = db.query(Users).filter(Users.username == "demo_user").first()

    if demo_user:
        print("Demo user already exists: demo_user")
        return demo_user

    demo_user = Users(
        username="demo_user",
        email="demo@example.com",
        first_name="Demo",
        last_name="User",
        role="admin",
        hashed_password=bcrypt_context.hash("demo_password"),
        is_active=True,
    )

    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    print("Created demo user: demo_user / demo_password")
    return demo_user


def seed_books() -> None:
    db = SessionLocal()

    try:
        demo_user = get_or_create_demo_user(db)
        added_count = 0

        for book_data in example_books:
            existing_book = (
                db.query(Books)
                .filter(Books.title == book_data["title"])
                .first()
            )

            if existing_book:
                print(f"Skipped existing book: {book_data['title']}")
                continue

            book = Books(
                title=book_data["title"],
                author=book_data["author"],
                description=book_data["description"],
                owner_id=demo_user.id,
            )

            db.add(book)
            added_count += 1

        db.commit()
        print(f"Seed complete. Added {added_count} new books.")

    except Exception as error:
        db.rollback()
        print(f"Error seeding books: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_books()