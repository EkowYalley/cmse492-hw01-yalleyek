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

    from clean_data_v1 import build_summary_table, load_inputs
    from file_stuff import ensure_folder, save_csv
    from plot_helpers import make_revenue_plot
    
    # NEW IMPORT: Importing a custom helper we will create
    # Or you can import seaborn directly here if you prefer
    import seaborn as sns
    import matplotlib.pyplot as plt

    sales_path = project_root  / "datafiles" / "sales_jan.csv"
    customers_path = project_root  /"datafiles" / "customer_lookup.csv"

    sales_df, customer_df = load_inputs(sales_path, customers_path)
    summary = build_summary_table(sales_df, customer_df)

    output_dir = ensure_folder(project_root / "outputs")
    summary_path = output_dir / "summary_by_region.csv"
    plot_path = output_dir / "revenue_by_region.png"
    
    # NEW OUTPUT PATH
    corr_plot_path = output_dir / "metric_correlations.png"

    save_csv(summary, summary_path)
    make_revenue_plot(summary, plot_path)

    # --- PERSONAL MODIFICATION START ---
    print("Generating correlation heatmap...")
    plt.figure(figsize=(10, 8))
    # Using Seaborn (the additional package)
    numeric_summary = summary.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_summary.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation of Metrics by Region")
    plt.savefig(corr_plot_path)
    plt.close()
    # --- PERSONAL MODIFICATION END ---

    print("Analysis complete.")
    print(f"Rows in summary: {len(summary)}")
    print(f"Summary written to: {summary_path}")
    print(f"Correlation plot written to: {corr_plot_path}") # New print statement

if __name__ == "__main__":
    main()