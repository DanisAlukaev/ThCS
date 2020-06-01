"""
Final Exam: Part 1 (20-05-2020)
Lambda Calculus Parser.
"""

__author__ = "Danis Alukaev"
__email__ = "d.alukaev@innopolis.university"
__copyright__ = "2020, BS19-02"
__version__ = "1.1.0"


def is_letter_or_digit(token):
    """
    Determine whether received token is latin letter or digit.
    :param token: symbol to be considered.
    :return: True if token is latin letter or digit, False - otherwise.
    """
    if (token >= "a" and token <= "z" or
            token >= "A" and token <= "Z" or
            token >= "0" and token <= "9"):
        return True
    return False


def is_lambda_expression(expression):
    """
    Check whether the expression is an element of the set of lambda-terms defined by the following grammar:
        Λ ::= V | (Λ)Λ | \V.Λ
    :param expression: string to be considered.
    :return: True if the expression is either variable or function application or function.
    """
    if is_variable(expression) or is_function_application(expression) or is_function(expression):
        # if the expression is either variable V or function application (Λ)Λ or function \V.Λ
        return True
    return False


def is_variable(expression):
    '''
    Check whether received expression is a variable in lambda calculus.
    By definition variable should belong to the set of non-empty strings build from latin letters and digits.
    :param expression: string to be considered.
    :return: True if the expression is a variable, False - otherwise.
    '''
    if len(expression) == 0:
        # if expression is empty string
        return False
    for token in expression:
        # determine whether all symbols in expression are latin letters or digits
        if not is_letter_or_digit(token):
            # if symbol is not latin letter or digit
            return False
    return True


def is_function_application(expression):
    """
    Check whether received expression is a function application in lambda calculus.
    By definition function application should have the following structure: (Λ)Λ, where Λ is the lambda expression.
    :param expression: string to be considered.
    :return: True if the expression is a function application, False - otherwise.
    """
    if (len(expression) == 0) or (expression[0] != '('):
        # if expression is empty string or doesn't start with open parenthesis
        return False
    # stack to check that parenthesis are balanced
    stack = []
    # set the index of close parenthesis
    index_of_closed = -1
    for i in range(len(expression)):
        if expression[i] == '(':
            # push into stack open parenthesis
            stack.append('(')
        elif expression[i] == ')':
            # pop open parenthesis from stack
            stack.pop()
            if not stack:
                # stack is empty
                index_of_closed = i
                break
    if index_of_closed == -1:
        # if expression hasn't close parenthesis
        return False
    # operator in function application
    operator = expression[1:index_of_closed]
    # operand in function application
    operand = expression[index_of_closed + 1:]
    if is_lambda_expression(operator) and is_lambda_expression(operand):
        # if operator or operand isn't valid
        return True
    return False


def is_function(expression):
    """
    Check whether received expression is the function in lambda calculus.
    It should have the following structure: \V.Λ, where V is the variable
    and Λ is the lambda expression.
    :param expression: string to be considered.
    :return: True if expression is the function, False - otherwise.
    """
    if (len(expression) == 0) or (expression[0] != '\\') or ('.' not in expression):
        # if expression is empty string or doesn't start with a lambda or contain a point
        return False
    # identifier of an argument of the function
    argument = expression[1:expression.index('.')]
    # body of the function
    body = expression[expression.index('.')+1:]
    if is_variable(argument) and is_lambda_expression(body):
        # if identifier of an argument is a variable and
        # body of the function is an lambda calculus expression
        return True
    return False


"""
===========================================================================
                                MAIN
===========================================================================
"""
if __name__ == "__main__":
    file = open('input.txt', 'r')  # an input file
    result = open('output.txt', 'w+')  # an output file
    description = file.readlines()  # convert IO strings to the list
    if description:
        # file isn't empty
        description = description[0]
    else:
        # file is empty
        description = ""
    if is_lambda_expression(description):
        # expression is valid
        # find number of β-redexes
        redex = description.count('(\\')
        result.write("YES\n")
        print("YES")
        result.write(str(redex))
        print(redex)
    else:
        # expression isn't valid
        result.write("NO")
        print("NO")
