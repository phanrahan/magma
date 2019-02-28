__all__  = ['get_current_definition']
__all__ += ['push_definition']
__all__ += ['pop_definition']


# Maintain a current definition and stack for nested definitions.
current_definition = None
current_definition_stack = []


def get_current_definition():
    global current_definition
    return current_definition


def push_definition(defn):
    global current_definition
    if current_definition:
        current_definition_stack.append(current_definition)
    current_definition = defn


def pop_definition():
    global current_definition
    if len(current_definition_stack) > 0:
        current_definition = current_definition_stack.pop()
    else:
        current_definition = None




