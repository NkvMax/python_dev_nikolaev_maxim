from datetime import datetime

from faker import Faker
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.models import Author, Blog, Post, Log
from app.db.session import SessionContent, SessionLogs
from sqlalchemy import select
from app.db.models import Author
from app.db.session import SessionContent, SessionLogs

fake = Faker("ru_RU")


def seed_content() -> None:
    with SessionContent() as db:  # type: Session
        authors = [
            Author(login=fake.user_name(), email=fake.email()) for _ in range(3)
        ]
        db.add_all(authors)
        db.flush()

        for a in authors:
            blog = Blog(
                owner_id=a.id,
                name=fake.sentence(nb_words=3),
                description=fake.text(),
            )
            db.add(blog)
            db.flush()

            for _ in range(3):
                db.add(
                    Post(
                        header=fake.sentence(nb_words=4),
                        text=fake.text(max_nb_chars=120),
                        author_id=a.id,
                        blog_id=blog.id,
                    )
                )
        db.commit()



def seed_logs() -> None:
    # берем авторов ORM-запросом
    with SessionContent() as content:
        stmt = select(Author.id).limit(3)
        users = [row.id for row in content.execute(stmt).all()]

    # пишем логи во вторую БД
    with SessionLogs() as logs:
        logs.add_all(
            [
                Log(
                    datetime=datetime.utcnow(),
                    user_id=u,
                    space_type_id=1,   # global
                    event_type_id=1,   # login
                )
                for u in users
            ]
        )
        logs.commit()


if __name__ == "__main__":
    seed_content()
    seed_logs()
    print(">>> demo data inserted")
