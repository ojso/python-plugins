from python_plugins.sqla.orm import select
from python_plugins.sqla.orm import delete
from python_plugins.sqla.models.multpk import Multpk
from . import db


def test_multpk():
    with db.Session() as session:
        db.create_all()
        stmt = delete(Multpk)
        session.execute(stmt)
        session.commit()

    mp11 = Multpk(id=1, id2=1, data="data1")
    mp12 = Multpk(id=1, id2=2, data="data2")
    mp21 = Multpk(id=2, id2=1, data="data3")
    with db.Session() as session:
        session.add_all(
            [
                mp11,
                mp12,
                mp21,
            ]
        )
        session.commit()
        stmt = select(Multpk)
        print(stmt)
        mps = session.execute(stmt).scalars()
        for mp in mps:
            assert isinstance(mp, Multpk)
            print(mp.id, mp.id2, mp.data)
