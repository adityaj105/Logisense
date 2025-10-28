from pathlib import Path
import pandas as pd
import difflib

EXPECTED_FILES = {
    "orders": "orders.csv",
    "delivery_performance": "delivery_performance.csv",
    "routes": "routes_distance.csv",
    "fleet": "vehicle_fleet.csv",
    "warehouse": "warehouse_inventory.csv",
    "feedback": "customer_feedback.csv",
    "costs": "cost_breakdown.csv",
}

EXPECTED_COLS = {
    "orders": ["order_id", "customer_id", "order_date", "carrier", "origin_warehouse_id", "destination", "route_id", "weight"],
    "delivery_performance": ["order_id", "status", "pickup_time", "delivery_time", "delay_minutes"],
    "routes": ["route_id", "origin", "destination", "distance"],
    "fleet": ["vehicle_id", "vehicle_type", "capacity", "age_years", "emission_class"],
    "warehouse": ["warehouse_id", "sku", "stock_qty", "reorder_level", "storage_cost_per_unit", "last_restock_date", "location"],
    "feedback": ["order_id", "rating", "comment", "feedback_date"],
    "costs": ["order_id", "cost_type", "amount"],
}

def _best_match(name, candidates):
    name = name.lower()
    candidates_lower = [c.lower() for c in candidates]
    matches = difflib.get_close_matches(name, candidates_lower, n=1, cutoff=0.6)
    return matches[0] if matches else None

def _map_columns(df, expected_cols):
    cols = list(df.columns)
    mapping = {}
    expected_low = [c.lower() for c in expected_cols]
    for c in cols:
        c_low = c.lower()
        if c_low in expected_low:
            mapping[c] = expected_cols[expected_low.index(c_low)]
            continue
        norm = c_low.replace(" ", "_").replace("-", "_")
        bm = _best_match(norm, expected_cols)
        if bm:
            mapping[c] = expected_cols[[ec.lower() for ec in expected_cols].index(bm)]
            continue
        if "warehouse" in c_low and "id" in c_low:
            mapping[c] = "warehouse_id"
            continue
        if any(k in c_low for k in ("stock", "units", "qty")):
            mapping[c] = "stock_qty"
            continue
        if "reorder" in c_low:
            mapping[c] = "reorder_level"
            continue
        if "restock" in c_low or "restocked" in c_low:
            mapping[c] = "last_restock_date"
            continue
        if ("product" in c_low and "category" in c_low) or ("sku" in c_low):
            mapping[c] = "sku"
            continue
        if "location" in c_low or "city" in c_low:
            mapping[c] = "location"
            continue
        if "distance" in c_low:
            mapping[c] = "distance"
            continue
        if "delay" in c_low or "delay_minutes" in c_low:
            mapping[c] = "delay_minutes"
            continue
        if "order" in c_low and "id" in c_low:
            mapping[c] = "order_id"
            continue
        mapping[c] = c_low.replace(" ", "_")
    return df.rename(columns=mapping)

def _read_csv_try(path: Path):
    try:
        return pd.read_csv(path)
    except Exception:
        try:
            return pd.read_csv(path, encoding="latin1")
        except Exception:
            return None

def load_all(data_dir: str):
    data_dir = Path(data_dir)
    datasets = {}
    for key, fname in EXPECTED_FILES.items():
        fpath = data_dir / fname
        if not fpath.exists():
            found = None
            for p in data_dir.glob("*.csv"):
                if key.lower() in p.name.lower():
                    found = p
                    break
            if found is None:
                datasets[key] = None
                continue
            fpath = found
        df = _read_csv_try(fpath)
        if df is None:
            datasets[key] = None
            continue
        expected = EXPECTED_COLS.get(key, [])
        df = _map_columns(df, expected)
        datasets[key] = df
    return datasets

def profile_df(df):
    return {
        "rows": len(df),
        "cols": df.columns.tolist(),
        "missing_perc": (df.isna().mean() * 100).round(2).to_dict(),
        "sample": df.head(5).to_dict(orient="records"),
    }
