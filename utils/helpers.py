import datetime
import random
import config

def get_timestamp():
    time_now = datetime.datetime.now()
    return time_now.strftime("%Y-%m-%d %H:%M:%S")

def generate_order_id():
    now = datetime.datetime.now()
    timestamp_part = now.strftime("%Y%m%d%H%M%S")
    return f"ORD{timestamp_part}"

def format_currency(amount):
    return f"{config.CURRENCY_SYMBOL}{amount:.2f}"