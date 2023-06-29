import ast


def check_input_type(input_str):
    """
    Determines the type of the input string and returns a string indicating the type.
    """
    try:
        # First, try parsing the input string as an expression
        parsed = ast.parse(input_str, mode='eval')
        if isinstance(parsed, ast.Expression):
            return "expression"
    except SyntaxError:
        pass

    # If parsing as an expression fails, try parsing as a statement
    try:
        parsed = ast.parse(input_str, mode='exec')
        if isinstance(parsed, ast.Module):
            if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
                return "value"
            elif len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Assign):
                if isinstance(parsed.body[0].targets[0], ast.Name):
                    return "variable"
            elif len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
                if isinstance(parsed.body[0].value, ast.Name) and isinstance(parsed.body[0].value.ctx, ast.Load):
                    if parsed.body[0].value.id in globals():
                        return "global variable"
                    else:
                        return "variable"
            else:
                return "invalid"
    except SyntaxError:
        pass

    # If parsing as a statement fails, assume it's a string
    return "string"

x = 42

print(check_input_type("1 + 2"))  # expression
print(check_input_type("hello"))  # variable
print(check_input_type("x"))  # global variable
print(check_input_type("foo + bar"))  # invalid
print(check_input_type("'hello'"))  # value
print(check_input_type("print('hello')"))  # invalid
print(check_input_type("not_a_valid_expression"))  # string