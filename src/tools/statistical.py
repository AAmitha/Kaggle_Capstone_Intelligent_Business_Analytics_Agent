"""Tool for performing statistical analysis."""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional


class StatisticalAnalysisTool:
    """Tool for performing statistical computations and analysis."""
    
    def __init__(self):
        self.name = "statistical_analysis"
        self.description = "Performs statistical analysis on data"
    
    def describe(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate descriptive statistics."""
        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            desc = data[numeric_cols].describe()
            
            return {
                "success": True,
                "statistics": desc.to_dict(),
                "summary": {
                    "numeric_columns": numeric_cols.tolist(),
                    "total_columns": len(data.columns),
                    "total_rows": len(data)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def correlation(self, data: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Calculate correlation matrix."""
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            if columns:
                numeric_data = numeric_data[columns]
            
            corr_matrix = numeric_data.corr()
            
            return {
                "success": True,
                "correlation_matrix": corr_matrix.to_dict(),
                "columns": corr_matrix.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def trend_analysis(self, data: pd.DataFrame, date_column: str, value_column: str) -> Dict[str, Any]:
        """Analyze trends over time."""
        try:
            if date_column not in data.columns or value_column not in data.columns:
                return {
                    "success": False,
                    "error": "Required columns not found"
                }
            
            # Convert date column if needed
            data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
            data = data.dropna(subset=[date_column, value_column])
            data = data.sort_values(date_column)
            
            # Calculate trend
            values = data[value_column].values
            x = np.arange(len(values))
            slope = np.polyfit(x, values, 1)[0]
            
            # Calculate percentage change
            if len(values) > 1:
                pct_change = ((values[-1] - values[0]) / values[0]) * 100
            else:
                pct_change = 0
            
            return {
                "success": True,
                "trend": "increasing" if slope > 0 else "decreasing",
                "slope": float(slope),
                "percentage_change": float(pct_change),
                "first_value": float(values[0]) if len(values) > 0 else None,
                "last_value": float(values[-1]) if len(values) > 0 else None,
                "data_points": len(values)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def group_by_analysis(self, data: pd.DataFrame, group_by: str, agg_column: str, agg_func: str = "sum") -> Dict[str, Any]:
        """Perform group by analysis."""
        try:
            if group_by not in data.columns or agg_column not in data.columns:
                return {
                    "success": False,
                    "error": "Required columns not found"
                }
            
            agg_func_map = {
                "sum": "sum",
                "mean": "mean",
                "count": "count",
                "max": "max",
                "min": "min"
            }
            
            func = agg_func_map.get(agg_func.lower(), "sum")
            grouped = data.groupby(group_by)[agg_column].agg(func)
            
            return {
                "success": True,
                "results": grouped.to_dict(),
                "group_by": group_by,
                "aggregation": agg_func
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a statistical analysis action."""
        if action == "describe":
            return self.describe(**kwargs)
        elif action == "correlation":
            return self.correlation(**kwargs)
        elif action == "trend_analysis":
            return self.trend_analysis(**kwargs)
        elif action == "group_by":
            return self.group_by_analysis(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }

