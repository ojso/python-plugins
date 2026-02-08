============
sqlalchemy
============

.. code-block:: python

   from python_plugins.sqla import db
   from python_plugins.sqla.mixins import PrimaryKeyMixin
   from python_plugins.sqla.mixins import DataMixin
   from python_plugins.sqla.mixins import TimestampMixin

   class MyModel(db.Model,PrimaryKeyMixin, DataMixin, TimestampMixin):
      __tablename__ = "my_model"