"""Tests for custom tools."""

import pytest
import pandas as pd
from src.tools.data_loader import DataLoaderTool
from src.tools.statistical import StatisticalAnalysisTool


def test_data_loader():
    """Test data loader tool."""
    loader = DataLoaderTool()
    
    # Test with invalid file
    result = loader.load_csv("nonexistent.csv")
    assert result["success"] is False


def test_statistical_tool():
    """Test statistical analysis tool."""
    tool = StatisticalAnalysisTool()
    
    # Create sample data
    data = pd.DataFrame({
        "value": [1, 2, 3, 4, 5],
        "category": ["A", "B", "A", "B", "A"]
    })
    
    result = tool.describe(data)
    assert result["success"] is True
    assert "statistics" in result

