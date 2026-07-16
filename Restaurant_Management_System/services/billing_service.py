from utils import helpers
import config
import os

def generate_bill(order):
    lines = []
    lines.append("=" * 35)
    lines.append("     SMART RESTAURANT RECEIPT")
    lines.append("=" * 35)
    lines.append(f"Order ID   : {order.order_id}")
    lines.append(f"Customer   : {order.customer_name}")
    lines.append(f"Date/Time  : {order.timestamp}")
    lines.append("-" * 35)
    lines.append(f"{'Item':<15}{'Qty':<5}{'Price':<8}{'Subtotal':<10}")
    lines.append("-" * 35)
    
    for item in order.items:
        subtotal = item["price"] * item["quantity"]
        lines.append(
            f"{item['name']:<15}{item['quantity']:<5}"
            f"{helpers.format_currency(item['price']):<8}"
            f"{helpers.format_currency(subtotal):<10}"
        )

    lines.append("-" * 35)

    tax_amount = order.total_amount * config.TAX_RATE
    grand_total = order.total_amount + tax_amount

    lines.append(f"{'Subtotal:':<25}{helpers.format_currency(order.total_amount)}")
    lines.append(f"{'Tax (' + str(int(config.TAX_RATE*100)) + '%):':<25}{helpers.format_currency(tax_amount)}")
    lines.append(f"{'TOTAL:':<25}{helpers.format_currency(grand_total)}")
    lines.append("=" * 35)

    return "\n".join(lines)

def print_bill(order):
    print(generate_bill(order))

def save_invoice(order):
    bill_text = generate_bill(order)
    invoice_path = os.path.join(config.INVOICE_DIR, f"{order.order_id}.txt")

    try:
        os.makedirs(config.INVOICE_DIR, exist_ok=True)
        with open(invoice_path, "w") as file:
            file.write(bill_text)
        print(f"Invoice saved to {invoice_path}")
    except PermissionError:
        print(f"Error: No permission to write invoice to {invoice_path}")
    except OSError as e:
        print(f"Error saving invoice: {e}")

