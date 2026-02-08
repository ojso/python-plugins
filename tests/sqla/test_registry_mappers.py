from . import db

def test_mappers():
    for mapper in db.Model.registry.mappers:
        print(mapper.class_.__name__, mapper.local_table)