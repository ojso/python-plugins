from datetime import datetime
from python_plugins.sqla.db import Db
from python_plugins.sqla.orm import Mapped
from python_plugins.sqla.orm import mapped_column


db = Db()


class Demo(db.Model):
    __tablename__ = "demo"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


def test_db():
    assert getattr(db, "Model", None) is not None
    assert getattr(db, "engine", None) is None
    assert getattr(db, "Session", None) is None

    # db.init_session(echo=True)
    db.init_session()

    assert getattr(db, "engine", None) is not None
    assert getattr(db, "Session", None) is not None

    db.create_all()
    demo_1 = Demo(name="demo1")
    with db.Session() as session:
        session.add(demo_1)
        session.commit()
        s1 = session.get(Demo, 1)
        assert s1 is not None
        assert s1.name == "demo1"
