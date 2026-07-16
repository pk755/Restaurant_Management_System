import json
class Order:
    def __init__(self,order_id,customer_name,items,time_stamp, status):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.time_stamp = time_stamp
        self.status = status
    
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