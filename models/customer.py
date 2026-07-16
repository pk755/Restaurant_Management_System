from order import order_details

class Customer:
    def __init__(self,name,contact,order_history=None):
        self.name = name
        self.contact = contact
        self.order_history = order_history if order_history is not None else []
        
    def add_order(self,order_id):
        self.order_history.append(order_id)
    
    def to_dict(self):
        return {
            "name": self.name,
            "contact_number": self.contact_number,
            "order_history": self.order_history
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            contact_number=data["contact_number"],
            order_history=data["order_history"]
        )

    def __str__(self):
        return f"{self.name} ({self.contact_number}) - {len(self.order_history)} orders"