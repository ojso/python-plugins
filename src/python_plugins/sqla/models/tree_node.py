from .. import db
from ..orm import ForeignKey
from ..orm import Mapped
from ..orm import mapped_column
from ..orm import relationship

# Adjacency List Relationships
# see https://docs.sqlalchemy.org/en/20/orm/self_referential.html


class TreeNode(db.Model):
    __tablename__ = "tree_node"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id = mapped_column(ForeignKey("tree_node.id"))
    data: Mapped[str]
    children = relationship("TreeNode", back_populates="parent")
    parent = relationship("TreeNode", back_populates="children", remote_side=[id])
