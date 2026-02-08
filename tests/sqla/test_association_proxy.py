from python_plugins.sqla.orm import select
from python_plugins.sqla.orm import selectinload
from python_plugins.sqla.models.association_proxy import AssociationProxyParent
from python_plugins.sqla.models.association_proxy import AssociationProxyChild
from . import db


def test_run():
    with db.Session() as session:
        c1 = AssociationProxyChild(name="Python")
        c2 = AssociationProxyChild(name="SQLAlchemy")
        c3 = AssociationProxyChild(name="Flask")
        p1 = AssociationProxyParent(name="alice")
        p2 = AssociationProxyParent(name="bob")
        session.add_all(
            [
                c1,
                c2,
                p1,
                p2,
            ]
        )
        p1.children.append(c1)
        p1.children.append(c2)
        p2.children.append(c3)
        session.commit()
        stmt = select(AssociationProxyParent).options(selectinload(AssociationProxyParent.children))
        print(stmt)
        proxy_parents = session.execute(stmt).scalars()
        for p in proxy_parents:
            assert isinstance(p, AssociationProxyParent)
            # print(u.name, u.kw)
            print(p.name, p.childrennames)
