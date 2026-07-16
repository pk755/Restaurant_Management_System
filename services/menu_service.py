from models.fooditem import FoodItem
from utils import file_handler
from utils import validator
import config

def load_menu():
    raw_data = file_handler.read_json(config.MENU_FILE, default={})
    menu_list = []
    for item_id, item_data in raw_data.items():
        menu_list.append(FoodItem.from_dict(item_id, item_data))
    return menu_list

def save_menu(menu_list):
    data = {}
    for item in menu_list:
        data[item.item_id] = item.to_dict()
    success = file_handler.write_json(config.MENU_FILE, data)
    if not success:
        print("Warning: menu could not be saved.")

def display_menu(menu_list):
    print("\n----- MENU -----")
    if not menu_list:
        print("No items available.")
        return

    for item in menu_list:
        status = "" if item.is_available() else "  (OUT OF STOCK)"
        print(f"{item}{status}")
    print("-----------------\n")
    
def find_item_by_id(menu_list, item_id):
    for item in menu_list:
        if item.item_id == item_id:
            return item
    return None

def generate_next_item_id(menu_list):
    if not menu_list:
        return "1"
    existing_ids = [int(item.item_id) for item in menu_list]
    return str(max(existing_ids) + 1)

def add_item(menu_list, name, category, price, stock):
    validator.validate_price(price)
    validator.validate_quantity(stock)

    new_id = generate_next_item_id(menu_list)
    new_item = FoodItem(new_id, name, category, price, stock)
    menu_list.append(new_item)
    save_menu(menu_list)
    print(f"Added: {new_item}")
    return new_item

def update_price(menu_list, item_id, new_price):
    validator.validate_price(new_price)

    item = find_item_by_id(menu_list, item_id)
    if item is None:
        raise ValueError(f"No item found with id {item_id}")

    item.price = new_price
    save_menu(menu_list)
    print(f"Updated price for {item.name} -> {new_price}")

def update_stock(menu_list, item_id, quantity_change):
    item = find_item_by_id(menu_list, item_id)
    if item is None:
        raise ValueError(f"No item found with id {item_id}")

    new_quantity = item.stock_quantity + quantity_change
    if new_quantity < 0:
        raise ValueError(f"Cannot reduce stock below 0 for {item.name}")

    item.stock_quantity = new_quantity
    save_menu(menu_list)
    
def remove_item(menu_list, item_id):
    item = find_item_by_id(menu_list, item_id)
    if item is None:
        raise ValueError(f"No item found with id {item_id}")

    menu_list.remove(item)
    save_menu(menu_list)
    print(f"Removed: {item.name}")