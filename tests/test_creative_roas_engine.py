#!/usr/bin/env python3
import json
import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
from creative_roas_testing_engine import run_engine, HILLSTROM_SHA256, UCI_BANK_SHA256


class TestCreativeRoasEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = run_engine()

    def test_01_public_dataset_provenance_and_row_counts(self):
        self.assertEqual(self.summary["hillstrom_records"], 64000)
        self.assertEqual(self.summary["uci_bank_records"], 45211)
        self.assertEqual(self.summary["total_public_records_audited"], 109211)
        self.assertEqual(self.summary["hillstrom_sha256"], HILLSTROM_SHA256)
        self.assertEqual(self.summary["uci_bank_sha256"], UCI_BANK_SHA256)

    def test_02_sqlite_integrity_and_24_cell_matrix(self):
        self.assertEqual(self.summary["sqlite_integrity_check"], "ok")
        self.assertEqual(self.summary["structured_test_cells_count"], 24)
        self.assertEqual(self.summary["sql_cte_rows_returned"], 24)

    def test_03_ab_testing_statistical_significance(self):
        ab = self.summary["ab_testing_results"]
        self.assertGreater(ab["pooled_visit_lift"]["rel_lift_pct"], 50.0)
        self.assertGreater(ab["pooled_conversion_lift"]["rel_lift_pct"], 80.0)
        self.assertLess(ab["mens_email_conversion_lift"]["p_value"], 1e-10)

    def test_04_creative_fatigue_and_thumb_stop_diagnostics(self):
        cf = self.summary["creative_fatigue_diagnostics"]
        self.assertGreater(cf["high_freq_fatigue_cvr_drop_pct"], 30.0)
        self.assertGreater(cf["thumb_stop_rate_lift_pct"], 20.0)
        self.assertGreater(cf["ctr_lift_pct"], 15.0)

    def test_05_marginal_roas_and_pixel_discrepancy_remediation(self):
        bp = self.summary["budget_pacing_and_roas_optimization"]
        tp = self.summary["tracking_pixel_utm_governance"]
        self.assertGreater(bp["roas_lift_pct"], 15.0)
        self.assertGreater(bp["cpa_reduction_pct"], 12.0)
        self.assertLess(tp["post_remediation_discrepancy_pct"], 1.5)
        self.assertGreater(tp["discrepancy_reduction_pct"], 85.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
