import pytest
import sqlite3
from datetime import datetime
from python_plugins.sqla.db import Db
from python_plugins.sqla.orm import select
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


def test_flask_db():
    """ """
    from flask import Flask

    db = Db()

    class Demo(db.Model):
        __tablename__ = "demo"
        id: Mapped[int] = mapped_column(primary_key=True)

    app = Flask(__name__)
    # Note: sqlite:///:memory: only available for single connection,
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    # app.config["SQLALCHEMY_ECHO"] = True
    db.init_app(app)

    # _get_scope_id without app context should raise RuntimeError
    with pytest.raises(RuntimeError):
        db._get_scope_id()

    with app.app_context():
        print("engine pool ID:", id(db.engine.pool))
        print("session connection ID:", id(db.session.connection()))
        scope_id_1 = db._get_scope_id()
        db.create_all()  # create tables
        demo_1 = Demo()
        db.session.add(demo_1)
        db.session.commit()

    with app.app_context():
        print("engine pool ID:", id(db.engine.pool))
        print("session connection ID:", id(db.session.connection()))
        scope_id_2 = db._get_scope_id()
        assert scope_id_1 != scope_id_2
        stmt = select(Demo)
        demos = db.session.execute(stmt).scalars().all()
        print([demo.id for demo in demos])

    with app.test_request_context():
        print("engine pool ID:", id(db.engine.pool))
        print("session connection ID:", id(db.session.connection()))
        stmt = select(Demo)
        demos = db.session.execute(stmt).scalars().all()
        print([demo.id for demo in demos])


def test_sqlite3():
    """sqlite3 在内存数据库中，每个连接都是独立的，所以不同连接之间看不到对方的数据"""

    # Connection 1
    conn1 = sqlite3.connect(":memory:")
    conn1.execute("CREATE TABLE test (x INT)")
    conn1.execute("INSERT INTO test VALUES (42)")
    print(
        "Conn1 count:", conn1.execute("SELECT COUNT(*) FROM test").fetchone()[0]
    )  # → 1

    # Connection 2
    conn2 = sqlite3.connect(":memory:")
    try:
        count = conn2.execute("SELECT COUNT(*) FROM test").fetchone()[0]
        raise AssertionError(
            "Expected an OperationalError due to missing table, but got count:", count
        )
    except sqlite3.OperationalError as e:
        print("Conn2 error:", e)  # → "no such table: test"
