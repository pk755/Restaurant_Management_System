def validate_price(value):
    if value<0:
        raise ValueError("Invalid Price!")
    else:
        return value
    
def validate_quantity(quantity):
    if quantity<0:
        raise ValueError("Invalid Quantity!")
    else:
        return quantity
    
def validate_menu_choice(choice,valid_options):
    if choice not in valid_options:
        raise ValueError("Make a valid choice!")
    else:
        return choice