import pandas as pd
from pathlib import Path

data_dir = Path("data")
files = sorted([p for p in data_dir.glob("*.csv")])
if not files:
    print("No CSV files found in ./data")
    raise SystemExit(1)

for f in files:
    print("="*80)
    print("FILE:", f.name)
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print("  ERROR reading file:", e)
        continue
    print("  rows:", len(df))
    print("  columns:", df.columns.tolist())
    print("  types:")
    print(df.dtypes.to_frame("dtype"))
    print("  sample rows:")
    print(df.head(3).to_string(index=False))
    print()
