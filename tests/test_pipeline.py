from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pyfiles" / "my_scripts"))

from clean_data_v1 import build_summary_table, validate_inputs


class SalesPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sales = pd.DataFrame(
            [
                {"order_id": 1, "date": "2026-01-01", "customer_id": "C1", "category": "office", "units": 2, "unit_price": 10.0},
                {"order_id": 2, "date": "2026-01-02", "customer_id": "C2", "category": "hardware", "units": 1, "unit_price": 25.0},
            ]
        )
        self.customers = pd.DataFrame(
            [
                {"customer_id": "C1", "customer_name": "Alpha", "region": "North", "segment": "SMB"},
                {"customer_id": "C2", "customer_name": "Beta", "region": "South", "segment": "Enterprise"},
            ]
        )

    def test_valid_inputs_pass(self) -> None:
        self.assertEqual(validate_inputs(self.sales, self.customers)["status"], "PASS")

    def test_revenue_and_orders_reconcile(self) -> None:
        summary = build_summary_table(self.sales, self.customers)
        self.assertAlmostEqual(float(summary["total_revenue"].sum()), 45.0)
        self.assertEqual(int(summary["orders"].sum()), 2)
        self.assertAlmostEqual(float(summary["revenue_share_pct"].sum()), 100.0)

    def test_duplicate_order_fails_validation(self) -> None:
        duplicated = pd.concat([self.sales, self.sales.iloc[[0]]], ignore_index=True)
        result = validate_inputs(duplicated, self.customers)
        self.assertFalse(result["checks"]["order_ids_unique"])

    def test_unmatched_customer_is_detected(self) -> None:
        unmatched = self.sales.copy()
        unmatched.loc[0, "customer_id"] = "MISSING"
        result = validate_inputs(unmatched, self.customers)
        self.assertFalse(result["checks"]["all_customers_matched"])


if __name__ == "__main__":
    unittest.main()
