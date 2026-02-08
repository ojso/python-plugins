from sqlalchemy.schema import CreateTable
from sqlalchemy import create_mock_engine
from python_plugins.sqla.models.demo import Demo


def mock_engine_for_dialect(dialect_name: str):
    if dialect_name == "postgresql":
        url = "postgresql:///"
    elif dialect_name == "sqlite":
        url = "sqlite:///"
    elif dialect_name == "mysql":
        url = "mysql:///"
    else:
        raise ValueError("Unsupported dialect")

    def dump(sql, *multiparams, **params):
        print(sql.compile(dialect=engine.dialect))

    engine = create_mock_engine(url, dump)
    return engine


class TestCreateTableSQL:
    def test_create_table_sql(self):
        s = CreateTable(Demo.__table__)
        # print(type(s))
        # print(s)
        assert "CREATE TABLE demo" in str(s)
    
    def test_create_table_sql_dialects(self):
        engine = mock_engine_for_dialect("sqlite")
        s = CreateTable(Demo.__table__).compile(engine)
        assert "CREATE TABLE demo" in str(s)

        # engine = mock_engine_for_dialect("postgresql")
        # db.create_all(bind=engine, checkfirst=False)
