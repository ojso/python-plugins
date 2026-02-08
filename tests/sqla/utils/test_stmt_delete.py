from python_plugins.sqla.orm import delete
from python_plugins.sqla.utils import select_pk_values
from python_plugins.sqla.utils import delete_by_pk_ids
from python_plugins.sqla.models.multpk import Singlepk
from python_plugins.sqla.models.multpk import Multpk
from .. import db

def test_normal():
    with db.Session() as session:
        m1 = Singlepk(id=1, data="first")
        m2 = Singlepk(id=2, data="second")
        m3 = Singlepk(id=3, data="third")
        m4 = Singlepk(id=4, data="fourth")
        session.add(m1)
        session.add(m2)
        session.add(m3)
        session.add(m4)
        session.commit()

        # select pk values
        stmt = select_pk_values(Singlepk)
        # print(stmt)
        rows = session.execute(stmt).all()
        pk_values = [row[0] for row in rows]
        assert pk_values == [1, 2, 3, 4]

        # delete by pk ids
        ids = [1, 2, 3]
        stmt = delete_by_pk_ids(Singlepk, ids)
        # print(stmt)
        result = session.execute(stmt)
        session.commit()
        # print(result.rowcount)
        assert result.rowcount == 3

        # verify remaining
        stmt = select_pk_values(Singlepk)
        rows = session.execute(stmt).all()
        remain_values = [row[0] for row in rows]
        assert len(remain_values) == 1
        assert remain_values == [4]


def test_multiple_pk():

    with db.Session() as session:
        stmt = delete(Multpk)
        session.execute(stmt)
        session.commit()

    with db.Session() as session:
        m1 = Multpk(id=1, id2=1, data="first")
        m2 = Multpk(id=1, id2=2, data="second")
        m3 = Multpk(id=2, id2=1, data="third")
        m4 = Multpk(id=2, id2=2, data="fourth")
        session.add(m1)
        session.add(m2)
        session.add(m3)
        session.add(m4)
        session.commit()

        # select pk values
        stmt = select_pk_values(Multpk)
        # print(stmt)
        rows = session.execute(stmt).all()
        pk_values = [tuple(row) for row in rows]
        assert pk_values == [(1, 1), (1, 2), (2, 1), (2, 2)]

        # delete by pk ids
        ids = [(1, 1), (1, 2)]
        stmt = delete_by_pk_ids(Multpk, ids)
        # print(stmt)
        # print(stmt.compile(db.engine, compile_kwargs={"literal_binds": True}))
        result = session.execute(stmt)
        session.commit()
        # print(result.rowcount)
        assert result.rowcount == 2

        # verify remaining
        stmt = select_pk_values(Multpk)
        rows = session.execute(stmt).all()
        remain_values = [tuple(row) for row in rows]
        assert len(remain_values) == 2
        assert remain_values == [(2, 1), (2, 2)]
