import json
class Order:
    def __init__(self,order_id,customer_name,items,timestamp, status="pending"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.timestamp = timestamp
        self.status = status
        self.total_amount = self.calculate_total()
    
    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total
    
    
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "timestamp": self.timestamp,
            "status": self.status,
            "total_amount": self.calculate_total()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_id=data["order_id"],
            customer_name=data["customer_name"],
            items=data["items"],
            timestamp=data["timestamp"],
            status=data["status"]
        )    