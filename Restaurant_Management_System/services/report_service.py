import os
from models.order import Order
from utils import file_handler, helpers
import config

def load_all_orders():
    raw_data = file_handler.read_json(config.ORDERS_FILE, default=[])
    return [Order.from_dict(d) for d in raw_data]

def calculate_total_revenue():
    orders = load_all_orders()
    total = sum(order.total_amount for order in orders)
    return total

def best_selling_items(top_n=5):
    orders = load_all_orders()
    sales_count = {}

    for order in orders:
        for item in order.items:
            name = item["name"]
            quantity = item["quantity"]
            if name in sales_count:
                sales_count[name] += quantity
            else:
                sales_count[name] = quantity

    # sort by quantity sold, highest first
    sorted_items = sorted(sales_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_items[:top_n]

def generate_daily_report():
    orders = load_all_orders()
    total_orders = len(orders)
    total_revenue = calculate_total_revenue()
    top_items = best_selling_items()

    lines = []
    lines.append("=" * 35)
    lines.append("       DAILY SALES REPORT")
    lines.append("=" * 35)
    lines.append(f"Generated on : {helpers.get_timestamp()}")
    lines.append(f"Total Orders : {total_orders}")
    lines.append(f"Total Revenue: {helpers.format_currency(total_revenue)}")
    lines.append("-" * 35)
    lines.append("Best Selling Items:")
    
    if not top_items:
        lines.append("  No sales recorded yet.")
    else:
        for rank, (name, quantity) in enumerate(top_items, start=1):
            lines.append(f"  {rank}. {name} - {quantity} sold")

    lines.append("=" * 35)

    report_text = "\n".join(lines)

    try:
        os.makedirs(config.REPORTS_DIR, exist_ok=True)
        report_path = os.path.join(config.REPORTS_DIR, "daily_report.txt")
        with open(report_path, "w") as file:
            file.write(report_text)
        print(f"Report saved to {report_path}")
    except PermissionError:
        print(f"Error: No permission to write report to {report_path}")
    except OSError as e:
        print(f"Error saving report: {e}")

    return report_text