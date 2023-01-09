# MyHy

Create novel Scheme-like DSL(isp)s using Python.

It has nothing to do with the MyPy or Hy projects.

## Usage

The `Lisp` class is the entry point for creating DSLs. It provides an API for creating Lisp-y constructs.

### Hello, World

A Python file is the "source code" for your DSL.

```python
# my_lisp.py
from myhy import Lisp

dsl = Lisp()  # an instance of Lisp() contains your entire 'language'


@dsl.function # decorated Python functions become part of the DSL
def hello():
    return "Hello, MyHy!"
```

Use the `myhy` executable to use the language.

Provide the path to your DSL (`my_lisp:dsl`) and some code:

```shell
myhy my_lisp:dsl -c "(hello)"
```

Functions registered in `myhy` can take arguments.

```python
@dsl.function
def hello(addressee):
    return f"Hello, {addressee}!"
```

```shell
myhy my_lisp:dsl -c "(hello you)"
```
