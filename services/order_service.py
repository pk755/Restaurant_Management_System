from models.order import Order
from services import menu_service
from utils import file_handler, helpers, validator
import config

class InsufficientStockError(Exception):
    pass

def create_order(customer_name, item_selections, menu_list):
    items = []

    for selection in item_selections:
        item_id = selection["item_id"]
        quantity = selection["quantity"]

        food_item = menu_service.find_item_by_id(menu_list, item_id)
        if food_item is None:
            raise ValueError(f"No menu item found with id {item_id}")

        if food_item.stock_quantity < quantity:
            raise InsufficientStockError(
                f"Not enough stock for {food_item.name}. "
                f"Requested: {quantity}, Available: {food_item.stock_quantity}"
            )

        items.append({
            "name": food_item.name,
            "price": food_item.price,      # locked in at order time
            "quantity": quantity
        })
    for selection in item_selections:
        menu_service.update_stock(menu_list, selection["item_id"], -selection["quantity"])

    order = Order(
        order_id=helpers.generate_order_id(),
        customer_name=customer_name,
        items=items,
       timestamp=helpers.get_timestamp()
    )

    return order

def save_order(order):
    all_orders = file_handler.read_json(config.ORDERS_FILE, default=[])
    all_orders.append(order.to_dict())
    file_handler.write_json(config.ORDERS_FILE, all_orders)

def load_all_orders():
    raw_data = file_handler.read_json(config.ORDERS_FILE, default=[])
    return [Order.from_dict(d) for d in raw_data]

def get_order_by_id(order_id):
    all_orders = load_all_orders()
    for order in all_orders:
        if order.order_id == order_id:
            return order
    return None