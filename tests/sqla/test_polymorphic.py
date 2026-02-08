from sqlalchemy import inspect
from python_plugins.sqla.orm import select
from python_plugins.sqla.models.polymorphic import Employee, Manager, Engineer
from . import db


def test_run():
    for M in (Employee, Manager, Engineer):
        mapper = inspect(M)
        assert mapper.polymorphic_on.name == "type"
        assert mapper.class_.__tablename__ == "employee"
        assert mapper.local_table.name == "employee"

    with db.Session() as session:
        db.create_all()
        session.add_all(
            [
                Manager(
                    name="Mr. Krabs",
                    manager_name="Eugene H. Krabs",
                ),
                Engineer(name="SpongeBob", engineer_info="Krabby Patty Master"),
                Engineer(
                    name="Squidward",
                    engineer_info="Senior Customer Engagement Engineer",
                ),
            ]
        )
        session.commit()
        stmt = select(Engineer)
        # print(stmt)
        assert "where employee.type" in str(stmt).lower()
        engineers = session.execute(stmt).scalars()
        for e in engineers:
            # print(e.name, e.type)
            assert isinstance(e, Engineer)
            assert e.type == "engineer"
