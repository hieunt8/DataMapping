from tkinter import END
import json
import ast
import sys

maps = set()


class JsonObject:
    def __init__(self, **kwargs):
        self._seen_objects = set()
        for key, value in kwargs.items():
            setattr(self, key, self._create_object(value))

    def _create_object(self, data):
        if id(data) in self._seen_objects:
            return data
        self._seen_objects.add(id(data))
        if isinstance(data, dict):
            return JsonObject(**data)
        elif isinstance(data, list):
            return [self._create_object(x) for x in data]
        else:
            return data

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, JsonObject):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [x.to_dict() if isinstance(x, JsonObject) else x for x in value]
            else:
                result[key] = value
        return result


def json_to_objects(file_import):
    class_name = file_import[0].strip()
    with open(file_import[1].strip()) as f:
        data = json.load(f)

    obj = JsonObject(**data)
    globals()[class_name] = obj

    for key, value in data.items():
        if isinstance(value, dict):
            setattr(obj, key, JsonObject(**value))
        elif isinstance(value, list):
            setattr(obj, key, [JsonObject(**x) if isinstance(x, dict) else x for x in value])

    return obj


def objects_to_json(obj):
    if isinstance(obj, JsonObject):
        return json.dumps(obj.to_dict(), indent=2)
    elif isinstance(obj, list):
        return [json.dumps(x.to_dict(), indent=2) if isinstance(x, JsonObject) else x for x in obj]
    else:
        return obj


def execute_logic(input_str):
    exec(input_str, globals())


def get_value(var_name):
    data = eval(f'objects_to_json({var_name})')
    return data


def action(in_data, out_data):
    out_data.delete('1.0', END)
    INPUT = in_data.get("1.0", "end")
    print(repr(INPUT))
    out_data.insert(END, "Hê Lô tình yêu")
    inputs = [string for string in INPUT.split("\n") if string.strip()]

    for txt in inputs:
        try:
            if '.json' in txt:
                json_to_objects(txt.split("="))
                out_data.insert(END, "\n" + "Import File: " + txt)
            elif "=" in txt and "map:" not in txt:
                execute_logic(txt)
                out_data.insert(END, "\n" + "Executed: " + txt)
            elif "map:" in txt:
                maps.add(txt.split("map:")[1].strip())
                out_data.insert(END, "\n" + "Add " + txt)
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
                out_data.insert(END, "\n" + "Value of " + nameOfVar + ": \n" + str(get_value(nameOfVar)))
            else:
                out_data.insert(END, "\n" + "Not valid Input: " + txt)
        except Exception as e:
            out_data.insert(END, "\nError: " + str(e))
            raise e
