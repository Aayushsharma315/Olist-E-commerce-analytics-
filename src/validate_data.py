import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

def validate_csv(file_path):
try:
df = pd.read_csv(file_path)

```
    print(f"\nFile: {file_path.name}")
    print("-" * 35)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Duplicate rows:", df.duplicated().sum())
    print("Missing values:", df.isnull().sum().sum())

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        print("\nMissing values by column:")
        print(missing)

except Exception as error:
    print(f"Error reading {file_path.name}: {error}")
```

def main():
if not DATA_DIR.exists():
print("Data folder not found:", DATA_DIR)
print("Please add the dataset CSV files to data/raw/")
return

```
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("No CSV files found in data/raw/")
    return

print("Olist E-Commerce Data Validation")
print("=" * 35)

for file_path in csv_files:
    validate_csv(file_path)
```

if **name** == "**main**":
main()
