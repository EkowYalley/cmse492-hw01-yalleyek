# Regional Sales Reporting Pipeline

This project turns raw sales transactions and a customer lookup table into a validated regional-and-category reporting dataset and revenue chart. It demonstrates practical data cleaning, joins, aggregation, reconciliation, automated checks, and reproducible output generation.

## Workflow

```text
sales transactions ─┐
                    ├─ validate ─ join ─ aggregate ─ reconcile ─ report
customer lookup ────┘
```

The pipeline:

1. Loads transaction and customer CSV files.
2. Validates required columns, order IDs, dates, units, prices, and customer matches.
3. Calculates line-level revenue as `units × unit_price`.
4. Joins transactions to customer regions.
5. Aggregates units, revenue, unique orders, average order revenue, and revenue share by region and category.
6. Reconciles output revenue and order counts to the source.
7. Exports a reporting table, chart, and machine-readable validation report.

## Verified run

The included sample run completed successfully:

- Sales rows: **48**
- Customers: **12**
- Source revenue: **$7,816.00**
- Reconciled summary revenue: **$7,816.00**
- Summary rows: **12**
- Automated pipeline checks passed: **8 of 8**
- Unit tests passed: **4 of 4**

The sample data are small and supplied for demonstration, so the project proves the workflow and validation logic rather than production scale.

## Validation

The production run checks that:

- Required columns are present.
- Order IDs are unique.
- Dates parse successfully.
- Units are positive.
- Prices are nonnegative.
- Every transaction matches a customer.
- Summary revenue reconciles to source revenue.
- Summary order counts reconcile to unique source orders.

The unit tests also confirm that duplicate orders and unmatched customers are detected rather than silently accepted.

## Repository structure

```text
.
├── datafiles/
│   ├── sales_jan.csv
│   └── customer_lookup.csv
├── pyfiles/
│   ├── analysis.py
│   └── my_scripts/
│       ├── clean_data_v1.py
│       └── plot_helpers.py
├── tests/
│   └── test_pipeline.py
├── outputs/
│   ├── summary_by_region.csv
│   ├── revenue_by_region.png
│   └── validation_report.json
├── Dockerfile
└── requirements.txt
```

## Reproduce

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python pyfiles/analysis.py
.venv/Scripts/python -m unittest discover -s tests -v
```

On macOS or Linux, use `.venv/bin/python` instead of `.venv/Scripts/python`.

## Outputs

- `summary_by_region.csv` provides the reporting-ready table.
- `revenue_by_region.png` shows total revenue by region.
- `validation_report.json` provides auditable pass/fail checks and source-to-output totals.

## Limitations

- The included dataset is a small demonstration sample, not a production sales system.
- Revenue is calculated from the provided price and unit fields; discounts, returns, taxes, and shipping are not represented.
- The pipeline runs as a batch process and does not include orchestration, incremental loading, or a database destination.
- Region and customer attributes are treated as current values because no historical customer dimension is supplied.

Earlier exploratory materials remain recoverable in repository history; the current branch contains the validated portfolio pipeline.

## Skills demonstrated

Python, pandas, CSV ingestion, schema validation, data-quality checks, relational joins, aggregation, reconciliation, automated testing, Matplotlib, and reproducible reporting.
