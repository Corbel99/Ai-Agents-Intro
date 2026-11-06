## Topic
Python Decorators
=====================

## Simple Explanation
--------------------

Python decorators are a powerful feature in Python that allows you to modify or extend the behavior of a function or class without changing its source code. In essence, a decorator is a small function that takes another function as an argument and returns a new function that "wraps" the original function. This allows you to wrap the original function with additional functionality without modifying its original code.

Think of decorators like a layer of frosting on a cake. The original function is like the cake, and the decorator is like the frosting. You can add different flavors or decorations to the frosting without changing the cake itself.

## Key Concepts
--------------

*   **Decorators as functions**: A decorator is a small function that takes another function as an argument.
*   **Decorators as classes**: In Python 3.8 and later, you can also use classes as decorators.
*   **@symbol**: The `@` symbol is used to denote a decorator. It is usually followed by the name of the decorator function or class.
*   **Function arguments**: Decorators can take arguments, just like regular functions.
*   **Return values**: Decorators should return a function or other callable object.

## Example
---------

Here's an example of a simple decorator that prints a message before and after the execution of the original function:

```python
def my_decorator(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

In this example, `my_decorator` is a function that takes `func` as an argument and returns a new function `wrapper`. The `wrapper` function calls the original function `func` and prints two messages before and after the execution.

When we use the `@my_decorator` syntax before the `say_hello` function, we're essentially replacing the `say_hello` function with the `wrapper` function returned by `my_decorator`. So, when we call `say_hello()`, it's actually calling the `wrapper` function, which calls the original `say_hello` function and prints the messages.

This is a simple example, but decorators can be much more powerful and flexible, and are used extensively in Python libraries and frameworks.