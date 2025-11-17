"""Tool for loading and preprocessing data files."""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any


class DataLoaderTool:
    """Tool for loading CSV, JSON, and other data formats."""
    
    def __init__(self):
        self.name = "data_loader"
        self.description = "Loads and preprocesses data from CSV, JSON files"
    
    def load_csv(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            **kwargs: Additional pandas read_csv parameters
            
        Returns:
            Dictionary with data and metadata
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "data": None
                }
            
            df = pd.read_csv(file_path, **kwargs)
            
            return {
                "success": True,
                "data": df.to_dict('records'),
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "summary": {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def load_json(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with data and metadata
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "data": None
                }
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame if it's a list of dicts
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                df = pd.DataFrame(data)
                return {
                    "success": True,
                    "data": data,
                    "shape": df.shape,
                    "columns": df.columns.tolist() if hasattr(df, 'columns') else None,
                    "summary": {
                        "rows": len(data),
                        "type": "list"
                    }
                }
            
            return {
                "success": True,
                "data": data,
                "summary": {
                    "type": type(data).__name__
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def preprocess_data(self, data: pd.DataFrame, operations: list) -> Dict[str, Any]:
        """
        Apply preprocessing operations to data.
        
        Args:
            data: DataFrame to process
            operations: List of operations to apply
            
        Returns:
            Processed data and metadata
        """
        try:
            df = data.copy()
            applied_ops = []
            
            for op in operations:
                if op == "remove_duplicates":
                    df = df.drop_duplicates()
                    applied_ops.append("remove_duplicates")
                elif op == "fill_na":
                    df = df.fillna(0)
                    applied_ops.append("fill_na")
                elif op == "drop_na":
                    df = df.dropna()
                    applied_ops.append("drop_na")
            
            return {
                "success": True,
                "data": df.to_dict('records'),
                "shape": df.shape,
                "operations_applied": applied_ops
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool action."""
        if action == "load_csv":
            return self.load_csv(**kwargs)
        elif action == "load_json":
            return self.load_json(**kwargs)
        elif action == "preprocess":
            return self.preprocess_data(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }

