import streamlit as st
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

import contextily as ctx

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
orders = pd.read_csv("Dataset/orders_dataset.csv", parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])
product_category_name_translation = pd.read_csv("Dataset/product_category_name_translation.csv")
products = pd.read_csv("Dataset/products_dataset.csv")
sellers = pd.read_csv("Dataset/sellers_dataset.csv")

# Calculate metrics
total_earnings = order_items["price"].sum()  # Total earnings from orders
total_orders = orders["order_id"].nunique()  # Total number of orders
total_customers = customers["customer_unique_id"].nunique()  # Total unique customers
total_products = products["product_id"].nunique()  # Total number of products
total_sellers = sellers["seller_id"].nunique()  # Total number of sellers

# Hitung total pendapatan per payment_type
payment_summary = order_payments.groupby('payment_type')['payment_value'].sum().reset_index()

# Ubah hasil menjadi dictionary untuk diakses dengan cepat
payment_summary_dict = payment_summary.set_index('payment_type')['payment_value'].to_dict()

# Gabungkan dataset untuk mendapatkan data transaksi
recent_transactions = (
    orders.merge(order_items, on="order_id")
    .assign(
        Date=lambda df: pd.to_datetime(df["order_purchase_timestamp"]).dt.strftime(
            "%d %b %Y"
        ),
        Total_Amount=lambda df: df["price"] + df["freight_value"],
    )
    .sort_values(by="order_purchase_timestamp", ascending=False)  # Urutkan berdasarkan tanggal terbaru
    .loc[:, ["order_id", "Date", "order_status", "product_id", "Total_Amount"]]
    .rename(
        columns={
            "order_id": "Transaction ID",
            "order_status": "Status",
            "product_id": "Product ID",
            "Total_Amount": "Total Amount",
        }
    )
    .head(5)  # Ambil 5 transaksi terbaru
)

# Ubah ke format HTML
table_html_rt = recent_transactions.to_html(index=False, classes="card-content table", border=0)

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
        white-space: nowrap;
    }
    .st-emotion-cache-uzeiqp table {
        margin-bottom: 1px;
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

# Layout dengan kolom
cols2 = st.columns([2, 3])

# Card untuk Payment Gateways
with cols2[0]:
    st.markdown(
        f"""
        <div class="card">
            <div class="header">Payment Gateways</div>
            <div class="subheader">Total earnings per payment gateway</div>
            <div class="item">
                <div class="icon">📱</div>
                <div class="details">
                    <div class="title">Boleto</div>
                    <div class="description">Brazil</div>
                </div>
                <div class="amount">${int(payment_summary_dict.get('boleto', 0)):,}</div>
            </div>
            <div class="item">
                <div class="icon">💳</div>
                <div class="details">
                    <div class="title">Debit card</div>
                    <div class="description">Bill payment</div>
                </div>
                <div class="amount">${int(payment_summary_dict.get('debit_card', 0)):,}</div>
            </div>
            <div class="item">
                <div class="icon">💳</div>
                <div class="details">
                    <div class="title">Credit card</div>
                    <div class="description">Money reversed</div>
                </div>
                <div class="amount">${int(payment_summary_dict.get('credit_card', 0)):,}</div>
            </div>
            <div class="item">
                <div class="icon">🔄</div>
                <div class="details">
                    <div class="title">Voucher</div>
                    <div class="description">Bill payment</div>
                </div>
                <div class="amount">${int(payment_summary_dict.get('voucher', 0)):,}</div>
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
                {table_html_rt}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
#Q1
orders['order_year'] = orders['order_purchase_timestamp'].dt.year
orders_2017 = orders[orders['order_year'] == 2017]

orders_2017['delivery_duration'] = (orders_2017['order_delivered_customer_date'] - orders_2017['order_purchase_timestamp']).dt.days

orders_customers = pd.merge(orders_2017, customers, on='customer_id', how='left')

orders_customers_reviews = pd.merge(orders_customers, order_reviews[['order_id', 'review_score']], on='order_id', how='left')

geolocation_unique = geolocation.drop_duplicates(subset=['geolocation_zip_code_prefix', 'geolocation_city'])
merged_data = pd.merge(orders_customers_reviews, geolocation_unique,
                       left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix',
                       how='left')

data_q1 = merged_data[['order_id', 'customer_city', 'delivery_duration', 'review_score',
                          'geolocation_lat', 'geolocation_lng']]

data_q1_cleaned = data_q1.drop_duplicates()

data_q1_cleaned = data_q1_cleaned.dropna(subset=['delivery_duration', 'review_score', 'geolocation_lat', 'geolocation_lng'])

data_q1_cleaned['delivery_duration'] = data_q1_cleaned['delivery_duration'].astype(float)
data_q1_cleaned['review_score'] = data_q1_cleaned['review_score'].astype(float)

data_q1_cleaned.to_csv('Dataset/data_q1_cleaned.csv', index=False)

data_q1_cleaned = pd.read_csv('Dataset/data_q1_cleaned.csv')

city_delivery_stats = data_q1_cleaned.groupby('customer_city')['delivery_duration'].agg(['mean', 'count']).reset_index()
city_delivery_stats.rename(columns={'mean': 'avg_delivery_duration', 'count': 'order_count'}, inplace=True)

top_delivery_cities = city_delivery_stats.sort_values(by='avg_delivery_duration', ascending=False).head(10)

review_stats = data_q1_cleaned.groupby('delivery_duration')['review_score'].mean().reset_index()

# Membuat bar chart dengan Altair
bar_chart = alt.Chart(top_delivery_cities).mark_bar().encode(
    x=alt.X('avg_delivery_duration:Q', title='Rata-Rata Waktu Pengiriman (Hari)'),
    y=alt.Y('customer_city:N', sort='-x', title='Kota'),
    color=alt.Color('avg_delivery_duration:Q', scale=alt.Scale(scheme='viridis'), title='Durasi (Hari)'),
    tooltip=['customer_city', 'avg_delivery_duration', 'order_count']
).properties(
    width=700,
    height=400,
)

st.altair_chart(bar_chart, use_container_width=True)

# Membuat scatter plot dengan threshold
scatter_plot = alt.Chart(review_stats).mark_circle(size=60, color='blue').encode(
    x=alt.X('delivery_duration:Q', title='Durasi Pengiriman (Hari)'),
    y=alt.Y('review_score:Q', title='Rata-Rata Skor Ulasan'),
    tooltip=['delivery_duration', 'review_score']
).properties(
    width=700,
    height=400,
)

# Menambahkan garis threshold vertikal di 10 hari
threshold_line = alt.Chart(pd.DataFrame({'x': [10]})).mark_rule(color='red', strokeDash=[5, 5]).encode(
    x='x:Q'
)

# Gabungkan scatter plot dengan garis threshold
combined_plot = scatter_plot + threshold_line

# Menampilkan scatter plot di Streamlit
st.altair_chart(combined_plot, use_container_width=True)

#Q2
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders_2017 = orders[orders['order_purchase_timestamp'].dt.year == 2017]

data_q2 = orders_2017.merge(order_items, on='order_id', how='inner')
data_q2 = data_q2.merge(customers, on='customer_id', how='inner')
data_q2 = data_q2.merge(order_payments, on='order_id', how='left')

data_q2['total_spent'] = data_q2['price'] + data_q2['freight_value']

data_q2 = data_q2[['customer_unique_id', 'order_id', 'order_purchase_timestamp',
                   'price', 'freight_value', 'total_spent',
                   'payment_value', 'payment_type']]

invalid_total_spent = data_q2[data_q2['total_spent'] < 0]
data_q2['payment_difference'] = abs(data_q2['payment_value'] - data_q2['total_spent'])
invalid_payments = data_q2[data_q2['payment_difference'] > 100]

data_q2_cleaned = data_q2.drop_duplicates()
data_q2_cleaned['order_purchase_timestamp'] = pd.to_datetime(data_q2_cleaned['order_purchase_timestamp'])
data_q2_cleaned = data_q2_cleaned[data_q2_cleaned['payment_difference'] <= 100]

data_q2_cleaned.to_csv('Dataset/data_q2_cleaned.csv', index=False)
data_q2_cleaned = pd.read_csv('Dataset/data_q2_cleaned.csv')

rfm = data_q2_cleaned.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (pd.Timestamp('2018-01-01') - pd.to_datetime(x).max()).days,
    'order_id': 'count',
    'total_spent': 'sum'
}).reset_index()

rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

rfm['R_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1])
rfm['F_score'] = pd.cut(
    rfm['frequency'],
    bins=[0, 1, 2, 5, rfm['frequency'].max()],
    labels=[1, 2, 3, 4],
    include_lowest=True
)
rfm['M_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4])

rfm['RFM_score'] = rfm['R_score'].astype(int) + rfm['F_score'].astype(int) + rfm['M_score'].astype(int)

def segment_customers(rfm_score):
    if rfm_score >= 10:
        return 'Best Customers'
    elif rfm_score >= 7:
        return 'Loyal Customers'
    elif rfm_score >= 5:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['segment'] = rfm['RFM_score'].apply(segment_customers)

#Q3
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
q1_orders = orders[
    (orders['order_purchase_timestamp'] >= '2017-01-01') &
    (orders['order_purchase_timestamp'] <= '2017-03-31')
]

data_q3 = q1_orders.merge(order_items, on='order_id', how='inner')
data_q3 = data_q3.merge(products[['product_id', 'product_category_name']], on='product_id', how='inner')
data_q3 = data_q3.merge(product_category_name_translation, on='product_category_name', how='left')

data_q3_cleaned = data_q3.copy()
data_q3_cleaned['product_category_name_english'].fillna('Unknown', inplace=True)

time_columns = ['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date']
for col in time_columns:
    data_q3_cleaned[col] = pd.to_datetime(data_q3_cleaned[col], errors='coerce')

date_columns = ['order_purchase_timestamp', 'shipping_limit_date', 'order_estimated_delivery_date']
for col in date_columns:
    data_q3_cleaned[col] = pd.to_datetime(data_q3_cleaned[col], errors='coerce')

data_q3_cleaned.drop(columns=['product_category_name'], inplace=True)

data_q3_cleaned.to_csv('Dataset/data_q3_cleaned.csv', index=False)
data_q3_cleaned = pd.read_csv('Dataset/data_q3_cleaned.csv')

data_q3_cleaned['total_revenue'] = data_q3_cleaned['price'] + data_q3_cleaned['freight_value']
revenue_per_category = data_q3_cleaned.groupby('product_category_name_english')['total_revenue'].sum().sort_values(ascending=False)

orders_per_category = data_q3_cleaned.groupby('product_category_name_english')['order_id'].count()
cancelled_per_category = data_q3_cleaned[data_q3_cleaned['order_status'] == 'canceled'].groupby('product_category_name_english')['order_id'].count()
cancel_rate_per_category = (cancelled_per_category / orders_per_category).fillna(0).sort_values(ascending=False)



# # Layout dengan kolom
# cols3 = st.columns([3, 2])

# # Card untuk Rata-Rata Waktu Pengiriman di Kota Teratas
# with cols3[0]:
#     st.markdown(
#         f"""
#         <div class="card">
#             <div class="header">Rata-Rata Waktu Pengiriman di Kota Teratas</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # Card untuk Hubungan Waktu Pengiriman dan Skor Ulasan
# with cols3[1]:
#     st.markdown(
#         f"""
#         <div class="card">
#             <div class="header">Hubungan Waktu Pengiriman dan Skor Ulasan</div>

#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

