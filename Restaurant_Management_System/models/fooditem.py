import json
class FoodItem:
    def __init__(self, item_id, name, price, category, stock_quantity):
        self.name = name
        self.price = price
        self.item_id = item_id
        self.category = category
        self.stock_quantity = stock_quantity
    
    
    def is_available(self):
        return self.stock_quantity > 0
    
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }

    @classmethod
    def from_dict(cls, item_id, data):
        return cls(
            item_id=item_id,
            name=data["name"],
            category=data["category"],
            price=data["price"],
            stock_quantity=data["stock_quantity"]
        )

    def __str__(self):
        return f"{self.item_id}. {self.name} ({self.category}) - ${self.price} - Stock: {self.stock_quantity}"
        
