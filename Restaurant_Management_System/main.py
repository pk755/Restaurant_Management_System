from services import menu_service, order_service, billing_service
from services.order_service import InsufficientStockError
from admin import admin
from utils import validator

def customer_flow(menu_list):
    menu_service.display_menu(menu_list)

    customer_name = input("Enter your name: ")
    selections = []

    print("\nEnter item id and quantity to order. Type 'done' when finished.")

    while True:
        item_id = input("Item id (or 'done'): ")
        if item_id.lower() == "done":
            break
        
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Please enter a valid number for quantity.")
            continue

        selections.append({"item_id": item_id, "quantity": quantity})

    if not selections:
        print("No items selected. Returning to main menu.")
        return

    try:
        order = order_service.create_order(customer_name, selections, menu_list)
        order_service.save_order(order)

        billing_service.print_bill(order)
        billing_service.save_invoice(order)

    except InsufficientStockError as e:
        print(f"Order failed: {e}")
    except ValueError as e:
        print(f"Invalid order: {e}")

def main():
    menu_list = menu_service.load_menu()
    while True:
        print("\n===== SMART RESTAURANT MANAGEMENT SYSTEM =====")
        print("1. Customer")
        print("2. Admin")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_flow(menu_list)

        elif choice == "2":
            admin.admin_menu(menu_list)

        elif choice == "3":
            print("Thank you for using Smart Restaurant Management System!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            
if __name__ == "__main__":
    main()