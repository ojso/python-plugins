============
ospath
============

.. code-block:: python

    from python_plugins.ospath.walk import remove_pycache
    from python_plugins.ospath.walk import remove_ipynb_checkpoints
    from python_plugins.ospath.walk import find_empty_dirs


    remove_pycache()   # default is "."
    remove_pycache("./tests")
    remove_ipynb_checkpoints()  # default is "."
    find_empty_dirs()  # default is "."

    