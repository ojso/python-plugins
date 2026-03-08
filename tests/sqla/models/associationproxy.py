from typing import Final
from typing import List
from . import db
from . import Mapped
from . import mapped_column
from . import ForeignKey
from . import relationship
from . import Table
from . import Column
from . import Integer
from . import String
from . import association_proxy
from . import AssociationProxy


class AssociationProxyChild(db.Model):
    __tablename__ = "association_proxy_child"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))


class AssociationProxyParent(db.Model):
    __tablename__ = "association_proxy_parent"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    children: Mapped[List[AssociationProxyChild]] = relationship(
        secondary=lambda: association_proxy_parent_child_table
    )
    # proxy the 'name' attribute from the 'children' relationship
    childrennames: AssociationProxy[List[str]] = association_proxy("children", "name")


association_proxy_parent_child_table: Final[Table] = Table(
    "association_proxy_parent_child",
    db.Model.metadata,
    Column(
        "association_proxy_parent_id",
        Integer,
        ForeignKey("association_proxy_parent.id"),
        primary_key=True,
    ),
    Column(
        "association_proxy_child_id",
        Integer,
        ForeignKey("association_proxy_child.id"),
        primary_key=True,
    ),
)
