import pytest
from datetime import datetime
from flask import Flask
from flask import current_app
from sqlalchemy.orm import Session
from python_plugins.sqla.orm import Mapped
from python_plugins.sqla.orm import mapped_column
from python_plugins.sqla.db import Db


db = Db()


class Demo(db.Model):
    __tablename__ = "demo"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


def test_flask_db():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # app.config['SQLALCHEMY_ECHO'] = False
    assert getattr(db, "Model", None) is not None
    assert getattr(db, "engine", None) is None
    assert getattr(db, "session", None) is None

    db.init_app(app)
    assert getattr(db, "engine", None) is not None
    assert getattr(db, "session", None) is not None

    with pytest.raises(RuntimeError):
        db.session()

    with app.app_context():
        assert db is current_app.extensions["sqlalchemy"]
        first = db.session()
        assert isinstance(first, Session)
        second = db.session()
        assert first is second

    with app.app_context():
        third = db.session()
        assert first is not third

    with app.app_context():
        db.create_all()
        demo_1 = Demo(name="demo1")
        db.session.add(demo_1)
        db.session.commit()
        d1 = db.session.get(Demo, 1)
        assert d1 is not None
        assert d1.name == "demo1"
