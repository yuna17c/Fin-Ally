class Expenses:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return "Item ('{}', '{}', '{}')".format (self.name, self.price, self.category)

