#!/usr/bin/env python3
"""
evaluate.py

Unified evaluator for skill rating files.
Supports: CSV, JSON, YAML (auto-detect by extension).

CSV expected columns (case-insensitive):
  Skill, Category, Weight (%), Score (0-10)
JSON expected structure:
{
  "skill": "Python",
  "categories": [
    {"name": "Core Syntax & Semantics", "weight": 12, "score": 8},
    ...
  ]
}

Usage:
  python code/evaluate.py path/to/skill.json
  python code/evaluate.py path/to/skill.csv --output out.csv
  python code/evaluate.py path/to/skill.csv --normalize
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from typing import List, Dict, Tuple

# optional dependency: pandas for CSV convenience; fallback to csv module
try:
    import pandas as pd
except Exception:
    pd = None

# YAML support
try:
    import yaml  # pyyaml
except Exception:
    yaml = None


def read_json(path: str) -> Tuple[str, List[Dict]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    skill = data.get("skill") or data.get("name") or "UNKNOWN_SKILL"
    cats = data.get("categories") or data.get("items") or []
    # normalize keys
    norm = []
    for c in cats:
        norm.append({
            "category": c.get("name") or c.get("category") or "UNKNOWN",
            "weight": float(c.get("weight", 0)),
            "score": float(c.get("score", 0))
        })
    return skill, norm


def read_yaml(path: str) -> Tuple[str, List[Dict]]:
    if yaml is None:
        raise RuntimeError("pyyaml is required to read YAML files. Install with `pip install pyyaml`")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    skill = data.get("skill") or data.get("name") or "UNKNOWN_SKILL"
    cats = data.get("categories") or data.get("items") or []
    norm = []
    for c in cats:
        norm.append({
            "category": c.get("name") or c.get("category") or "UNKNOWN",
            "weight": float(c.get("weight", 0)),
            "score": float(c.get("score", 0))
        })
    return skill, norm


def read_csv(path: str) -> Tuple[str, List[Dict]]:
    # Prefer pandas if available because it handles headers robustly
    if pd is not None:
        df = pd.read_csv(path)
        # Normalize column names
        cols = {c.lower().strip(): c for c in df.columns}
        # Try to find skill name column (not mandatory)
        skill = df[cols.get("skill")] .iloc[0] if "skill" in cols else "UNKNOWN_SKILL"
        # Required category columns mapping
        # Accept variations: "category" or "name"
        cat_col = cols.get("category") or cols.get("name")
        weight_col = cols.get("weight (%)") or cols.get("weight") or cols.get("weight_percent") or cols.get("weight (%)".lower())
        score_col = cols.get("score (0-10)") or cols.get("score") or cols.get("rating")
        if cat_col is None or weight_col is None or score_col is None:
            # fallback to positional columns if header different
            expected = df.columns.tolist()
            # heuristic: assume columns order [Skill?, Category, Weight, Score, ...]
            if len(expected) >= 4:
                cat_col = expected[1]
                weight_col = expected[2]
                score_col = expected[3]
            else:
                raise ValueError("CSV must contain Category, Weight and Score columns (or follow template). Columns found: %s" % expected)
        cats = []
        for _, row in df.iterrows():
            cats.append({
                "category": str(row[cat_col]),
                "weight": float(row[weight_col]),
                "score": float(row[score_col])
            })
        return skill, cats
    else:
        # Basic csv reader fallback
        import csv
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            h = [c.strip().lower() for c in header]
            # find indices
            try:
                cat_i = h.index("category") if "category" in h else 1
                weight_i = h.index("weight (%)") if "weight (%)" in h else h.index("weight") if "weight" in h else 2
                score_i = h.index("score (0-10)") if "score (0-10)" in h else h.index("score") if "score" in h else 3
            except ValueError:
                raise ValueError("CSV header must include 'Category', 'Weight' and 'Score' columns.")
            cats = []
            skill = "UNKNOWN_SKILL"
            for row in reader:
                cats.append({
                    "category": row[cat_i],
                    "weight": float(row[weight_i]) if row[weight_i] else 0.0,
                    "score": float(row[score_i]) if row[score_i] else 0.0
                })
            return skill, cats


def validate_categories(cats: List[Dict]) -> None:
    for c in cats:
        if c["weight"] < 0 or c["score"] < 0:
            raise ValueError("Negative weight/score not allowed.")
        if c["score"] > 10:
            raise ValueError("Scores must be in 0-10 range.")


def compute_weighted_total(cats: List[Dict], normalize: bool = False) -> Tuple[float, List[Dict]]:
    total_weight = sum(c["weight"] for c in cats)
    if total_weight == 0:
        raise ValueError("Total weight is zero. Provide non-zero weights.")
    if normalize and total_weight != 100:
        # normalize weights proportionally to sum to 100
        for c in cats:
            c["orig_weight"] = c["weight"]
            c["weight"] = c["weight"] * 100.0 / total_weight
        total_weight = 100.0
    validate_categories(cats)
    weighted_sum = 0.0
    results = []
    for c in cats:
        wscore = c["score"] * c["weight"] / 100.0
        weighted_sum += wscore
        results.append({
            "category": c["category"],
            "weight": c["weight"],
            "score": c["score"],
            "weighted_score": round(wscore, 4)
        })
    # weighted_sum is on 0..10 scale (if scores 0-10 and weights sum to 100)
    return weighted_sum, results


def pretty_print(skill: str, cats: List[Dict], weighted_sum: float, results: List[Dict], total_weight: float, output_path: str = None):
    print("\nSkill:", skill)
    print("Total weight (sum of weights):", round(total_weight, 4))
    print("Weighted total (0-10):", round(weighted_sum, 4))
    final_rating = int(round(weighted_sum, 0))
    print("Final Rating (1-10):", max(1, final_rating))
    print("\nBreakdown:")
    print(f"{'Category':40s} {'Weight':>8s} {'Score':>8s} {'Weighted':>10s}")
    print("-" * 70)
    for r in results:
        print(f"{r['category'][:40]:40s} {r['weight']:8.2f} {r['score']:8.2f} {r['weighted_score']:10.4f}")
    if output_path:
        # write a JSON or CSV depending on extension
        out_ext = os.path.splitext(output_path)[1].lower()
        if out_ext in (".json",):
            out = {
                "skill": skill,
                "total_weight": total_weight,
                "weighted_total": round(weighted_sum, 4),
                "final_rating": max(1, final_rating),
                "breakdown": results
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(out, f, indent=2)
            print(f"\nSaved detailed result to {output_path}")
        else:
            # default to CSV
            try:
                import csv
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Category", "Weight", "Score", "Weighted Score"])
                    for r in results:
                        writer.writerow([r["category"], r["weight"], r["score"], r["weighted_score"]])
                    writer.writerow([])
                    writer.writerow(["TOTAL_WEIGHT", total_weight, "", round(weighted_sum, 4)])
                    writer.writerow(["FINAL_RATING", "", "", max(1, final_rating)])
                print(f"\nSaved detailed result to {output_path}")
            except Exception as e:
                print("Failed to save CSV:", e)


def main():
    p = argparse.ArgumentParser(description="Unified skill evaluator (CSV/JSON/YAML).")
    p.add_argument("input", help="Path to input file (.csv, .json, .yml/.yaml)")
    p.add_argument("--output", "-o", help="Optional output file path (csv or json).")
    p.add_argument("--normalize", action="store_true", help="Normalize weights to sum to 100 if they don't.")
    args = p.parse_args()

    path = args.input
    if not os.path.exists(path):
        print("Input file not found:", path)
        sys.exit(2)

    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".json":
            skill, cats = read_json(path)
        elif ext in (".yml", ".yaml"):
            skill, cats = read_yaml(path)
        elif ext == ".csv":
            skill, cats = read_csv(path)
        else:
            raise ValueError("Unsupported file type. Use .csv, .json, or .yml/.yaml")
    except Exception as e:
        print("Failed to read input:", e)
        sys.exit(3)

    if not cats:
        print("No categories found in input.")
        sys.exit(4)

    total_weight = sum(c["weight"] for c in cats)

    try:
        weighted_sum, results = compute_weighted_total(cats, normalize=args.normalize)
    except Exception as e:
        print("Error computing weighted total:", e)
        sys.exit(5)

    pretty_print(skill, cats, weighted_sum, results, total_weight, args.output)


if __name__ == "__main__":
    main()
