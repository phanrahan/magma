from magma.common import prologue, epilogue


def test_prologue():

    def prologue_fn(lst):
        lst[0] = True

    @prologue(prologue_fn)
    def fn(lst):
        assert lst[0] is True
        lst[1] = True

    fn([False for _ in range(10)])


def test_epilogue():

    def epilogue_fn(lst):
        lst[0] = True

    @epilogue(epilogue_fn)
    def fn(lst):
        assert lst[0] is False
        lst[1] = True

    my_lst = [False for _ in range(10)]
    fn(my_lst)
    assert my_lst[0] is True
