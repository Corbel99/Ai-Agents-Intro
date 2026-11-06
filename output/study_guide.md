**Explanation**

Python decorators are a powerful feature that allows you to modify or extend the behavior of a function without changing its implementation. A decorator is a small function that takes another function as an argument and returns a new function that "wraps" the original function. This allows you to add additional functionality to an existing function without altering its source code.

Think of decorators like a wrapper around a present. You can decorate a function with a decorator, and the decorator will "wrap" the function, adding its own functionality without changing the original function.

**Key Concepts**

* **Decorators**: Small functions that modify or extend the behavior of another function.
* **Wrapping**: The process of adding additional functionality to an existing function without changing its source code.
* **Arguments**: Decorators can take arguments, which are passed to the decorator when it's applied to a function.
* **Return values**: Decorators can return values, which are used to modify the original function's behavior.
* **@symbol**: The `@` symbol is used to apply a decorator to a function.
* **Function annotations**: Decorators can use function annotations to modify the behavior of a function.

**Example**

Here's a simple example of a decorator that logs the execution time of a function:
```python
import time
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@log_execution_time
def add_numbers(a, b):
    time.sleep(1)  # Simulate some work
    return a + b

result = add_numbers(2, 3)
print(result)  # Output: 5
```
In this example, the `log_execution_time` decorator is applied to the `add_numbers` function. When `add_numbers` is called, the decorator measures the execution time and prints it to the console. The `wraps` function is used to preserve the original function's name and docstring.