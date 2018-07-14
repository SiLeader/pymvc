PyMVC
================

&copy; 2018 SiLeader and Cerussite.

## Overview
PyMVC is MVC-like server side framework for python.
This framework is using Flask.

## How to
### How to Install
```shell
pip install pymvc
```

### How to Use
```python
import pymvc


# setting: ex1
pymvc.settings.database.database = "pymmvc_example"


# router: ex1. Add route by method
class TopController(pymvc.Controller):
    VIEW = "top.html"

    def get(self, **kwargs):
        pass


pymvc.add_route("/", TopController)


# router: ex2. Add route by decorator
@pymvc.route("/users/<id>")
class UserController(pymvc.Controller):
    VIEW = "user.html"

    def get(self, id):
        return pymvc.render(id=id)


# model: ex1. User manager model
class User(pymvc.Model):
    name = pymvc.StringType()
    id = pymvc.UniqueIdType(primary=True)


if __name__ == '__main__':
    pymvc.app.run()
```

`pymvc.app` is Flask instance.

1. set database name. (use `pymvc.settings.database.database` property)
1. create classes
    + Controller class
    + Model class
1. register controller classes to router.
1. start app
    + call `run()` method.
    + use `pymvc.app` as WSGI app.


### Controller
Controller class has `VIEW` (class variable) and `get`, `post`, `put` and `delete` instance methods.
if you want to support GET method, override `get` method.
these functions' default operation is `return abort(405)`.

### Model
Model class is ORM for MongoDB (using pymongo).
if inherit it, it creates collection.

collection's data is specified as class variable.

```python
import pymvc


class Other1(pymvc.Model):
    pass


class ModelExample(pymvc.Model):
    string_data = pymvc.StringType()  # string
    int_data = pymvc.IntType()  # integer
    float_data = pymvc.FloatType()  # float
    unique_data = pymvc.UniqueIdType()  # UUID
    foreign_data1 = pymvc.ForeignType(Other1)  # other collection
    foreign_data2 = pymvc.ForeignType("Other2")  # other collection


class Other2(pymvc.Model):
    pass

```

collection name is snake case of class name. (e.g. User: user, UserInfo: user_info)

#### Model data type
model data types' constructor parameters are `primary` and `default`.

if `primary` is `True`, this value is marked as primary key.
`default` is default value.

### View
PyMVC add some Jinja2 function.

| function | operation |
|:--------:|:----------|
| load_one(model, primary=None, **query) | load one data (using find_one) |
| load_many(model, primary=None, **query) | load all data match query and primary data |

`model` is require parameter.
`primary` is primary key value.
key value hint is `**query`.

## Dependencies
+ Flask
+ PyMongo
+ MongoDB

## License
Apache License 2.0
