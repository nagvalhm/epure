Epure
=====

<a href="https://github.com/nagvalhm/epure">Epure</a> is agnostic ORM - you can store and retrieve data having no idea about database, table and columns. 
All technical details hidden from you. Care only about your business logic.


Installing
----------

Install and update using <a href="https://pip.pypa.io/en/stable/getting-started/">`pip`</a>:

```
    $ pip install -U epure
```

Install and update using <a href="https://python-poetry.org/docs/">`poetry`</a>:

```
    $ poetry add epure
```


Connecting Epure to database
----------

Create example class with Epure, create instance of it and read it from DB.

```python

    # import connection functions from Epure
    from epure.resource.gres.gres_db import GresDb
    from epure.epure import connect

    # First way to connect database to epure

    # Format of string to connect ('database://user:password@host:port')
    connect(GresDb('postgres://postgres:postgres@localhost:5432',
    log_level=3))

    # Alternative way of connection

    db = GresDb('postgres://postgres:postgres@localhost:32', 
    # host="localhost", 
    port="5432", 
    # database="postgres", 
    # user="postgres", 
    password="postgres",
    log_level=3)
    connect(db)

    # log_level defines level of description of opertaions with DB in auto-generated file epure_db.log

```


A Simple Example
----------------

```python

    # save this as epure_example.py
    from epure.epure import epure

    # different types hints avalible
    import types

    # In order to save attributes of class to db, type hints is required!

    # decorate class by @epure() wrap function
    @epure()
    class Example:

        int_attr:int
        bool_attr:bool
        str_attr:str
        complex_attr:complex
        list_attr:list
        dict_attr:Dict[int, str]
        str_attr_with_default_val:str = 'example_str'
        epure_cls_attr:SomeEpureCls
        NoneType_attr:types.NoneType

    # creating instance of epurized Example class
    obj = Example()
    
    # assigning vals to instance
    obj.int_attr = 1
    obj.str_attr = "example"
    obj.list_attr = [1,2,3,4]

    #saving obj instance to database
    epure.save()

    # saved instance has attribute of node_id that is unique
    node_id = epure.node_id 
    
    # node_id is used to search epure objects and retrive them from DB via read() method
    res = epure.table.read(node_id=node_id)

```

Developers
-----
Nikita Umarov (Pichugin), 
Pavel Pichugin


Links
-----

-   Documentation: https://github.com/nagvalhm/epure/blob/main/README.md
-   Changes: https://github.com/nagvalhm/epure
-   PyPI Releases: https://pypi.org/project/epure/
-   Source Code: https://github.com/nagvalhm/epure
-   Issue Tracker: https://github.com/nagvalhm/epure/issues
-   Website: https://pypi.org/project/epure/