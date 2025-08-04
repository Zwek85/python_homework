#log-decorator

import logging
from functools import wraps

# One-time logger setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call the function
        result = func(*args, **kwargs)

        # Format arguments
        positional = list(args) if args else "none"
        keyword = kwargs if kwargs else "none"

        # To write a log record:
        logger.info(
            f"function: {func.__name__}\n"
            f"positional parameters: {positional}\n"
            f"keyword parameters: {keyword}\n"
            f"return: {result}\n"
        )

        return result
    return wrapper

# Function 1: no parameters, no return
@logger_decorator
def greet():
    print("Hello, World!")

# Function 2: variable positional arguments
@logger_decorator
def check_args(*args):
    return True

# Function 3: variable keyword arguments, returns logger_decorator
@logger_decorator
def keyword_args_function(**kwargs):
    return logger_decorator

# main test code
if __name__ == "__main__":
    greet()
    check_args(1, 2, 3)
    keyword_args_function(a=1, b=2, c="test")
