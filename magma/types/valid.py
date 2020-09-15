from magma.bit import Bit
from magma.t import Type
from magma.tuple import Product, ProductKind


class ValidKind(ProductKind):
    def __getitem__(cls, T: Type):
        if not issubclass(T, Type):
            raise TypeError(
                f"Valid[T] expected T to be a subclass of m.Type not {T}"
            )
        fields = {"valid": Bit, "data": T}
        return type(f"Valid[{T}]", (Valid, ), fields)


class Valid(Product, metaclass=ValidKind):
    pass
