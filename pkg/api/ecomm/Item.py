
class Item:
    quantity: int
    name: str
    category: str

    def __init__(self, quantity: int, name: str, category: str):
        self.quantity = quantity
        self.name = name
        self.category = category