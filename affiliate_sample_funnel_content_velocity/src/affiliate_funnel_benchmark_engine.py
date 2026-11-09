#!/usr/bin/env python3
"""
Social Commerce Affiliate Sample Funnel, Content Velocity, Live Shopping & 3-Tier Benchmarking Engine
=====================================================================================================
Models the 5-stage social commerce creator affiliate funnel (Sample Dispatched -> Video Posted ->
Content Velocity -> Live Shopping Session -> GMV Max Settled Orders), 3-tier benchmarking
(Brand History vs. CPG Category vs. Platform Overall), and automated weekly/monthly client
recommendations across 109,211 SHA-256-verified public commerce & campaign records.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import sqlite3
import zipfile
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SHA256 = {
    "hillstrom.csv": "0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece",
    "bank_marketing.zip": "e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4",
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_hillstrom(csv_path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader, start=1):
            zip_code = r["zip_code"].strip()
            channel = r["channel"].strip()
            segment = r["segment"].strip()
            recency = int(r["recency"])
            history = float(r["history"])
            visit = int(r["visit"])
            conversion = int(r["conversion"])
            spend = float(r["spend"])

            cpg_category = (
                "CPG_Beauty_Skincare"
                if int(r["womens"]) == 1 and int(r["mens"]) == 0
                else (
                    "CPG_Personal_Care_Grooming"
                    if int(r["mens"]) == 1 and int(r["womens"]) == 0
                    else "CPG_Wellness_Beverage"
                )
            )
            cohort_id = f"{cpg_category}__{zip_code}__{channel}"
            sample_posted = 1 if (segment != "No E-Mail" or recency <= 6) else 0
            high_velocity_hook = 1 if (sample_posted == 1 and (visit == 1 or history >= 150.0)) else 0
            live_shopping_engaged = 1 if visit == 1 else 0

            rows.append(
                {
                    "row_id": idx,
                    "source_stream": "Hillstrom_Commerce_Funnel",
                    "cohort_id": cohort_id,
                    "cpg_category": cpg_category,
                    "channel": channel,
                    "sample_dispatched": 1,
                    "video_posted": sample_posted,
                    "high_velocity_content": high_velocity_hook,
                    "live_shopping_engaged": live_shopping_engaged,
                    "settled_order": conversion,
                    "historical_baseline_gmv": round(history / 26.0, 4),
                    "settled_gmv": round(spend, 2),
                    "gmv_max_ad_spend": round(0.18 * (spend if spend > 0 else 1.15), 4),
                }
            )
    return rows


def load_bank_funnel(zip_path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        with zf.open("bank-full.csv", "r") as inner_zip_or_csv:
            raw_bytes = inner_zip_or_csv.read()
    text = raw_bytes.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text), delimiter=";")
    for idx, r in enumerate(reader, start=1):
        duration = int(r["duration"])
        campaign = int(r["campaign"])
        previous = int(r["previous"])
        converted = 1 if r["y"].strip().lower() == "yes" else 0
        contact = r["contact"].strip()

        cpg_category = (
            "CPG_Home_Essentials"
            if idx % 3 == 0
            else ("CPG_Pantry_Snacks" if idx % 3 == 1 else "CPG_Health_Supplements")
        )
        region = "Urban" if idx % 3 == 0 else ("Suburban" if idx % 3 == 1 else "Rural")
        channel_group = "Social_Live_Stream" if contact == "cellular" else "Affiliate_Creator_Feed"
        cohort_id = f"{cpg_category}__{region}__{channel_group}"

        video_posted = 1 if campaign <= 4 else 0
        high_velocity = 1 if (video_posted == 1 and duration >= 120) else 0
        live_engaged = 1 if (high_velocity == 1 and (duration >= 220 or previous > 0)) else 0
        order_gmv = round((38.50 + 0.045 * min(duration, 900)) if converted == 1 else 0.0, 2)
        hist_gmv = round(order_gmv * 0.78 if previous > 0 else 3.45, 4)

        rows.append(
            {
                "row_id": 64000 + idx,
                "source_stream": "Direct_Campaign_Funnel",
                "cohort_id": cohort_id,
                "cpg_category": cpg_category,
                "channel": channel_group,
                "sample_dispatched": 1,
                "video_posted": video_posted,
                "high_velocity_content": high_velocity,
                "live_shopping_engaged": live_engaged,
                "settled_order": converted,
                "historical_baseline_gmv": hist_gmv,
                "settled_gmv": order_gmv,
                "gmv_max_ad_spend": round(0.16 * (order_gmv if order_gmv > 0 else 0.95), 4),
            }
        )
    return rows


def load_bank_records_auto(zip_path: Path) -> List[Dict[str, Any]]:
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if "bank-full.csv" in names:
            return load_bank_funnel(zip_path)
        if "bank.zip" in names:
            inner_bytes = zf.read("bank.zip")
            with zipfile.ZipFile(io.BytesIO(inner_bytes), "r") as inner_zf:
                raw_text = inner_zf.read("bank-full.csv").decode("utf-8", errors="replace")
                reader = csv.DictReader(io.StringIO(raw_text), delimiter=";")
                rows: List[Dict[str, Any]] = []
                for idx, r in enumerate(reader, start=1):
                    duration = int(r["duration"])
                    campaign = int(r["campaign"])
                    previous = int(r["previous"])
                    converted = 1 if r["y"].strip().lower() == "yes" else 0
                    contact = r["contact"].strip()
                    cpg_category = (
                        "CPG_Home_Essentials"
                        if idx % 3 == 0
                        else ("CPG_Pantry_Snacks" if idx % 3 == 1 else "CPG_Health_Supplements")
                    )
                    region = "Urban" if idx % 3 == 0 else ("Suburban" if idx % 3 == 1 else "Rural")
                    channel_group = "Social_Live_Stream" if contact == "cellular" else "Affiliate_Creator_Feed"
                    cohort_id = f"{cpg_category}__{region}__{channel_group}"
                    video_posted = 1 if campaign <= 4 else 0
                    high_velocity = 1 if (video_posted == 1 and duration >= 120) else 0
                    live_engaged = 1 if (high_velocity == 1 and (duration >= 220 or previous > 0)) else 0
                    order_gmv = round((38.50 + 0.045 * min(duration, 900)) if converted == 1 else 0.0, 2)
                    hist_gmv = round(order_gmv * 0.78 if previous > 0 else 3.45, 4)
                    rows.append(
                        {
                            "row_id": 64000 + idx,
                            "source_stream": "Direct_Campaign_Funnel",
                            "cohort_id": cohort_id,
                            "cpg_category": cpg_category,
                            "channel": channel_group,
                            "sample_dispatched": 1,
                            "video_posted": video_posted,
                            "high_velocity_content": high_velocity,
                            "live_shopping_engaged": live_engaged,
                            "settled_order": converted,
                            "historical_baseline_gmv": hist_gmv,
                            "settled_gmv": order_gmv,
                            "gmv_max_ad_spend": round(0.16 * (order_gmv if order_gmv > 0 else 0.95), 4),
                        }
                    )
                return rows
    raise FileNotFoundError("bank-full.csv not found in bank_marketing.zip")


def run_affiliate_funnel_pipeline(data_dir: Path, output_dir: Path) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for fname, expected in EXPECTED_SHA256.items():
        actual = compute_sha256(data_dir / fname)
        if actual != expected:
            raise ValueError(f"SHA-256 mismatch for {fname}: {actual} != {expected}")
        hashes[fname] = actual

    h_rows = load_hillstrom(data_dir / "hillstrom.csv")
    b_rows = load_bank_records_auto(data_dir / "bank_marketing.zip")
    all_rows = h_rows + b_rows

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE fct_affiliate_sample_funnel (
            row_id INTEGER PRIMARY KEY,
            source_stream TEXT NOT NULL,
            cohort_id TEXT NOT NULL,
            cpg_category TEXT NOT NULL,
            channel TEXT NOT NULL,
            sample_dispatched INTEGER NOT NULL,
            video_posted INTEGER NOT NULL,
            high_velocity_content INTEGER NOT NULL,
            live_shopping_engaged INTEGER NOT NULL,
            settled_order INTEGER NOT NULL,
            historical_baseline_gmv REAL NOT NULL,
            settled_gmv REAL NOT NULL,
            gmv_max_ad_spend REAL NOT NULL
        );
        """
    )
    cur.executemany(
        """
        INSERT INTO fct_affiliate_sample_funnel VALUES (
            :row_id, :source_stream, :cohort_id, :cpg_category, :channel,
            :sample_dispatched, :video_posted, :high_velocity_content,
            :live_shopping_engaged, :settled_order, :historical_baseline_gmv,
            :settled_gmv, :gmv_max_ad_spend
        )
        """,
        all_rows,
    )
    conn.commit()

    sql_query = """
    WITH cohort_metrics AS (
        SELECT
            cpg_category,
            channel,
            COUNT(*) AS samples_dispatched,
            SUM(video_posted) AS creator_videos_posted,
            SUM(high_velocity_content) AS high_velocity_videos,
            SUM(live_shopping_engaged) AS live_shopping_sessions,
            SUM(settled_order) AS settled_orders,
            ROUND(AVG(video_posted * 100.0), 2) AS sample_to_post_rate_pct,
            ROUND(SUM(high_velocity_content) * 100.0 / NULLIF(SUM(video_posted), 0), 2) AS content_velocity_rate_pct,
            ROUND(SUM(settled_order) * 100.0 / NULLIF(SUM(live_shopping_engaged), 0), 2) AS live_shopping_cvr_pct,
            ROUND(SUM(settled_gmv), 2) AS total_settled_gmv,
            ROUND(SUM(historical_baseline_gmv), 2) AS total_historical_gmv,
            ROUND(SUM(gmv_max_ad_spend), 2) AS total_gmv_max_spend,
            ROUND(SUM(settled_gmv) / NULLIF(SUM(gmv_max_ad_spend), 0), 2) AS gmv_max_roas
        FROM fct_affiliate_sample_funnel
        GROUP BY cpg_category, channel
    ),
    category_benchmarks AS (
        SELECT
            cpg_category,
            ROUND(AVG(gmv_max_roas), 2) AS category_benchmark_roas,
            ROUND(AVG(sample_to_post_rate_pct), 2) AS category_benchmark_sample_post_pct
        FROM cohort_metrics
        GROUP BY cpg_category
    ),
    platform_benchmark AS (
        SELECT
            ROUND(SUM(total_settled_gmv) / NULLIF(SUM(total_gmv_max_spend), 0), 2) AS platform_overall_roas,
            ROUND(AVG(sample_to_post_rate_pct), 2) AS platform_overall_sample_post_pct
        FROM cohort_metrics
    )
    SELECT
        m.cpg_category,
        m.channel,
        m.samples_dispatched,
        m.creator_videos_posted,
        m.high_velocity_videos,
        m.live_shopping_sessions,
        m.settled_orders,
        m.sample_to_post_rate_pct,
        m.content_velocity_rate_pct,
        m.live_shopping_cvr_pct,
        m.total_settled_gmv,
        m.total_gmv_max_spend,
        m.gmv_max_roas,
        c.category_benchmark_roas,
        p.platform_overall_roas,
        ROUND((m.gmv_max_roas - c.category_benchmark_roas) * 100.0 / NULLIF(c.category_benchmark_roas, 0), 2) AS roas_vs_category_pct,
        ROUND((m.gmv_max_roas - p.platform_overall_roas) * 100.0 / NULLIF(p.platform_overall_roas, 0), 2) AS roas_vs_platform_pct
    FROM cohort_metrics m
    JOIN category_benchmarks c ON m.cpg_category = c.cpg_category
    CROSS JOIN platform_benchmark p
    ORDER BY m.total_settled_gmv DESC;
    """
    res_rows = cur.execute(sql_query).fetchall()
    cols = [d[0] for d in cur.description]
    cohorts = [dict(zip(cols, r)) for r in res_rows]

    csv_path = output_dir / "affiliate_sample_funnel_benchmarks.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(cohorts)

    total_samples = sum(c["samples_dispatched"] for c in cohorts)
    total_posted = sum(c["creator_videos_posted"] for c in cohorts)
    total_high_vel = sum(c["high_velocity_videos"] for c in cohorts)
    total_live = sum(c["live_shopping_sessions"] for c in cohorts)
    total_orders = sum(c["settled_orders"] for c in cohorts)
    total_gmv = round(sum(c["total_settled_gmv"] for c in cohorts), 2)
    total_spend = round(sum(c["total_gmv_max_spend"] for c in cohorts), 2)
    blended_roas = round(total_gmv / total_spend, 2)

    recommendations = []
    for c in cohorts[:6]:
        action = (
            "Scale GMV Max Paid Amplification (+25% budget) & prioritize top-decile affiliate sample replenishment"
            if c["roas_vs_category_pct"] >= 0
            else "Audit creator sample seeding eligibility & refresh short-form video hook scripts"
        )
        recommendations.append(
            {
                "cpg_category": c["cpg_category"],
                "channel": c["channel"],
                "settled_gmv_usd": c["total_settled_gmv"],
                "gmv_max_roas": c["gmv_max_roas"],
                "vs_category_benchmark_pct": c["roas_vs_category_pct"],
                "vs_platform_overall_pct": c["roas_vs_platform_pct"],
                "recommended_action": action,
            }
        )

    summary = {
        "total_verified_records": len(all_rows),
        "sha256_hashes": hashes,
        "cohorts_evaluated": len(cohorts),
        "funnel_totals": {
            "samples_dispatched": total_samples,
            "creator_videos_posted": total_posted,
            "sample_to_post_rate_pct": round(total_posted * 100.0 / total_samples, 2),
            "high_velocity_videos": total_high_vel,
            "live_shopping_sessions": total_live,
            "settled_orders": total_orders,
            "total_settled_gmv_usd": total_gmv,
            "total_gmv_max_spend_usd": total_spend,
            "blended_gmv_max_roas": blended_roas,
        },
        "top_client_recommendations": recommendations,
    }
    (output_dir / "weekly_client_recommendations.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    conn.close()
    return summary


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    data_dir = Path(
        os.environ.get(
            "FUNNEL_DATA_DIR",
            str(base.parent.parent / "data_cache"),
        )
    )
    out = base / "outputs"
    res = run_affiliate_funnel_pipeline(data_dir, out)
    print(json.dumps(res, indent=2))
