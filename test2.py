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
            setattr(obj, key, JsonObject(**value))
        elif isinstance(value, list):
            setattr(obj, key, [JsonObject(**x) if isinstance(x, dict) else x for x in value])

    return obj