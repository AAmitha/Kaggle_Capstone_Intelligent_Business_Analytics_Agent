"""Helper utility functions."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def create_sample_data(output_path: str = "data/sample_data.csv", rows: int = 100) -> pd.DataFrame:
    """
    Create sample sales data for testing.
    
    Args:
        output_path: Path to save the sample data
        rows: Number of rows to generate
        
    Returns:
        Generated DataFrame
    """
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime.now() - timedelta(days=rows)
    dates = [start_date + timedelta(days=i) for i in range(rows)]
    
    # Generate sample data
    data = {
        "date": dates,
        "product": np.random.choice(["Product A", "Product B", "Product C", "Product D"], rows),
        "region": np.random.choice(["North", "South", "East", "West"], rows),
        "sales": np.random.uniform(1000, 10000, rows),
        "quantity": np.random.randint(10, 100, rows),
        "customer_id": np.random.randint(1000, 9999, rows)
    }
    
    df = pd.DataFrame(data)
    
    # Save to file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    return df


def format_output(result: dict, format_type: str = "console") -> str:
    """
    Format output for display.
    
    Args:
        result: Result dictionary
        format_type: Output format (console, json, markdown)
        
    Returns:
        Formatted string
    """
    if format_type == "json":
        import json
        return json.dumps(result, indent=2, default=str)
    
    elif format_type == "markdown":
        md = []
        if result.get("success"):
            md.append("## Analysis Results\n")
            if "analysis" in result:
                md.append("### Insights\n")
                md.append(result["analysis"].get("insights", ""))
            if "report" in result:
                md.append(f"\n### Report\n")
                md.append(f"Report saved to: {result['report'].get('filepath', 'N/A')}")
        else:
            md.append("## Error\n")
            md.append(result.get("error", "Unknown error"))
        return "\n".join(md)
    
    else:  # console
        output = []
        if result.get("success"):
            output.append("✓ Analysis completed successfully\n")
            if "analysis" in result:
                output.append("\nInsights:")
                output.append(result["analysis"].get("insights", ""))
            if "report" in result:
                output.append(f"\nReport: {result['report'].get('filepath', 'N/A')}")
        else:
            output.append("✗ Analysis failed")
            output.append(f"Error: {result.get('error', 'Unknown error')}")
        return "\n".join(output)

