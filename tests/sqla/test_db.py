import pytest
import sqlite3
from datetime import datetime
from python_plugins.sqla.orm import Mapped
from python_plugins.sqla.orm import mapped_column
from . import db
from .models.simple import Simple




def test_db():
    assert getattr(db, "Model", None) is not None
    assert getattr(db, "engine", None) is not None
    assert getattr(db, "session", None) is not None

    db.create_all()
    simple_1 = Simple(name="simple1")
    with db.session() as session:
        session.add(simple_1)
        session.commit()
        s1 = session.get(Simple, 1)
        assert s1 is not None
        assert s1.name == "simple1"


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
