from tkinter import END
import json
import ast
import sys

maps = set()


class JsonObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = JsonObject(**value)
            elif isinstance(value, list):
                value = [JsonObject(**x) if isinstance(x, dict) else x for x in value]
            setattr(self, key, value)


def json_to_objects(file_import):
    class_name = file_import[0].strip()
    with open(file_import[1].strip()) as f:
        data = json.load(f)

    obj_class = type(class_name, (JsonObject,), {})
    obj = obj_class(**data)

    globals()[class_name] = obj

    for key, value in data.items():
        if isinstance(value, dict):
            sub_class_name = key.capitalize()
            sub_obj_class = type(sub_class_name, (JsonObject,), {})
            setattr(obj, key, sub_obj_class(**value))
        elif isinstance(value, list):
            sub_objs = []
            for x in value:
                if isinstance(x, dict):
                    sub_class_name = key.capitalize()
                    sub_obj_class = type(sub_class_name, (JsonObject,), {})
                    sub_objs.append(sub_obj_class(**x))
                else:
                    sub_objs.append(x)
            setattr(obj, key, sub_objs)

    return obj


def execute_logic(input_str):
    """
    Verifies the input string and executes it using `eval` or `exec` if it is safe.
    Raises a ValueError if the input string contains any unsafe code.
    """
    # Whitelist of safe functions and modules
    safe_list = ['math', 'sin', 'cos', 'tan']

    # Parse the input string as an abstract syntax tree (AST)
    parsed = ast.parse(input_str, mode='exec')

    # Check if the AST contains any unsafe nodes
    for node in ast.walk(parsed):
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in safe_list:
                raise ValueError(f"Unsafe function call: {ast.dump(node)}")
        elif isinstance(node, ast.Attribute):
            if not isinstance(node.value, ast.Name) or node.value.id not in safe_list:
                raise ValueError(f"Unsafe attribute access: {ast.dump(node)}")

    try:
        # If the input string is safe, execute it using `eval` or `exec`
        # If the input string is safe, execute it using `eval` or `exec`
        exec(input_str, globals())
    except SyntaxError:
        raise SyntaxError('Invalid syntax in input: {}'.format(input_str))
    except NameError:
        raise NameError('Undefined variable in input: {}'.format(input_str))
    return None


def printFunc(var_name):
    if var_name in globals():
        return globals()[var_name]
    else:
        return "Not Found"


def Action(IN, OUT):
    OUT.delete('1.0', END)
    INPUT = IN.get("1.0", "end")
    print(repr(INPUT))
    OUT.insert(END, "Hê Lô tình yêu")
    inputs = [string for string in INPUT.split("\n") if string.strip()]

    for txt in inputs:
        try:
            if '.' in txt and "print" not in txt:
                json_to_objects(txt.split("="))
                OUT.insert(END, "\n" + "Import File: " + txt)
            elif "=" in txt and "map:" not in txt:
                execute_logic(txt)
                OUT.insert(END, "\n" + "Executed: " + txt)
            elif "map:" in txt:
                maps.add(txt.split("map:")[1].strip())
                OUT.insert(END, "\n" + "Add " + txt)
            elif "print" in txt:
                temp = ''
                try:
                    for map in maps:
                        temp = map
                        execute_logic(map)
                except Exception as e:
                    maps.remove(temp)
                    raise Exception(str(e) + "\nRemoved mapping: {}".format(temp))
                nameOfVar = txt.split("(")[1].split(")")[0]
                OUT.insert(END, "\n" + "Value of " + nameOfVar + ": " + str(printFunc(nameOfVar)))
            else:
                OUT.insert(END, "\n" + "Not valid Input: " + txt)
        except Exception as e:
            OUT.insert(END, "\nError: " + str(e))
            raise e
