#!/usr/bin/env python3
"""Unit tests for the SEO/GEO, Marketplace & Weekly/Monthly Readout P1 Module."""

import sys
import unittest
from pathlib import Path

MOD_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOD_DIR / "src"))

from seo_geo_marketplace_readout import run_readout_mart  # noqa: E402


class TestSeoGeoMarketplaceReadout(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = run_readout_mart()

    def test_all_eight_parity_gates_pass(self) -> None:
        self.assertEqual(self.summary["gates_passed"], 8)
        self.assertEqual(self.summary["gates_total"], 8)

    def test_record_count_and_discrepancy_governance(self) -> None:
        self.assertEqual(self.summary["combined_records"], 109211)
        self.assertEqual(self.summary["monthly_channel_cohorts"], 18)
        self.assertLess(self.summary["reconciled_tracking_discrepancy_pct"], 1.0)

    def test_exported_scorecard_exists(self) -> None:
        scorecard_path = MOD_DIR / "outputs" / "seo_geo_marketplace_scorecard.csv"
        self.assertTrue(scorecard_path.exists())
        self.assertGreater(scorecard_path.stat().st_size, 300)


if __name__ == "__main__":
    unittest.main(verbosity=2)
