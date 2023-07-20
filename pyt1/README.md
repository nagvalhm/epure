Epure
=====

<a href="https://github.com/nagvalhm/epure">Epure</a> is python agnostic ORM - you can store and retrieve data having no idea about database, table and columns. 
All technical details hidden from you. Care only about your business logic.

Supported databases
----------
Postgres: yes :heavy_check_mark:
Oracle: no :x:

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

```python
# import connection functions from Epure
from epure import GresDb
from epure import connect

# Classic way to connect database to epure

# Format of string to connect ('database://user:password@host:port')
GresDb('postgres://postgres:postgres@localhost:5432',
log_level=3).connect()

# Alternative way of connection

db = GresDb('postgres://postgres:postgres@localhost:32', 
# host="localhost", 
port="5432", 
# database="postgres", 
# user="postgres", 
password="postgres",
log_level=3) # log_level defines level of description of opertaions
db.connect() #  with DB written in auto-generated file epure_db.log

```


A Simple Example
----------------
<font color="red">In order to save attributes of class to db, type hints is required!</font>
Create example class with Epure, create instance of it and read it from DB.
```python
# save this as epure_example.py
# --------------------------------
# import epure class decorator
from epure import epure
# different types hints avalible
import types
from typing import List, Dict, Tuple, Callable

# In order to save attributes of class to db, type hints is required!

# decorate class by @epure() wrap function
@epure()
class Example:
    int_attr:int 
    bool_attr:bool
    float_attr:float
    str_attr:str
    range_attr:range
    complex_attr:complex
    list_attr:list
    generic_list_attr:List[int]
    dict_attr:Dict[int, str]
    str_attr_with_default_val:str = 'example_str' # with default val 'example_str'
    epure_cls_attr:SomeEpureCls # field that contains another epure class
    NoneType_attr:types.NoneType

# creating instance of epurized Example class
obj = Example()

# assigning vals to instance
obj.int_attr = 1
obj.str_attr = "example"
obj.list_attr = [1,2,3,4]

# saving obj instance to database
obj.save()

# saved instance has attribute of node_id that is unique
node_id = epure.node_id # -> UUID4

# node_id is used to search epure objects and retrive them from DB via read() method, returns list of list with object(s)
res = epure.table.read(node_id=node_id) # -> list[list[epure_object]]
```

Read from table method variations
----------------
#### 1. Read by kwargs:
Use keyword arguments to select records with specified fields
```python 
# node_id is UUID type id used to search epure objects and 
# retrive them from DB via read() method, returns list of list with object(s)
res = epure.table.read(node_id=node_id) # -> list[list[epure_object]]

# find objects with several keyword args
res = epure.table.read(int3=6, str3="str3_value") # -> list[list[epure_object(s)]]
```
#### 2. Read by lambda function:
Use python lambda function to select records with certain conditions and to use joins 
```python
# tp is table proxy of Example table cls, dbp is database proxy of all tables
# when lambda is used tp and dbp will be assumed as table proxy and db proxy of Example class
res = Example.resource.read(lambda tp, dbp: 
    [tp.float_attr, tp.range_attr, tp.epure_cls_attr, dbp['example'].node_id,
    
    dbp['example'] << (tp.epure_cls_attr == dbp['example'].node_id # "<<" is a join operator
    | tp.generic_list0 == dbp['example'].generic_list_attr) ^

    tp.str_attr == 'str3_value' 
    & (tp.int_attr > 3 | tp.float_attr < 0.8)

    ^dbp['another_table'] << tp.epure_class1 == dbp['another_table'].node_id
    ]
) # -> list[list[epure_object]]
```
#### 3. Read by @ (at/matmul) sign:
@ (at/matmul) is used in query as header query delimeter
```python
exmpl_db_proxy = Example.resource.resource_proxy['example']
an_ex_db_proxy = Example.resource.resource_proxy['another_table']

#Example A
Example.resource.read(exmpl_db_proxy @ int_attr > 12) # -> list[list[epure_objects]]

#Example B
#   exmpl_db_proxy.str_attr is a query header
Example.resource.read(exmpl_db_proxy.str_attr @ exmpl_db_proxy.str_attr == an_ex_db_proxy.str2 | exmpl_db_proxy.int1 == an_ex_db_proxy.int0 % 3 & 5 == an_ex_db_proxy.int3 | (an_ex_db_proxy.int2 > an_ex_db_proxy.int7)) # -> list[list[epure_objects]]
```
#### 4. Read by sql query:
```python
#   use your query to select epure obj from db
Example.resource.read('select * from example where int = 42') # -> list[list[epure_objects]]
```

Avalible operators in query
----------------
#### 1. equals "=="
```python
Example.resource.read(int_attr == 12)
```
#### 2. and "&"
```python
Example.resource.read(int_attr == 12 & str_attr == "cute doge")
```
#### 3. or "|"
```python
Example.resource.read(int_attr == 12 | str_attr == "cute doge")
```
#### 4. more ">" / less "<" 
```python
Example.resource.read(int_attr > 12 | float_attr < 8.31)
```
#### 5. in: gte(greater than or equals) ">=" /lte(less than or equals) "<="
##### Gte and Lte operators are used as "in" sql operator in cases when operands are:
##### One of operands is table proxy and other is a tuple or an subquery:
```python
# tuple
Example.resource.read(int_attr >= (12, 24)) # int_attr in (12, 24)

# subquery
Example.resource.read(int_attr >= (exmpl_db_proxy @ int_attr > 2)) # int_attr in subquery
```
##### In any other case >= operator functions as normal gte operator, like for int:
```python
# tuple
Example.resource.read(int_attr >= 12) # int_attr more or equals 12 
```
#### 6. like "%" (modulo)
##### % operator is used as "like" sql operator in cases when operands are:
##### If left operand is a table proxy and right op is a string
```python
Example.resource.read(exmpl_db_proxy.string_attr % '%a%') # this % will be treated as 'like' op
```
##### in any other case % will be treated like regular modulo
```python
Example.resource.read(exmpl_db_proxy.int_attr % 3) # this % will be treated as regular modulo
```
#### 7. not "!=" (ne) (in development)
```python
```
#### 8. join << / >> (bit shift) (in development)
```python
Example.resource.read(another_table_proxy << x. == y.f4 ^ x.f1 == y.f2 & 5 == x.f5 | x.f6 == y.f7)
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