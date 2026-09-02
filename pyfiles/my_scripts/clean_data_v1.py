from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_inputs(sales_path: Path, customers_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(customers_path)
    return sales, customers


def validate_inputs(sales_df: pd.DataFrame, customer_df: pd.DataFrame) -> dict:
    required_sales = {"order_id", "date", "customer_id", "category", "units", "unit_price"}
    required_customers = {"customer_id", "customer_name", "region", "segment"}
    missing_sales = sorted(required_sales.difference(sales_df.columns))
    missing_customers = sorted(required_customers.difference(customer_df.columns))
    if missing_sales or missing_customers:
        raise ValueError(
            f"Missing columns — sales: {missing_sales or 'none'}; "
            f"customers: {missing_customers or 'none'}"
        )

    parsed_dates = pd.to_datetime(sales_df["date"], errors="coerce")
    duplicate_orders = int(sales_df["order_id"].duplicated().sum())
    invalid_dates = int(parsed_dates.isna().sum())
    invalid_units = int((sales_df["units"] <= 0).sum())
    invalid_prices = int((sales_df["unit_price"] < 0).sum())
    unmatched_customers = int(
        (~sales_df["customer_id"].isin(customer_df["customer_id"])).sum()
    )
    checks = {
        "required_columns_present": True,
        "order_ids_unique": duplicate_orders == 0,
        "dates_parse": invalid_dates == 0,
        "units_positive": invalid_units == 0,
        "prices_nonnegative": invalid_prices == 0,
        "all_customers_matched": unmatched_customers == 0,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "evidence": {
            "sales_rows": int(len(sales_df)),
            "customer_rows": int(len(customer_df)),
            "duplicate_orders": duplicate_orders,
            "invalid_dates": invalid_dates,
            "invalid_units": invalid_units,
            "invalid_prices": invalid_prices,
            "unmatched_customers": unmatched_customers,
        },
    }


def build_summary_table(sales_df: pd.DataFrame, customer_df: pd.DataFrame) -> pd.DataFrame:
    data = sales_df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["revenue"] = data["units"] * data["unit_price"]

    merged = data.merge(customer_df, on="customer_id", how="left")
    merged["region"] = merged["region"].fillna("Unknown")

    summary = (
        merged.groupby(["region", "category"], as_index=False)
        .agg(total_units=("units", "sum"), total_revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .sort_values(["total_revenue", "region"], ascending=[False, True])
    )
    summary["avg_revenue_per_order"] = (summary["total_revenue"] / summary["orders"]).round(2)
    summary["total_revenue"] = summary["total_revenue"].round(2)
    summary["revenue_share_pct"] = (
        100 * summary["total_revenue"] / summary["total_revenue"].sum()
    ).round(2)
    return summary
