import pandas as pd
from pathlib import Path

BASE_DIR = Path(**file**).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_csv(filename):
file_path = RAW_DIR / filename

```
if not file_path.exists():
    print(f"File not found: {filename}")
    return None

return pd.read_csv(file_path)
```

def prepare_orders():
orders = load_csv("olist_orders_dataset.csv")

```
if orders is None:
    return

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    if column in orders.columns:
        orders[column] = pd.to_datetime(
            orders[column], errors="coerce"
        )

duplicate_count = orders.duplicated(subset="order_id").sum()

print("Orders loaded:", len(orders))
print("Duplicate order IDs:", duplicate_count)
print("Missing values by column:")
print(orders.isnull().sum())

# Keep one row per order ID if duplicate IDs exist.
orders = orders.drop_duplicates(
    subset="order_id", keep="first"
)

orders.to_csv(
    PROCESSED_DIR / "orders_clean.csv",
    index=False
)

print("Saved: data/processed/orders_clean.csv")
```

def prepare_order_items():
items = load_csv("olist_order_items_dataset.csv")

```
if items is None:
    return

print("Order items loaded:", len(items))
print("Duplicate rows:", items.duplicated().sum())

items = items.drop_duplicates()

items.to_csv(
    PROCESSED_DIR / "order_items_clean.csv",
    index=False
)

print("Saved: data/processed/order_items_clean.csv")
```

def main():
if not RAW_DIR.exists():
print("Raw data folder does not exist.")
print("Create data/raw and add the Olist CSV files.")
return

```
prepare_orders()
prepare_order_items()
```

if **name** == "**main**":
main()

