from typing import Optional, List
from datetime import datetime
from datetime import date
from datetime import time
import enum

from .. import db
from ..orm import Integer
from ..orm import Boolean
from ..orm import String
from ..orm import Float
from ..orm import DateTime
from ..orm import Date
from ..orm import Time
from ..orm import LargeBinary
from ..orm import Enum
from ..orm import JSON
from ..orm import Mapped
from ..orm import mapped_column
from ..orm import relationship
from ..orm import composite
from ..orm import synonym
from ..orm import Table
from ..orm import Column
from ..orm import ForeignKey
from ..orm import hybrid_property
from ..orm import hybrid_method
from ..orm import association_proxy
from ..orm import AssociationProxy

# see https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html

class Point:
    x: int
    y: int


# Status = Literal["pending", "received", "completed"]
class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"


class Demo(db.Model):
    __tablename__ = "demo"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    data: Mapped[dict] = mapped_column(JSON)
    bool_field: Mapped[bool] = mapped_column(Boolean, nullable=True)
    date_field: Mapped[date] = mapped_column(Date, nullable=True)
    time_field: Mapped[time] = mapped_column(Time, nullable=True)
    datetime_field: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    x: Mapped[int]
    y: Mapped[int]
    start: Mapped[int]
    end: Mapped[int]
    status: Mapped[Status]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    point: Mapped[Point] = composite("x", "y")

    syn_status = synonym("status")

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @hybrid_method
    def contains(self, point: int) -> bool:
        return (self.start <= point) & (point <= self.end)

    tg: Mapped[List["Tag"]] = relationship(secondary=lambda: demo_tag_table)
    # proxy the 'keyword' attribute from the 'kw' relationship
    tags: AssociationProxy[List[str]] = association_proxy("tg", "tag")

    addresses: Mapped[List["Address"]] = relationship(back_populates="demo")

    def __init__(self, name: str):
        self.name = name


class Address(db.Model):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str]
    demo_id = mapped_column(ForeignKey("demo.id"))
    demo: Mapped["Demo"] = relationship(back_populates="addresses")


class Tag(db.Model):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str]

    def __init__(self, tag: str):
        self.tag = tag

    def __repr__(self) -> str:
        return f"Tag({self.tag!r})"


demo_tag_table = Table(
    "demo_tag",
    db.Model.metadata,
    Column("demo_id", ForeignKey("demo.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
