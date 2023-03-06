class Converter:

    @staticmethod
    def to_convert(obj, unit1, unit2):
        print("A")

    @classmethod
    def convert(cls, obj, unit1, unit2):
        cls.to_convert(1, 1, 1)


class RandomConverter(Converter):
    @staticmethod
    def to_convert(obj, unit1, unit2):
        print("B")



print(RandomConverter.convert(1, 1, 1))
print(Converter.convert(1, 1, 1))
