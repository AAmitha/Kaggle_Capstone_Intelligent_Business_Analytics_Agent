"""Data Analyst Agent for performing statistical analysis."""

import google.generativeai as genai
import pandas as pd
from typing import Dict, Any, Optional

from ..tools.data_loader import DataLoaderTool
from ..tools.statistical import StatisticalAnalysisTool
from ..observability import get_logger, get_tracer, get_metrics_collector


class DataAnalystAgent:
    """Specialized agent for data analysis tasks."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Data Analyst Agent.
        
        Args:
            api_key: Gemini API key (if None, uses environment variable)
        """
        self.logger = get_logger("data_analyst_agent")
        self.tracer = get_tracer()
        self.metrics = get_metrics_collector()
        
        # Initialize tools
        self.data_loader = DataLoaderTool()
        self.statistical_tool = StatisticalAnalysisTool()
        
        # Initialize Gemini model
        if api_key:
            genai.configure(api_key=api_key)
        
        try:
            self.model = genai.GenerativeModel('gemini-pro')
            self.logger.info("Data Analyst Agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def analyze_data(self, data: pd.DataFrame, query: str) -> Dict[str, Any]:
        """
        Analyze data based on a natural language query.
        
        Args:
            data: DataFrame to analyze
            query: Natural language query about the data
            
        Returns:
            Analysis results
        """
        with self.tracer.span("data_analysis", {"query": query}):
            self.metrics.increment("data_analyst.analysis_requests")
            
            try:
                # Perform statistical analysis
                desc_result = self.statistical_tool.describe(data)
                
                # Generate insights using Gemini
                data_summary = f"Dataset shape: {data.shape}, Columns: {', '.join(data.columns.tolist())}"
                prompt = f"""
                You are a data analyst. Analyze the following data and answer the query.
                
                Data Summary: {data_summary}
                Statistical Summary: {desc_result.get('statistics', {})}
                
                Query: {query}
                
                Provide:
                1. Key findings
                2. Statistical insights
                3. Recommendations
                
                Be concise and data-driven.
                """
                
                response = self.model.generate_content(prompt)
                insights = response.text
                
                result = {
                    "success": True,
                    "query": query,
                    "insights": insights,
                    "statistics": desc_result.get("statistics", {}),
                    "data_shape": data.shape
                }
                
                self.metrics.increment("data_analyst.analysis_success")
                self.logger.info(f"Analysis completed for query: {query}")
                
                return result
                
            except Exception as e:
                self.logger.error(f"Analysis failed: {e}")
                self.metrics.increment("data_analyst.analysis_errors")
                return {
                    "success": False,
                    "error": str(e)
                }
    
    def identify_patterns(self, data: pd.DataFrame, columns: Optional[list] = None) -> Dict[str, Any]:
        """Identify patterns in the data."""
        with self.tracer.span("pattern_identification"):
            try:
                if columns:
                    analysis_data = data[columns]
                else:
                    analysis_data = data.select_dtypes(include=['number'])
                
                # Correlation analysis
                corr_result = self.statistical_tool.correlation(analysis_data)
                
                # Generate pattern insights
                prompt = f"""
                Analyze the following correlation matrix and identify patterns:
                
                {corr_result.get('correlation_matrix', {})}
                
                Identify:
                1. Strong correlations (positive or negative)
                2. Potential relationships
                3. Data patterns
                """
                
                response = self.model.generate_content(prompt)
                patterns = response.text
                
                return {
                    "success": True,
                    "patterns": patterns,
                    "correlations": corr_result.get("correlation_matrix", {})
                }
                
            except Exception as e:
                self.logger.error(f"Pattern identification failed: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }
    
    def compare_groups(self, data: pd.DataFrame, group_by: str, value_column: str) -> Dict[str, Any]:
        """Compare groups in the data."""
        with self.tracer.span("group_comparison", {"group_by": group_by}):
            try:
                result = self.statistical_tool.group_by_analysis(
                    data, group_by, value_column, "mean"
                )
                
                if result["success"]:
                    # Generate comparison insights
                    prompt = f"""
                    Compare the following groups:
                    
                    {result.get('results', {})}
                    
                    Provide:
                    1. Which group performs best/worst
                    2. Differences between groups
                    3. Recommendations
                    """
                    
                    response = self.model.generate_content(prompt)
                    comparison = response.text
                    
                    result["comparison_insights"] = comparison
                
                return result
                
            except Exception as e:
                self.logger.error(f"Group comparison failed: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }

