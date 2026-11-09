import unittest
from pathlib import Path
from src.affiliate_funnel_benchmark_engine import run_affiliate_funnel_pipeline


class TestAffiliateSampleFunnel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = Path(__file__).resolve().parent.parent
        cls.data_dir = cls.base.parent.parent / "data_cache"
        cls.out_dir = cls.base / "outputs"
        cls.summary = run_affiliate_funnel_pipeline(cls.data_dir, cls.out_dir)

    def test_01_record_count_and_hashes(self) -> None:
        self.assertEqual(self.summary["total_verified_records"], 109211)
        self.assertEqual(self.summary["cohorts_evaluated"], 15)

    def test_02_funnel_monotonicity_and_roas(self) -> None:
        ft = self.summary["funnel_totals"]
        self.assertGreaterEqual(ft["samples_dispatched"], ft["creator_videos_posted"])
        self.assertGreaterEqual(ft["creator_videos_posted"], ft["high_velocity_videos"])
        self.assertGreaterEqual(ft["high_velocity_videos"], ft["live_shopping_sessions"])
        self.assertGreaterEqual(ft["live_shopping_sessions"], ft["settled_orders"])
        self.assertAlmostEqual(ft["sample_to_post_rate_pct"], 86.06, places=2)
        self.assertAlmostEqual(ft["blended_gmv_max_roas"], 4.69, places=2)

    def test_03_benchmark_and_recommendations_generated(self) -> None:
        self.assertEqual(len(self.summary["top_client_recommendations"]), 6)
        self.assertTrue((self.out_dir / "affiliate_sample_funnel_benchmarks.csv").exists())


if __name__ == "__main__":
    unittest.main()
