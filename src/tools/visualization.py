"""Tool for generating visualizations."""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
import base64
import io


class VisualizationTool:
    """Tool for creating charts and visualizations."""
    
    def __init__(self, output_dir: str = "outputs/visualizations"):
        self.name = "visualization"
        self.description = "Generates charts and visualizations"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_line_chart(self, data: pd.DataFrame, x: str, y: str, title: str = "Line Chart", save_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a line chart."""
        try:
            fig = px.line(data, x=x, y=y, title=title)
            
            if save_path:
                full_path = self.output_dir / save_path
                fig.write_image(str(full_path))
            
            # Convert to base64 for embedding
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "type": "line_chart",
                "image_base64": img_base64,
                "save_path": str(save_path) if save_path else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_bar_chart(self, data: pd.DataFrame, x: str, y: str, title: str = "Bar Chart", save_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a bar chart."""
        try:
            fig = px.bar(data, x=x, y=y, title=title)
            
            if save_path:
                full_path = self.output_dir / save_path
                fig.write_image(str(full_path))
            
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "type": "bar_chart",
                "image_base64": img_base64,
                "save_path": str(save_path) if save_path else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_pie_chart(self, data: pd.Series, title: str = "Pie Chart", save_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a pie chart."""
        try:
            fig = px.pie(values=data.values, names=data.index, title=title)
            
            if save_path:
                full_path = self.output_dir / save_path
                fig.write_image(str(full_path))
            
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "type": "pie_chart",
                "image_base64": img_base64,
                "save_path": str(save_path) if save_path else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_scatter_plot(self, data: pd.DataFrame, x: str, y: str, title: str = "Scatter Plot", save_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a scatter plot."""
        try:
            fig = px.scatter(data, x=x, y=y, title=title)
            
            if save_path:
                full_path = self.output_dir / save_path
                fig.write_image(str(save_path))
            
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "type": "scatter_plot",
                "image_base64": img_base64,
                "save_path": str(save_path) if save_path else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a visualization action."""
        if action == "line_chart":
            return self.create_line_chart(**kwargs)
        elif action == "bar_chart":
            return self.create_bar_chart(**kwargs)
        elif action == "pie_chart":
            return self.create_pie_chart(**kwargs)
        elif action == "scatter_plot":
            return self.create_scatter_plot(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }

