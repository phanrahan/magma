from magma.t import Type


def set_name(name: str, value):
    if not isinstance(value, Type):
        # in case we run into an unexpected type of value, for now we just
        # ignore it and don't give it a name
        return value
    temp = type(value).undirected_t(name=name)
    temp @= value
    return temp
