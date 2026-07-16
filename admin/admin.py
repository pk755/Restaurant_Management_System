from services import menu_service, report_service
from utils import validator

def admin_menu(menu_list):
    while True:
        print("\n----- ADMIN MENU -----")
        print("1. View Menu")
        print("2. Add New Item")
        print("3. Update Price")
        print("4. Update Stock")
        print("5. Remove Item")
        print("6. View Sales Report")
        print("7. Exit Admin Menu")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            menu_service.display_menu(menu_list)

        elif choice == "2":
            add_item_flow(menu_list)

        elif choice == "3":
            update_price_flow(menu_list)

        elif choice == "4":
            update_stock_flow(menu_list)

        elif choice == "5":
            remove_item_flow(menu_list)

        elif choice == "6":
            report_text = report_service.generate_daily_report()
            print(report_text)

        elif choice == "7":
            print("Exiting admin menu...")
            break

        else:
            print("Invalid choice. Please enter a number from 1-7.")

def add_item_flow(menu_list):
    try:
        name = input("Item name: ")
        category = input("Category (starter/main/dessert/beverage): ")
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))

        validator.validate_price(price)
        validator.validate_quantity(stock)

        menu_service.add_item(menu_list, name, category, price, stock)

    except ValueError as e:
        print(f"Invalid input: {e}")
        
def update_price_flow(menu_list):
    try:
        item_id = input("Enter item id to update: ")
        new_price = float(input("Enter new price: "))

        menu_service.update_price(menu_list, item_id, new_price)

    except ValueError as e:
        print(f"Invalid input: {e}")

def update_stock_flow(menu_list):
    try:
        item_id = input("Enter item id to restock/adjust: ")
        quantity_change = int(input("Enter quantity change (e.g. 10 or -5): "))

        menu_service.update_stock(menu_list, item_id, quantity_change)
        print("Stock updated successfully.")

    except ValueError as e:
        print(f"Invalid input: {e}")
        
def remove_item_flow(menu_list):
    try:
        item_id = input("Enter item id to remove: ")
        menu_service.remove_item(menu_list, item_id)

    except ValueError as e:
        print(f"Invalid input: {e}")