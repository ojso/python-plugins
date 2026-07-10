from python_plugins.sqla import db


if db.session is None:
    # db.init_session(echo=True)
    db.init_session()
    db.create_all()
