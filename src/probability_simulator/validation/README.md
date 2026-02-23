# Validation Descriptors

This module contains reusable descriptors for validating attributes in the `probability_simulator` package. 


A [Descriptor](https://docs.python.org/3/howto/descriptor.html) is a python object that defines one or more of:
- `__get__`
- `__set__`
- `__delete__`

When a class attribute is defined using a Descriptor instance, we have pre-configured methods that get run whenever that attribute is then accessed or assigned. In other words, they control how *external code* deals with our attributes


## Overview

Consider the below snippet:

```python
class Coin:
    bias = RealNumber()

    def __init__(self, bias):
        self.bias = bias
```

Here, 
- `self.bias = RealNumber()` creates a class-level descriptor
- `self.bias = bias` calls the `RealNumber.__set__()` method
- Validation happens automatically on assignment

The actual numeric value is stored in `Coin`'s `__dict__`, but all validation logic lives in the descriptor 

## Why use a descriptor?

Descriptors allow us to:
- Enforce validation when attributes are assigned
- Keep validation logic away from the main simulation classes 
- Avoid repeating common validation checks 

Compared to a value object, it also looks much cleaner

Instead of: 
```python
coin.bias = RealNumberObj(0.5)
coin.bias = RealNumberObj(0.6)
```

We can write
```python
coin.bias = 0.5   # validated automatically
coin.bias = 0.6
```

# Validator Descriptors Defined

The module is structured around a small hierarchy of reusable descriptor classes.

```
validation/
├── __init__.py
├── fields.py        # descriptor implementations
└── README.md
```

Core Concepts:
1. `Field` is the Base Descriptor which handles
    - Type Checking
    - `None` handling
2. Specialised Descriptors, built on top of `Field`. For example:
    - `RealNumber`
    - `RealNumberInRange(min, max)`
    - `IntegerInRange(min, max)` 
    - `FunctionWithParams({...})`
    - ...

Useful implementations
1. `Interval` - which deals with string-representation bounded and unbounded intervals 

Each of these `Field` objects also has a public `validate()` instance method, which runs the validation logic. This means that we can run validation in other contexts. 