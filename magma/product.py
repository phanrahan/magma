class ProductMeta(type):
    def __call__(cls, *value):
        for v, t in zip(value, cls.fields):
            if not isinstance(v, t):
                raise TypeError('Value {} is not of type {}'.format(v, t))
            print(v, t)
        exit(1)
        return super().__call__(*value)


class Product(metaclass=ProductMeta):
    pass
