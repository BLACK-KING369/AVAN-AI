import re


def calculate(expression):

    try:
        expression = expression.replace("multiply", "")
        expression = expression.replace("x", "*")
        expression = expression.replace("×", "*")

        result = eval(expression.strip())

        return f"The answer is {result} Boss."

    except:
        return None