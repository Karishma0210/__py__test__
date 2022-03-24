def is_attribute(Cls, attribute):
    attributes = get_attributes(Cls)
    return attribute in attributes

def get_attributes(Cls):
    attributes = []
    for key in Cls.__dict__.keys():
        if not (key.startswith('_') or callable(getattr(Cls, key))):
            attributes.append(key)
    return attributes