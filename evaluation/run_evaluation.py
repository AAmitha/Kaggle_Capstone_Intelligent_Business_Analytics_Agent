"""Simple evaluation harness for tool-level checks.

This script performs a non-Gemini evaluation using the StatisticalAnalysisTool
on the provided sample data. If `GEMINI_API_KEY` is set, it will also attempt
to run a lightweight end-to-end analyze call via the Coordinator (may incur
model calls).
"""

import os
import json
from pathlib import Path

import pandas as pd

from src.tools.statistical import StatisticalAnalysisTool


def run_tool_checks(data_path: str):
    print(f"Running tool-only checks on {data_path}")
    tool = StatisticalAnalysisTool()
    df = pd.read_csv(data_path)
    desc = tool.describe(df)
    print("Descriptive statistics keys:", list(desc.get("statistics", {}).keys()))
    return desc


def try_end_to_end(data_path: str):
    # Attempt a coordinator analyze if GEMINI_API_KEY is present
    try:
        from src.coordinator import CoordinatorAgent
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "Replacewith_key":
            print("GEMINI_API_KEY not set or placeholder — skipping model-driven evaluation.")
            return None

        coordinator = CoordinatorAgent(user_id="eval_user", api_key=api_key)
        result = coordinator.analyze("Analyze sample data and generate a brief report", data_file=data_path)
        print("Coordinator analyze returned success:", result.get("success"))
        return result
    except Exception as e:
        print("End-to-end evaluation failed:", e)
        return None


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    sample_data = repo_root / "data" / "sample_data.csv"
    if not sample_data.exists():
        print("sample_data.csv not found in data/ — ensure sample data is present")
        exit(1)

    # Tool-only checks
    desc = run_tool_checks(str(sample_data))
    with open(repo_root / "evaluation" / "tool_check_results.json", "w") as f:
        json.dump(desc, f, default=str, indent=2)

    # Attempt optional end-to-end (requires GEMINI_API_KEY)
    try_end_to_end(str(sample_data))
