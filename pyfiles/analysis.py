"""Main analysis script for the starter repository.
Run with: python analysis.py
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path

def resolve_project_root() -> Path:
    env_root = os.getenv("STARTER_REPO_ROOT") or os.getenv("PROJECT_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    
    # Check if we are inside 'pyfiles'. If so, the root is the parent.
    current_path = Path(__file__).resolve().parent
    if current_path.name == "pyfiles":
        return current_path.parent
    return current_path


def configure_paths(project_root: Path) -> None:
    extra_paths = [
        project_root / "pyfiles",           # Where analysis.py and helpers live
        project_root / "pyfiles" / "my_scripts",
        project_root / "utility",            # If you have a utility folder
    ]
    for p in extra_paths:
        if p.exists():
            sys.path.insert(0, str(p.resolve()))


def main() -> None:
    project_root = resolve_project_root()
    configure_paths(project_root)

    from clean_data_v1 import build_summary_table, load_inputs, validate_inputs
    from file_stuff import ensure_folder, save_csv
    from plot_helpers import make_revenue_plot
    
    sales_path = project_root  / "datafiles" / "sales_jan.csv"
    customers_path = project_root  /"datafiles" / "customer_lookup.csv"

    sales_df, customer_df = load_inputs(sales_path, customers_path)
    validation = validate_inputs(sales_df, customer_df)
    if validation["status"] != "PASS":
        raise ValueError(f"Input validation failed: {validation['checks']}")
    summary = build_summary_table(sales_df, customer_df)

    output_dir = ensure_folder(project_root / "outputs")
    summary_path = output_dir / "summary_by_region.csv"
    plot_path = output_dir / "revenue_by_region.png"
    
    save_csv(summary, summary_path)
    make_revenue_plot(summary, plot_path)

    source_revenue = float((sales_df["units"] * sales_df["unit_price"]).sum())
    summary_revenue = float(summary["total_revenue"].sum())
    validation["checks"]["summary_revenue_reconciles"] = abs(source_revenue - summary_revenue) < 0.01
    validation["checks"]["summary_order_count_reconciles"] = (
        int(summary["orders"].sum()) == int(sales_df["order_id"].nunique())
    )
    validation["evidence"]["source_revenue"] = round(source_revenue, 2)
    validation["evidence"]["summary_revenue"] = round(summary_revenue, 2)
    validation["evidence"]["summary_rows"] = int(len(summary))
    validation["status"] = "PASS" if all(validation["checks"].values()) else "FAIL"
    (output_dir / "validation_report.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )
    if validation["status"] != "PASS":
        raise ValueError(f"Output validation failed: {validation['checks']}")

    print("Analysis complete.")
    print(f"Rows in summary: {len(summary)}")
    print(f"Summary written to: {summary_path}")
    print(f"Validation report written to: {output_dir / 'validation_report.json'}")

if __name__ == "__main__":
    main()
