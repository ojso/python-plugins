from python_plugins.sqla.orm import select
from python_plugins.sqla.orm import selectinload
from python_plugins.sqla.models.tree_node import TreeNode
from . import db


def test_create_table():
    with db.Session() as session:
        db.create_all()
        tn1 = TreeNode(data="root")
        tn2 = TreeNode(data="child1", parent=tn1)
        tn3 = TreeNode(data="child2", parent=tn1)
        session.add_all(
            [
                tn1,
                tn2,
                tn3,
            ]
        )
        session.commit()
        stmt = select(TreeNode).options(selectinload(TreeNode.children))
        print(stmt)
        tns = session.execute(stmt).scalars()
        for tn in tns:
            assert isinstance(tn, TreeNode)
            print(tn.data, tn.children)
