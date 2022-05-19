from magma.common import Stack


class WhenCondStack(Stack):
    def __init__(self, defn):
        super().__init__()
        self._defn = defn

    def push(self, value):
        super().push(value)
        self._defn.add_when_cond(value)


# Contains a stack of WhenCondStacks.  Each active definition has its own when
# cond stack (allows for multiple, active nested definitions).  Each when cond
# stack contains the current active when conditions (allows for nested
# conditions)
_DEFN_STACK = Stack()

# Used to store the previous when condition for elsewhen/otherwise logic
_PREV_WHEN_COND = None


def push_when_cond_stack(stack):
    global _DEFN_STACK
    _DEFN_STACK.push(stack)


def pop_when_cond_stack():
    return _DEFN_STACK.pop()


def peek_when_cond_stack():
    return _DEFN_STACK.peek()


def reset_context():
    """
    Note, this needs to be called by tests that may raise an exception (to
    reset the global when condition state)
    """
    global _DEFN_STACK, _PREV_WHEN_COND
    _DEFN_STACK.clear()
    _PREV_WHEN_COND = None


class WhenCtx:
    def __init__(self, cond, prev_cond=None):
        self._cond = cond
        # Get the current definition when cond stack
        self.when_cond_stack = _DEFN_STACK.peek()

        self._children = []

        # If there's an active when condition, store a parent pointer
        self._parent = self.when_cond_stack.safe_peek()
        if self._parent is not None:
            # Parents have references to their children
            self.parent.add_child(self)

        # Used for reference chain to previous when/elsewhen statements
        self._prev_cond = prev_cond

        global _PREV_WHEN_COND
        # Reset activate prev cond to avoid a nested `elsewhen` or `otherwise`
        # continuing a chain
        _PREV_WHEN_COND = None

        self._is_otherwise = cond is None
        self._conditional_wires = {}

    def __enter__(self):
        self.when_cond_stack.push(self)

    def __exit__(self, exc_type, exc_value, traceback):
        self.when_cond_stack.pop()
        if not self._is_otherwise:
            # Only populate _PREV_WHEN_COND when not an otherwise (otherwise we
            # "close" the chain)
            global _PREV_WHEN_COND
            _PREV_WHEN_COND = self
        else:
            assert _PREV_WHEN_COND is None

    @property
    def parent(self):
        return self._parent

    @property
    def cond(self):
        return self._cond

    @property
    def prev_cond(self):
        return self._prev_cond

    @property
    def conditional_wires(self):
        return self._conditional_wires

    def add_conditional_wire(self, input, output):
        self._conditional_wires[input] = output

    def remove_conditional_wire(self, input):
        del self._conditional_wires[input]

    def has_conditional_wires(self):
        return (bool(self._conditional_wires) or
                any(child.has_conditional_wires() for child in self._children))

    def add_child(self, child):
        return self._children.append(child)


when = WhenCtx


def _check_prev_when_cond(name):
    global _PREV_WHEN_COND
    if _PREV_WHEN_COND is None:
        raise SyntaxError(f"Cannot use {name} without a previous when")
    prev_cond = _PREV_WHEN_COND
    # Remove it so it can't be used in nesting
    _PREV_WHEN_COND = None
    return prev_cond


def elsewhen(cond):
    return WhenCtx(cond, _check_prev_when_cond('elsewhen'))


def otherwise():
    return WhenCtx(None, _check_prev_when_cond('otherwise'))
