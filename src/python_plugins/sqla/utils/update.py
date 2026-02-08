def update_obj(session, Model, obj, data: dict):
    """insert or update object

    :param session: sqlalchemy session
    :param Model: object Model
    :param obj: object of Model
    :param data: data dict
    """

    if obj is None:
        new_obj = Model()
        for k in data:
            if hasattr(new_obj, k):
                setattr(new_obj, k, data.get(k))
        session.add(new_obj)
        session.commit()
        print(f"{new_obj} inserted")
    else:
        for k in data:
            if hasattr(obj, k):
                setattr(obj, k, data.get(k))
        session.commit()
        print(f"{obj} updated")
