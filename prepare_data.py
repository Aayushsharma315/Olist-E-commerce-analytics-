"""
Olist E-Commerce Analytics - data preparation.

build(path) reads the raw Olist CSV files, cleans them and returns small
summary tables. The Streamlit app (app.py) calls build() automatically;
you can also run this file directly to save the tables as CSV files:

    python prepare_data.py
"""
import os
import pandas as pd

OUT_DIR = os.environ.get("OUT_DIR", "data/processed")


def get_data_path():
    """Use data/raw if the CSVs are there, otherwise download from Kaggle."""
    local = "data/raw"
    if os.path.exists(os.path.join(local, "olist_orders_dataset.csv")):
        return local
    import kagglehub
    return kagglehub.dataset_download("olistbr/brazilian-ecommerce")


def _read(path, name, **kw):
    return pd.read_csv(os.path.join(path, name), **kw)


def build(path):
    date_cols = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    orders = _read(path, "olist_orders_dataset.csv", parse_dates=date_cols)
    items = _read(path, "olist_order_items_dataset.csv")
    pays = _read(path, "olist_order_payments_dataset.csv")
    reviews = _read(path, "olist_order_reviews_dataset.csv")
    cust = _read(path, "olist_customers_dataset.csv")
    prods = _read(path, "olist_products_dataset.csv")
    sellers = _read(path, "olist_sellers_dataset.csv")
    cat = _read(path, "product_category_name_translation.csv")

    # ---- cleaning ----
    orders = orders.drop_duplicates("order_id")
    reviews = reviews.drop_duplicates("review_id")
    # some orders have more than one review -> one score per order
    review_per_order = reviews.groupby("order_id", as_index=False)["review_score"].mean()

    orders["purchase_month"] = (
        orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    )
    orders["delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.days
    orders["is_late"] = (
        orders["order_delivered_customer_date"] > orders["order_estimated_delivery_date"]
    )
    delivered = orders[
        (orders["order_status"] == "delivered")
        & orders["order_delivered_customer_date"].notna()
    ].copy()

    order_pay = pays.groupby("order_id", as_index=False)["payment_value"].sum()
    orders = orders.merge(order_pay, on="order_id", how="left")
    delivered = delivered.merge(review_per_order, on="order_id", how="left")
    delivered = delivered.merge(
        cust[["customer_id", "customer_state"]], on="customer_id", how="left"
    )

    out = {}

    # ---- 1. KPI summary ----
    out["kpi_summary"] = pd.DataFrame([{
        "total_orders": orders["order_id"].nunique(),
        "total_customers": cust["customer_unique_id"].nunique(),
        "total_payment_value": round(pays["payment_value"].sum(), 2),
        "average_order_value": round(order_pay["payment_value"].mean(), 2),
        "delivered_orders": int((orders["order_status"] == "delivered").sum()),
        "delivery_rate_pct": round(
            100 * (orders["order_status"] == "delivered").mean(), 2
        ),
        "avg_review_score": round(reviews["review_score"].mean(), 2),
        "total_sellers": sellers["seller_id"].nunique(),
        "avg_delivery_days": round(delivered["delivery_days"].mean(), 1),
        "late_delivery_pct": round(100 * delivered["is_late"].mean(), 2),
    }])

    # ---- 2. Monthly sales (data is very sparse outside Jan 2017 - Aug 2018) ----
    monthly = (
        orders.groupby("purchase_month")
        .agg(orders=("order_id", "nunique"), revenue=("payment_value", "sum"))
        .reset_index()
    )
    monthly = monthly[
        (monthly["purchase_month"] >= "2017-01")
        & (monthly["purchase_month"] <= "2018-08")
    ]
    monthly["revenue"] = monthly["revenue"].round(2)
    out["monthly_sales"] = monthly

    # ---- 3. Category sales ----
    it = items.merge(
        prods[["product_id", "product_category_name"]], on="product_id", how="left"
    ).merge(cat, on="product_category_name", how="left")
    it["category"] = it["product_category_name_english"].fillna("unknown")
    it = it.merge(review_per_order, on="order_id", how="left")
    out["category_sales"] = (
        it.groupby("category")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("price", "sum"),
            avg_review=("review_score", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    # ---- 4. Delivery by state ----
    by_state = (
        delivered.groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            avg_delivery_days=("delivery_days", "mean"),
            late_pct=("is_late", "mean"),
        )
        .reset_index()
    )
    by_state["avg_delivery_days"] = by_state["avg_delivery_days"].round(1)
    by_state["late_pct"] = (100 * by_state["late_pct"]).round(2)
    out["delivery_by_state"] = by_state.sort_values("orders", ascending=False)

    # ---- 5. Review score vs delivery ----
    rv = (
        delivered.dropna(subset=["review_score"])
        .assign(review_score=lambda d: d["review_score"].round().astype(int))
        .groupby("review_score")
        .agg(
            orders=("order_id", "nunique"),
            avg_delivery_days=("delivery_days", "mean"),
            late_pct=("is_late", "mean"),
        )
        .reset_index()
    )
    rv["avg_delivery_days"] = rv["avg_delivery_days"].round(1)
    rv["late_pct"] = (100 * rv["late_pct"]).round(2)
    out["review_vs_delivery"] = rv

    # ---- 6. Payment types ----
    out["payment_types"] = (
        pays.groupby("payment_type")
        .agg(payments=("order_id", "count"), value=("payment_value", "sum"))
        .round(2)
        .reset_index()
        .sort_values("value", ascending=False)
    )

    # ---- 7. Top sellers ----
    s = items.merge(review_per_order, on="order_id", how="left").merge(
        sellers[["seller_id", "seller_state"]], on="seller_id", how="left"
    )
    out["top_sellers"] = (
        s.groupby(["seller_id", "seller_state"])
        .agg(
            orders=("order_id", "nunique"),
            revenue=("price", "sum"),
            avg_review=("review_score", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(100)
    )
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tables = build(get_data_path())
    for name, df in tables.items():
        df.to_csv(os.path.join(OUT_DIR, f"{name}.csv"), index=False)
        print(f"saved {name}.csv: {len(df)} rows")


if __name__ == "__main__":
    main()
