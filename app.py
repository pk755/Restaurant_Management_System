import streamlit as st
from services import menu_service, order_service, billing_service,report_service
from utils import validator

st.set_page_config(page_title="BOXNCOX Restaurant", layout = "wide")

if "menu_list" not in st.session_state:
    st.session_state.menu_list = menu_service.load_menu()

menu_list = st.session_state.menu_list

st.title("BOXNOX Restaurant")
tab_menu, tab_order, tab_admin, tab_billing = st.tabs(["Menu","New Order","Admin","Billing"])

#menu tab
with tab_menu:
    if not  menu_list:
        st.info("No items yet — add some from the Admin tab.")

    for item in menu_list:
        cols = st.columns([3, 2, 2, 2])
        cols[0].write(f"**{item.name}**  ({item.category})")
        cols[1].write(f"${item.price:.2f}")
        cols[2].write(f"Stock: {item.stock_quantity}")
        cols[3].write("Available" if item.is_available() else  "Out of stock")

#order tab
with tab_order:
    st.subheader("Place an order")
    customer_name = st.text_input("Customer name")
    available_items = [i for i in menu_list if i.is_available()]
    selections = []
    if not available_items:
        st.warning("Nothing in stock right now.")
    else:
        st.caption("Set a quantity for anything the customer wants.")
        for item in available_items:
            qty = st.number_input(
                f"{item.name} (${item.price:.2f}, {item.stock_quantity} in stock)",
                min_value=0, max_value=int(item.stock_quantity), step=1,
                key=f"qty_{item.item_id}",
            )
            if qty > 0:
                selections.append({"item_id": item.item_id, "quantity": qty})
    if st.button("Place order", type="primary", disabled=not customer_name or not selections):
        try:
            order = order_service.create_order(customer_name, selections, menu_list)
            order_service.save_order(order)
            billing_service.save_invoice(order)
            st.success(f"Order {order.order_id} placed for {customer_name}.")
            st.code(billing_service.generate_bill(order))
            for item in available_items:
                st.session_state.pop(f"qty_{item.item_id}", None)
            st.rerun()
        except order_service.InsufficientStockError as e:
            st.error(str(e))
        except ValueError as e:
            st.error(str(e))

#billing tab
with tab_billing:
    st.subheader("Look up a bill")
    all_orders = order_service.load_all_orders()
    if not all_orders:
        st.info("No orders placed yet.")
    else:
        order = st.selectbox(
            "Order",
            sorted(all_orders, key=lambda o: o.timestamp, reverse=True),
            format_func=lambda o: f"{o.order_id} — {o.customer_name} ({o.timestamp})",
        )
        bill_text = billing_service.generate_bill(order)
        st.code(bill_text)
        st.download_button(
            "Download bill", bill_text,
            file_name=f"{order.order_id}.txt", key="download_lookup_bill",
        )

#admin tab
with tab_admin:
    st.subheader("Manage the menu")
    action = st.radio("",["Add item", "Update price", "Update stock", "Remove item"], horizontal=True)
    if action == "Add item":
        with st.form("add_item_form"):
            name = st.text_input("Item name")
            category = st.selectbox("Category", ["starter", "main", "dessert", "beverage"])
            price = st.number_input("Price", min_value=0.0, step=0.5)
            stock = st.number_input("Stock quantity", min_value=0, step=1)
            submitted = st.form_submit_button("Add item")
        if submitted:
            try:
                validator.validate_price(price)
                validator.validate_quantity(stock)
                menu_service.add_item(menu_list, name, category, price, stock)
                st.success(f"Added {name}.")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    elif action == "Update price":
        if not menu_list:
            st.info("No items to update yet.")
        else:
            item = st.selectbox("Item", menu_list, format_func=lambda i: f"{i.item_id} — {i.name}", key="price_item")
            new_price = st.number_input("New price", min_value=0.0, step=0.5, value=float(item.price))
            if st.button("Update price"):
                try:
                    menu_service.update_price(menu_list, item.item_id, new_price)
                    st.success(f"Updated {item.name}'s price to ${new_price:.2f}.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    elif action == "Update stock":
        if not menu_list:
            st.info("No items to update yet.")
        else:
            item = st.selectbox("Item", menu_list, format_func=lambda i: f"{i.item_id} — {i.name}", key="stock_item")
            change = st.number_input("Quantity change (+/-)", step=1, value=0)
            if st.button("Update stock"):
                try:
                    menu_service.update_stock(menu_list, item.item_id, change)
                    st.success(f"{item.name} stock is now {item.stock_quantity}.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    elif action == "Remove item" :  
        if not menu_list:
            st.info("No items to remove.")
        else:
            item = st.selectbox("Item", menu_list, format_func=lambda i: f"{i.item_id} — {i.name}", key="remove_item")
            if st.button("Remove item"):
                menu_service.remove_item(menu_list, item.item_id)
                st.success(f"Removed {item.name}.")
                st.rerun()
                
    else: #View Report
        scope = st.radio("Scope", ["Today", "All time", "Specific date"], horizontal=True, key="report_scope")
        if scope == "Today":
            report_text = report_service.generate_daily_report()
        elif scope == "All time":
            report_text = report_service.generate_full_report()
        else:
            picked = st.date_input("Date")
            report_text = report_service.generate_daily_report(picked.strftime("%Y-%m-%d"))

        st.code(report_text)
        st.download_button("Download report", report_text, file_name="sales_report.txt", key="download_report")


        
