from python_plugins.sqla import db
from python_plugins.sqla.models.demo import Demo,Address,Tag


if db.Session is None:
    # db.init_session(echo=True)
    db.init_session()
    db.create_all()
    