import jsonpickle


def serialize(obj: any) -> str:
    return jsonpickle.encode(obj)


def deserialize(json_string: str) -> any:
    return jsonpickle.decode(json_string)
