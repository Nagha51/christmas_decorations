**WIP - Everything's fine**
------------
Main Goal:
---

Create a decorator restricting access to method based on boolean operation against list of strings

```python
from s_class import S # Working ?
from deco import access_require # Not yet implem


"""
    Symbol table
    &:  logical and
    |:  logical or
"""

@access_require((S("tokenscope1") & S("tokenscope2")) | S("admin"),
                scopes=["tokenscope1","tokenscope2"])
def superfunction():
    return "Wow you managed to get here ! Now time to return..."


@access_require((S(["tokenscope1","tokenscope2"])) | S("admin"),
                scopes=["tokenscope1","tokenscope2"])
def superfunction2():
    """ Default for a list would be 'and' """
    return "Wow you managed to get here ! Now time to return..."


@access_require((S(["tokenscope1","tokenscope2"], any=True)) | S("admin"),
                scopes=["tokenscope1","tokenscope2"])
def superfunction3():
    """ Accept "any" as keyword to replace default 'and' with 'or' """
    return "Wow you managed to get here ! Now time to return..."



```

WIP: class `S()` seems to work properly, and is way more clearer with nested function

TODO: 🔥🍕 or improve injection of token_scopes to `access_require`


To study:
----
Django ORM using query.filter management with `S()`

    Tree generation ? ...

Another way to input required scopes

    Env variable of proxy variable.attribute to get() ?
        g.scopes ?
    Inject config object... hopefully not each time using a decorator class ?

Interesting precedence of `lambda` vs `for` [on stack](https://stackoverflow.com/questions/6076270/python-lambda-function-in-list-comprehensions)
