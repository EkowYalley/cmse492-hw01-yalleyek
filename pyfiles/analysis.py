"""Main analysis script for the starter repository.
Run with: python analysis.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

def resolve_project_root() -> Path:
    env_root = os.getenv("STARTER_REPO_ROOT") or os.getenv("PROJECT_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if candidate.exists():
            return candidate
    return Path(__file__).resolve().parent


def configure_paths(project_root: Path) -> None:
    extra_paths = [
        project_root / "my_scripts",
        project_root / "utility",
    ]
    for p in extra_paths:
        sys.path.insert(0, str(p))


def main() -> None:
    project_root = resolve_project_root()
    configure_paths(project_root)

    from clean_data_v1 import build_summary_table, load_inputs
    from file_stuff import ensure_folder, save_csv
    from plot_helpers import make_revenue_plot

    sales_path = project_root / "datafiles" / "sales_jan.csv"
    customers_path = project_root / "datafiles" / "customer_lookup.csv"

    sales_df, customer_df = load_inputs(sales_path, customers_path)
    summary = build_summary_table(sales_df, customer_df)

    output_dir = ensure_folder(project_root / "outputs")
    summary_path = output_dir / "summary_by_region.csv"
    plot_path = output_dir / "revenue_by_region.png"

    save_csv(summary, summary_path)
    make_revenue_plot(summary, plot_path)

    print("Analysis complete.")
    print(f"Rows in summary: {len(summary)}")
    print(f"Summary written to: {summary_path}")
    print(f"Plot written to: {plot_path}")


if __name__ == "__main__":
    main()
