# Topic: Python decorators

### Simple Explanation

Python decorators are a powerful feature that allows programmers to modify or extend the behavior of a function without changing its source code. They are called "decorators" because they "decorate" the original function with additional functionality.

Think of a decorator as a wrapper that adds some extra behavior to a function, but doesn't change the function itself. You can apply multiple decorators to a single function to create a new behavior that builds upon the original one.

For example, imagine you want to add logging to a function. You could create a decorator that logs the input and output of the function, and then apply that decorator to your original function.

### Key Concepts

* **Function wrappers**: Decorators are essentially function wrappers that can modify the behavior of a function.
* **Function call**: When a decorator is applied to a function, it is essentially creating a new function that calls the original function.
* **Function arguments**: Decorators can accept arguments, which are used to customize the behavior of the decorator.
* **Return value**: Decorators can return values, which are used to modify the behavior of the decorated function.

### Example

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before calling the function")
        result = func(*args, **kwargs)
        print("After calling the function")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

print(add(2, 3))  # Output: Before calling the function, After calling the function, 5
```

In this example, the `my_decorator` decorator is applied to the `add` function. The decorator logs a message before and after calling the `add` function, and returns the result of the function call.

Note how the `@my_decorator` syntax is used to apply the decorator to the `add` function. This is just a shorthand way of saying `add = my_decorator(add)`.

## Practice Exercise
**Exercise: Logging Function Calls with a Decorator**

Create a decorator that logs the input and output of a function. The decorator should accept an argument `log_level` that specifies the level of logging (e.g. `debug`, `info`, `warning`, `error`).

Apply this decorator to a simple function that takes two arguments and returns their sum.

**Expected Input and Output**

* The input should be a function with two arguments (e.g. `int` or `float`).
* The output should be a function with the same two arguments, but with logging added.

**Expected Output**
```python
print(log_add(2, 3))  # Output: debug: Adding 2 and 3, result: 5
print(log_add(4, 5))  # Output: info: Adding 4 and 5, result: 9
print(log_add(-1, 1))  # Output: warning: Adding -1 and 1, result: 0
print(log_add(0, 0))  # Output: error: Adding 0 and 0, result: 0
```
**Hints**

* Use the `logging` module to implement the logging functionality.
* Use string formatting to include the log level and input/output values in the log messages.
* Consider using an `enum` to define the log levels and their corresponding values.

## Common Mistakes
### 1. Forgetting to import the `logging` module

Many beginners forget to import the `logging` module, which is necessary for implementing the logging functionality in the decorator. Make sure to add `import logging` at the top of your code.

### 2. Not using the correct logging level

When logging, it's essential to use the correct logging level to ensure that the log messages are displayed at the correct level. For example, if you want to log debug messages, you should use the `DEBUG` level, not `INFO`. Make sure to use the correct logging level for your use case.

### 3. Not handling exceptions

When implementing the decorator, don't forget to handle exceptions that may occur during the execution of the decorated function. This will ensure that the decorator handles errors correctly and doesn't crash the program. Consider using a `try`-`except` block to catch and handle exceptions.

## Review Comments
### Missing Information
* The explanation of the `enum` hint in the practice exercise is not provided. It would be helpful to include an example of how to use an `enum` to define the log levels and their corresponding values.

### Clearing Up Uncertainty
* The explanation of the logging levels (`debug`, `info`, `warning`, `error`) is not provided. It would be helpful to include a brief explanation of the differences between these levels and why they are used.

### Short and Specific Suggestions
* In the example code, the variable `result` could be named `function_result` to better indicate its purpose.
* In the practice exercise, the expected input and output could be more clearly defined. For example, the expected input could be a function with the signature `def log_add(a: int, b: int) -> int:`.

### Clarity and Consistency
* The formatting of the log messages in the practice exercise could be more consistent. For example, all log messages could use the same format, such as `"log_level: Function call with input {input} and output {output}"`.

## Final Summary
This study guide provides a clear introduction to Python decorators, including their purpose, key concepts, and a practical example. The guide also includes a practice exercise that requires readers to implement a decorator with logging functionality. The only areas for improvement are providing additional information on logging levels and handling exceptions, as well as clarifying the expected input and output of the practice exercise. Overall, the guide is well-structured and provides a solid foundation for readers to build upon.
