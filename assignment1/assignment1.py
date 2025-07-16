# Write your code here.
#Task1
def hello():
    return "Hello!"
print(hello())

#Task2
def greet(name):
    return f"Hello, {name}!"
print(greet("Joe"))

#Task3
def calc(a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a ** b
            case _:
                return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
#Task4
def data_type_conversion(value, type):
    try:
        match type:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case _:
                return f"Unsupported type: {type}"
    except ValueError:
        return f"You can't convert {value} into a {type}."
    
print(data_type_conversion("505", "int"))      # 123
print(data_type_conversion("2.5", "float"))   # 3.14
print(data_type_conversion(100, "str"))        # "123"
print(data_type_conversion("wrong", "float"))   # You can't convert wrong into a float.
print(data_type_conversion("211", "synt"))     # Unsupported type: synt

#Task5
def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    except:
        return "Invalid data was provided."
print(grade(100, 95, 90))   # ➞ A
print(grade(70, 65, 60))   # ➞ D
print(grade())             # ➞ "Invalid data was provided."

#Task6
def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result
print(repeat("Hey!", 3))   # ➞ "Hey!Hey!Hey!"

#Task7
def student_scores(mode, **kwargs):
    if mode == "best":
        best_student = max(kwargs, key=kwargs.get)
        return best_student
    elif mode == "mean":
        scores = kwargs.values()
        return sum(scores) / len(scores)
    else:
        return "Invalid mode"

print(student_scores("best", Joe=90, Rob=85, David=95))
print(student_scores("mean", Joe=90, Rob=85, David=95))

#Task8
def titleize(text):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = text.lower().split()  
    result = []

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1: 
            result.append(word.capitalize())
        elif word in little_words:
            result.append(word) 
        else:
            result.append(word.capitalize())
    
    return " ".join(result)
print(titleize("superman and bob")) 

#Task9
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result
print(hangman("alphabet", "above"))       

#Task10
def pig_latin(sentence):
    vowels = "aeiou"
    words = sentence.split()
    result = []

    for word in words:
        if word.startswith("qu"):
            new_word = word[2:] + "quay"
        elif word[0] in vowels:
            new_word = word + "ay"
        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                if word[i:i+2] == "qu":
                    i += 2  
                    break
                i += 1
            new_word = word[i:] + word[:i] + "ay"

        result.append(new_word)
    
    return " ".join(result)
print(pig_latin("hello")) 