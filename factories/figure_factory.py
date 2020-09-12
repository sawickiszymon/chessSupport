import factory


class FigureFactory(factory.DictFactory):
    field = factory.Sequence(lambda n: f"H{n % 7 + 1}")
