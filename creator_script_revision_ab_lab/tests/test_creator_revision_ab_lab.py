#!/usr/bin/env python3
"""Unit tests for Creator Script Review & Hook Revision A/B Lab (P1 Module)."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

MOD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOD_ROOT / "src"))

from creator_revision_ab_lab import OUTPUTS_DIR, run_revision_lab  # noqa: E402


class TestCreatorRevisionAbLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.res = run_revision_lab()

    def test_record_conservation_and_integrity(self) -> None:
        self.assertEqual(self.res["total_verified_records"], 64176)
        self.assertEqual(self.res["instagram_creator_drafts"], 176)
        self.assertEqual(self.res["randomized_experiment_assignments"], 64000)
        self.assertEqual(self.res["sqlite_integrity_check"], "ok")

    def test_revision_rubric_explore_and_follow_lifts(self) -> None:
        self.assertGreater(self.res["explore_share_approved_pct"], self.res["explore_share_unrevised_pct"])
        self.assertGreater(self.res["impression_to_follow_rel_lift_pct"], 25.0)
        self.assertGreater(self.res["randomized_ab_visit_lift_pct"], 55.0)
        self.assertGreater(self.res["randomized_ab_conversion_lift_pct"], 85.0)

    def test_exported_artifacts(self) -> None:
        self.assertTrue((OUTPUTS_DIR / "creator_revision_validation.json").is_file())
        self.assertTrue((OUTPUTS_DIR / "creator_revision_rubric_scorecard.csv").is_file())


if __name__ == "__main__":
    unittest.main()
