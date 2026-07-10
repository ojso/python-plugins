from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class Db:
    def __init__(self):
        self.Model = Base
        self.engine = None
        self.session = None

    def init_session(
        self, url: str | None = None, echo: bool = False, **engine_options
    ) -> None:
        """Initialize the database engine and session factory in non-Flask environments.

        Examples:
            db = Db()
            db.init_session(url="sqlite:///mydb.sqlite", echo=True)
            db.create_all()

            with db.session() as session:
                session.add(obj)
                session.commit()
        """
        self._cleanup()

        options = {"url": url or "sqlite:///:memory:"}
        if echo:
            options["echo"] = True
        options.update(engine_options)

        self.engine = create_engine(**options)
        self.session = sessionmaker(bind=self.engine)

    def _cleanup(self) -> None:
        """clear old connections and sessions"""
        if self.session is not None:
            self.session = None

        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
  
    def create_all(self, **kwargs):
        if "bind" not in kwargs:
            kwargs["bind"] = self.engine
        self.Model.metadata.create_all(**kwargs)

    def reset_models(self):
        self.Model.metadata.drop_all(self.engine)
        self.Model.metadata.create_all(self.engine)
