import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="E-commerce - Faaris Muda Dwi Nugraha",
    page_icon="🔶",
    layout="wide",
)

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Load datasets
customers = pd.read_csv("Dataset/customers_dataset.csv")
geolocation = pd.read_csv("Dataset/geolocation_dataset.csv")
order_items = pd.read_csv("Dataset/order_items_dataset.csv")
order_payments = pd.read_csv("Dataset/order_payments_dataset.csv")
order_reviews = pd.read_csv("Dataset/order_reviews_dataset.csv")
orders = pd.read_csv("Dataset/orders_dataset.csv")
products = pd.read_csv("Dataset/products_dataset.csv")
sellers = pd.read_csv("Dataset/sellers_dataset.csv")

# Calculate metrics
total_earnings = order_items["price"].sum()  # Total earnings from orders
total_orders = orders["order_id"].nunique()  # Total number of orders
total_customers = customers["customer_unique_id"].nunique()  # Total unique customers
total_products = products["product_id"].nunique()  # Total number of products
total_sellers = sellers["seller_id"].nunique()  # Total number of sellers

# Layout for 5 cards with equal spacing
cols = st.columns([1, 1, 1, 1, 1])

# Card 1: Total Earnings
with cols[0]:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 7px; padding: 20px; text-align: center; 
                    box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px; margin: 10px;">
            <div style="font-size: 50px; margin-bottom: 10px;">🛒</div>
            <div>Total Earnings</div>
            <div style="font-size: 24px; font-weight: bold;">${total_earnings:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 2: Total Orders
with cols[1]:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 7px; padding: 20px; text-align: center; 
                    box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px; margin: 10px;">
            <div style="font-size: 50px; margin-bottom: 10px;">📃</div>
            <div>Orders</div>
            <div style="font-size: 24px; font-weight: bold;">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 3: Total Customers
with cols[2]:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 7px; padding: 20px; text-align: center; 
                    box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px; margin: 10px;">
            <div style="font-size: 50px; margin-bottom: 10px;">👤</div>
            <div>Customers</div>
            <div style="font-size: 24px; font-weight: bold;">{total_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 4: Total Products
with cols[3]:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 7px; padding: 20px; text-align: center; 
                    box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px; margin: 10px;">
            <div style="font-size: 50px; margin-bottom: 10px;">🪑</div>
            <div>Products</div>
            <div style="font-size: 24px; font-weight: bold;">{total_products:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 5: Total Sellers
with cols[4]:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 7px; padding: 20px; text-align: center; 
                    box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px; margin: 10px;">
            <div style="font-size: 50px; margin-bottom: 10px;">💼</div>
            <div>Sellers</div>
            <div style="font-size: 24px; font-weight: bold;">{total_sellers:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# CSS styling untuk card
st.markdown(
    """
    <style>
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 7px;
        box-shadow: rgba(145, 158, 171, 0.2) 0px 0px 2px 0px,rgba(145, 158, 171, 0.12) 0px 12px 24px -4px;
        margin: 10px;
    }
    .header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader {
        color: gray;
        font-size: 14px;
        margin-bottom: 15px;
    }
    .item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .icon {
        display: flex;
        align-items: center;
        font-size: 20px;
    }
    .details {
        flex: 1;
        margin-left: 10px;
    }
    .details .title {
        font-size: 16px;
        font-weight: bold;
    }
    .details .description {
        font-size: 12px;
        color: gray;
    }
    .amount {
        font-size: 16px;
        font-weight: bold;
        color: black;
    }
    .amount.negative {
        color: red;
    }
    
    .card-content {
        overflow-x: auto;
        max-width: 100%;
        padding-bottom: 14px;
    }
    
    .card-content table {
        width: 100%;
        border-collapse: collapse;
    }
    .card-content table th,
    .card-content table td {
        border: 1px solid #ddd;
        padding: 6.8px;
        text-align: left;
    }
    .st-emotion-cache-uzeiqp table {
        margin-bottom: 0px;
    }
    .card-content table th {
        background-color: #f4f4f4;
        font-weight: bold;
    }
    .card-content table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .card-content table tr:hover {
        background-color: #f1f1f1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data untuk Recent Transactions
data = {
    "Transaction ID": ["#369451", "#541285", "#545710", "#558964", "#562100"],
    "Date": ["13 Aug 2024", "20 Feb 2024", "10 Sep 2024", "02 Jun 2024", "20 Sep 2024"],
    "Customers": [
        "Jenny Wilson",
        "Wade Warren",
        "Cody Fisher",
        "Albert Flores",
        "Cody Fisher",
    ],
    "Product": [
        "Long Dress",
        "Samsung TV",
        "Comfort Sofa",
        "Spring Bed",
        "Comfort Sofa",
    ],
    "QTY": [212, 512, 500, 620, 208],
    "Payments": ["Bank Transfer", "PayPal", "Credit Card", "Gpay", "Credit Card"],
    "Total Amount": ["$12.32", "$52.00", "$14.35", "$82.00", "$45.87"],
}
df = pd.DataFrame(data)
table_html = df.to_html(index=False, classes="card-content table", border=0)

# Layout dengan kolom
cols2 = st.columns([2, 3])

# Card untuk Payment Gateways
with cols2[0]:
    st.markdown(
        """
        <div class="card">
            <div class="header">Payment Gateways</div>
            <div class="subheader">Total earnings per payment gateway</div>
            <div class="item">
                <div class="icon">💳</div>
                <div class="details">
                    <div class="title">Boleto</div>
                    <div class="description">Big Brands</div>
                </div>
                <div class="amount">+6,235</div>
            </div>
            <div class="item">
                <div class="icon">💵</div>
                <div class="details">
                    <div class="title">Debit card</div>
                    <div class="description">Bill payment</div>
                </div>
                <div class="amount">+345</div>
            </div>
            <div class="item">
                <div class="icon">💳</div>
                <div class="details">
                    <div class="title">Credit card</div>
                    <div class="description">Money reversed</div>
                </div>
                <div class="amount">+2,235</div>
            </div>
            <div class="item">
                <div class="icon">🔄</div>
                <div class="details">
                    <div class="title">Voucher</div>
                    <div class="description">Bill payment</div>
                </div>
                <div class="amount negative">-32</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card untuk Recent Transactions
with cols2[1]:
    st.markdown(
        f"""
        <div class="card">
            <div class="header">Recent Transactions</div>
            <div class="card-content">
                {table_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
