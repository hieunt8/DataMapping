from tkinter import END


def execute_logic(input_string):
    try:
        exec(input_string, globals())
        if '=' in input_string:
            variable_name = input_string.split('=')[0].strip()
            return globals()[variable_name]
    except SyntaxError:
        raise SyntaxError('Invalid syntax in input: {}'.format(input_string))
    except NameError:
        raise NameError('Undefined variable in input: {}'.format(input_string))
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
            if '.' in txt:
                a = 1
                #do get file
            elif "=" in txt:
                execute_logic(txt)
                OUT.insert(END,  "\n" + "Insert " + txt)
            elif "print" in txt:
                nameOfVar= txt.split("(")[1].split(")")[0]
                OUT.insert(END, "\n" + "Value of " + nameOfVar + " " + str(printFunc(nameOfVar)))
            else:
                OUT.insert(END, "\n" + "Not valid Input: " + txt)
        except Exception as e:
            OUT.insert(END, "\nError " + txt + ": " + str(e))