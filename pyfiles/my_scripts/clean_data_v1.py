from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_inputs(sales_path: Path, customers_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(customers_path)
    return sales, customers


def build_summary_table(sales_df: pd.DataFrame, customer_df: pd.DataFrame) -> pd.DataFrame:
    data = sales_df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["revenue"] = data["units"] * data["unit_price"]

    merged = data.merge(customer_df, on="customer_id", how="left")
    merged["region"] = merged["region"].fillna("Unknown")

    summary = (
        merged.groupby(["region", "category"], as_index=False)
        .agg(total_units=("units", "sum"), total_revenue=("revenue", "sum"), orders=("order_id", "count"))
        .sort_values(["total_revenue", "region"], ascending=[False, True])
    )
    summary["avg_revenue_per_order"] = (summary["total_revenue"] / summary["orders"]).round(2)
    summary["total_revenue"] = summary["total_revenue"].round(2)
    return summary
