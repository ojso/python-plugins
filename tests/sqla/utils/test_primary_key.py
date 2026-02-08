import ast
from sqlalchemy import inspect
from python_plugins.sqla.models.multpk import Singlepk
from python_plugins.sqla.models.multpk import Multpk
from .. import db


def test_single_pk():
    mapper_singlepk = inspect(Singlepk)
    # print(mapper_singlepk.primary_key)
    assert len(mapper_singlepk.primary_key) == 1

    with db.Session() as session:
        db.create_all()
        m1 = Singlepk(data="first")
        m2 = Singlepk(data="second")
        session.add(m1)
        session.add(m2)
        session.commit()

    insp = inspect(m1)
    k1 = insp.identity
    k2 = insp.identity[0]

    with db.Session() as session:
        s1 = session.get(Singlepk, k1)
        s2 = session.get(Singlepk, k2)
    assert s1 is s2


def test_multiple_pk():
    mapper_multpk = inspect(Multpk)
    # print(mapper_multpk.primary_key)
    assert len(mapper_multpk.primary_key) == 2

    with db.Session() as session:
        db.reset_models()
        m1 = Multpk(id=1, id2=1, data="first")
        m2 = Multpk(id=1, id2=2, data="second")
        session.add(m1)
        session.add(m2)
        session.commit()

    insp = inspect(m1)
    # print(insp.identity)
    k1 = insp.identity
    k2 = str(k1)

    with db.Session() as session:
        s1 = session.get(Multpk, k1)
        s2 = session.get(Multpk, ast.literal_eval(k2))

    assert s1 is s2
