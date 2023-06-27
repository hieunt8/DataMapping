import json


class JsonObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = JsonObject(**value)
            elif isinstance(value, list):
                value = [JsonObject(**x) if isinstance(x, dict) else x for x in value]
            setattr(self, key, value)


def json_to_objects(file_path):
    with open(file_path) as f:
        data = json.load(f)

    class_name = file_path.split('/')[-1].split('.')[0]
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
