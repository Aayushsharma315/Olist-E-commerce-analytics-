# Olist E-Commerce Analytics

End-to-end analysis of the Olist Brazilian E-Commerce dataset: SQL analysis, Python data preparation and an interactive Streamlit dashboard covering sales trends, product categories, delivery performance, customer reviews, payments and sellers.

**Live dashboard:** https://olist-e-commerce-analyst.streamlit.app/

## Business questions answered
- How many orders, customers and sellers are there, and how much revenue is generated?
- How do monthly sales and order volumes change over time?
- Which product categories drive the most revenue?
- How long do deliveries take, and which states have the most late deliveries?
- Do late deliveries lead to lower review scores?
- Which payment methods are most used?
- Who are the top sellers?

## Tools
Python, Pandas, MySQL, Streamlit, Altair (charts), Power BI (planned)

## Project structure
```
sql/            01_schema -> 09_kpi_analysis (MySQL queries)
app.py          Streamlit dashboard
prepare_data.py Cleans raw Olist data and builds summary tables
requirements.txt
```

## SQL files
| File | Purpose |
|------|---------|
| 01_schema.sql | Table creation |
| 02_data_quality_checks.sql | Nulls, duplicates, consistency checks |
| 03_business_analysis.sql | Core business questions |
| 04_customer_analysis.sql | Customer behaviour |
| 05_product_seller_analysis.sql | Products and sellers |
| 06_delivery_analysis.sql | Delivery time and delays |
| 07_payment_analysis.sql | Payment methods and values |
| 08_advanced_analysis.sql | Advanced queries |
| 09_kpi_analysis.sql | Headline KPIs |

## Data preparation (prepare_data.py)
- Removes duplicate orders and reviews
- Averages multiple reviews per order into one score
- Calculates delivery days and late-delivery flag (delivered after estimated date)
- Counts unique customers using `customer_unique_id`
- Trims the monthly trend to Jan 2017 - Aug 2018 (very few orders outside this range)

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
On first run the app downloads the dataset from Kaggle automatically
([Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)).

## Author
Aayush Sharma
