import streamlit as st
import requests
from data import products

st.set_page_config(page_title="InstaMart", page_icon="🛒", layout="wide")
st.title("🛒 InstaMart Grocery App")

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Sidebar: category filter
categories = sorted(set([p["category"] for p in products]))
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)
search = st.sidebar.text_input("Search product")

# Filter products
filtered_products = products
if selected_category != "All":
    filtered_products = [p for p in filtered_products if p["category"] == selected_category]
if search:
    filtered_products = [p for p in filtered_products if search.lower() in p["name"].lower()]

# Display products
st.subheader("Products")
cols = st.columns(3)
for i, product in enumerate(filtered_products):
    with cols[i % 3]:
        st.markdown(f"### {product['name']}")
        st.write(f"Category: {product['category']}")
        st.write(f"Price: ${product['price']}")
        qty = st.number_input(
            f"Qty_{product['name']}",
            min_value=0,
            max_value=100,
            value=st.session_state.cart.get(product["name"], 0),
            key=product["name"]
        )
        if qty > 0:
            st.session_state.cart[product["name"]] = qty
        elif product["name"] in st.session_state.cart:
            del st.session_state.cart[product["name"]]

# Checkout button
if st.button("Checkout"):
    if st.session_state.cart:
        order_data = {
            "items": st.session_state.cart,
            "total": sum(
                qty * next(p["price"] for p in products if p["name"] == item)
                for item, qty in st.session_state.cart.items()
            )
        }
        try:
            res = requests.post("http://127.0.0.1:5050/place_order", json=order_data)
            if res.status_code == 200:
                st.balloons()
                st.success("Order sent to store successfully 🚚")
                st.session_state.cart = {}
            else:
                st.error("Failed to send order to server")
        except Exception as e:
            st.error(f"Error sending order: {e}")
    else:
        st.info("Your cart is empty")
