"""
Olist E-Commerce Analytics Dashboard (Streamlit)
Run locally:  streamlit run app.py
"""
import os

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Olist E-Commerce Analytics", page_icon="📦", layout="wide")

PROCESSED = "data/processed"
NAMES = [
    "kpi_summary", "monthly_sales", "category_sales", "delivery_by_state",
    "review_vs_delivery", "payment_types", "top_sellers",
]


@st.cache_data(show_spinner="Loading data... first run downloads the Olist dataset (1-2 min).")
def load_tables():
    # 1) ready-made summary CSVs in data/processed, if present
    if all(os.path.exists(f"{PROCESSED}/{n}.csv") for n in NAMES):
        return {n: pd.read_csv(f"{PROCESSED}/{n}.csv") for n in NAMES}
    # 2) otherwise build them from the raw Olist data (local data/raw or Kaggle)
    import prepare_data
    return prepare_data.build(prepare_data.get_data_path())


def bar(df, x, y, title, horizontal=True, fmt=",.0f"):
    if horizontal:
        enc_x = alt.X(f"{x}:Q", title=title)
        enc_y = alt.Y(f"{y}:N", sort="-x", title=None)
    else:
        enc_x = alt.X(f"{x}:N", title=None)
        enc_y = alt.Y(f"{y}:Q", title=title)
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(x=enc_x, y=enc_y, tooltip=[alt.Tooltip(c, format=fmt) if pd.api.types.is_numeric_dtype(df[c]) else c for c in df.columns])
        .properties(height=max(280, 24 * len(df)) if horizontal else 320)
    )


try:
    T = load_tables()
except Exception as e:  # noqa: BLE001
    st.error("Could not load the data.")
    st.exception(e)
    st.stop()

k = T["kpi_summary"].iloc[0]
monthly = T["monthly_sales"]
cat = T["category_sales"]
state = T["delivery_by_state"]
rv = T["review_vs_delivery"]
pay = T["payment_types"]
sellers = T["top_sellers"]

st.title("📦 Olist E-Commerce Analytics")
st.caption(
    "Brazilian e-commerce marketplace (Olist, 2016-2018): sales, products, delivery, "
    "reviews, payments and sellers. Built with Python, SQL and Streamlit."
)

# ---------------- KPI row ----------------
c = st.columns(5)
c[0].metric("Total orders", f"{int(k.total_orders):,}")
c[1].metric("Unique customers", f"{int(k.total_customers):,}")
c[2].metric("Total payment value", f"R$ {k.total_payment_value/1e6:,.2f}M")
c[3].metric("Avg order value", f"R$ {k.average_order_value:,.2f}")
c[4].metric("Avg review score", f"{k.avg_review_score:.2f} / 5")
c = st.columns(5)
c[0].metric("Delivered orders", f"{int(k.delivered_orders):,}")
c[1].metric("Delivery rate", f"{k.delivery_rate_pct:.1f}%")
c[2].metric("Avg delivery time", f"{k.avg_delivery_days:.1f} days")
c[3].metric("Late deliveries", f"{k.late_delivery_pct:.1f}%")
c[4].metric("Sellers", f"{int(k.total_sellers):,}")

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Sales trend", "🛍️ Products", "🚚 Delivery", "⭐ Reviews", "💳 Payments & sellers"]
)

with tab1:
    st.subheader("Monthly revenue and orders")
    m = monthly.copy()
    base = alt.Chart(m).encode(x=alt.X("purchase_month:N", title="Month", sort=None))
    st.altair_chart(
        base.mark_line(point=True).encode(
            y=alt.Y("revenue:Q", title="Revenue (BRL)"),
            tooltip=["purchase_month", alt.Tooltip("revenue", format=",.0f"), "orders"],
        ).properties(height=320),
        use_container_width=True,
    )
    st.altair_chart(
        base.mark_bar().encode(
            y=alt.Y("orders:Q", title="Orders"), tooltip=["purchase_month", "orders"]
        ).properties(height=260),
        use_container_width=True,
    )
    st.caption("Trimmed to Jan 2017 - Aug 2018; the dataset has very few orders outside this range.")

with tab2:
    st.subheader("Top product categories by revenue")
    n = st.slider("Number of categories", 5, 25, 10)
    st.altair_chart(bar(cat.head(n), "revenue", "category", "Revenue (BRL)"), use_container_width=True)
    st.subheader("Average review score of top categories")
    st.dataframe(
        cat.head(n)[["category", "orders", "revenue", "avg_review"]],
        use_container_width=True, hide_index=True,
    )

with tab3:
    st.subheader("Late deliveries by customer state")
    min_orders = st.slider("Only states with at least this many orders", 0, 2000, 100, step=50)
    s = state[state["orders"] >= min_orders]
    st.altair_chart(bar(s, "late_pct", "customer_state", "Late deliveries (%)", fmt=".1f"), use_container_width=True)
    st.subheader("Average delivery time by state")
    st.altair_chart(bar(s, "avg_delivery_days", "customer_state", "Days", fmt=".1f"), use_container_width=True)

with tab4:
    st.subheader("Does late delivery hurt reviews?")
    st.altair_chart(
        bar(rv, "review_score", "late_pct", "Late deliveries (%)", horizontal=False, fmt=".1f"),
        use_container_width=True,
    )
    st.dataframe(rv, use_container_width=True, hide_index=True)

with tab5:
    a, b = st.columns(2)
    with a:
        st.subheader("Payment types (by value)")
        st.altair_chart(bar(pay, "value", "payment_type", "Payment value (BRL)"), use_container_width=True)
    with b:
        st.subheader("Top 10 sellers by revenue")
        st.dataframe(sellers.head(10), use_container_width=True, hide_index=True)

# ---------------- Insights (computed from the data) ----------------
st.divider()
st.subheader("Key insights")
top_cat = cat.iloc[0]
top5_share = 100 * cat.head(5)["revenue"].sum() / cat["revenue"].sum()
worst_state = state[state["orders"] >= 100].sort_values("late_pct", ascending=False).iloc[0]
low = rv[rv["review_score"] <= 2]["late_pct"].mean()
high = rv[rv["review_score"] >= 4]["late_pct"].mean()
top_pay = pay.iloc[0]
pay_share = 100 * top_pay["value"] / pay["value"].sum()
best_month = monthly.sort_values("revenue", ascending=False).iloc[0]

st.markdown(
    f"""
- **Top category:** `{top_cat['category']}` earns the most item revenue (R$ {top_cat['revenue']:,.0f}); the top 5 categories make up **{top5_share:.0f}%** of item revenue.
- **Best month:** {best_month['purchase_month']} with R$ {best_month['revenue']:,.0f} revenue.
- **Delivery vs reviews:** orders rated 1-2 stars were late **{low:.1f}%** of the time versus **{high:.1f}%** for 4-5 star orders.
- **Weakest region:** `{worst_state['customer_state']}` has the highest late-delivery rate ({worst_state['late_pct']:.1f}%) among states with 100+ orders.
- **Payments:** `{top_pay['payment_type']}` accounts for **{pay_share:.0f}%** of total payment value.
"""
)
st.caption("Data: Olist Brazilian E-Commerce Public Dataset (Kaggle). Project by Aayush Sharma.")
