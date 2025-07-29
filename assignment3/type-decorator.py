#type-decorator

def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Function 1: returns an int, will be converted to str
@type_converter(str)
def return_int():
    return 5

# Function 2: returns a string that cannot be converted to int
@type_converter(int)
def return_string():
    return "not a number"

# main
if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  # This should print "str"

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  # This is what should happen
