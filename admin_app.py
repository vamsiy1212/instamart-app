import streamlit as st
import requests

st.set_page_config(page_title="InstaMart Admin", page_icon="📦", layout="wide")
st.title("📦 Store Orders Dashboard")

try:
    res = requests.get("http://127.0.0.1:5050/get_orders")
    orders = res.json()
except Exception as e:
    st.error(f"Cannot connect to server: {e}")
    orders = []

if orders:
    for i, order in enumerate(orders, 1):
        st.subheader(f"Order #{i}")
        st.write("Items:", order["items"])
        st.write("Total:", order["total"])
        st.divider()
else:
    st.info("No orders yet.")
