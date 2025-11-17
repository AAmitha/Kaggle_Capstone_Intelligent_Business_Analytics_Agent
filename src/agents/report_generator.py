"""Report Generator Agent for creating comprehensive reports."""

import google.generativeai as genai
from typing import Dict, Any, List, Optional

from ..tools.report_formatter import ReportFormatterTool
from ..tools.visualization import VisualizationTool
from ..observability import get_logger, get_tracer, get_metrics_collector


class ReportGeneratorAgent:
    """Specialized agent for generating reports."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Report Generator Agent.
        
        Args:
            api_key: Gemini API key (if None, uses environment variable)
        """
        self.logger = get_logger("report_generator_agent")
        self.tracer = get_tracer()
        self.metrics = get_metrics_collector()
        
        # Initialize tools
        self.formatter = ReportFormatterTool()
        self.visualizer = VisualizationTool()
        
        # Initialize Gemini model
        if api_key:
            genai.configure(api_key=api_key)
        
        try:
            self.model = genai.GenerativeModel('gemini-pro')
            self.logger.info("Report Generator Agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def generate_report(
        self,
        title: str,
        analysis_results: Dict[str, Any],
        include_visualizations: bool = True,
        format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report from analysis results.
        
        Args:
            title: Report title
            analysis_results: Results from data analysis
            include_visualizations: Whether to include charts
            format: Output format (markdown or html)
            
        Returns:
            Generated report
        """
        with self.tracer.span("report_generation", {"title": title}):
            self.metrics.increment("report_generator.report_requests")
            
            try:
                sections = []
                
                # Executive Summary
                summary_prompt = f"""
                Create an executive summary for a business analytics report titled "{title}".
                
                Analysis Results:
                {analysis_results}
                
                Write a concise executive summary (2-3 paragraphs) highlighting key findings.
                """
                
                summary_response = self.model.generate_content(summary_prompt)
                sections.append({
                    "heading": "Executive Summary",
                    "content": summary_response.text,
                    "level": 2
                })
                
                # Key Findings
                if "insights" in analysis_results:
                    sections.append({
                        "heading": "Key Findings",
                        "content": analysis_results["insights"],
                        "level": 2
                    })
                
                # Statistical Analysis
                if "statistics" in analysis_results:
                    stats_content = self._format_statistics(analysis_results["statistics"])
                    sections.append({
                        "heading": "Statistical Analysis",
                        "content": stats_content,
                        "level": 2
                    })
                
                # Recommendations
                recommendations_prompt = f"""
                Based on the following analysis results, provide actionable business recommendations:
                
                {analysis_results}
                
                List 3-5 specific, actionable recommendations.
                """
                
                rec_response = self.model.generate_content(recommendations_prompt)
                sections.append({
                    "heading": "Recommendations",
                    "content": rec_response.text,
                    "level": 2
                })
                
                # Generate report
                report_result = self.formatter.create_report(
                    title=title,
                    sections=sections,
                    format=format,
                    save=True
                )
                
                self.metrics.increment("report_generator.report_success")
                self.logger.info(f"Report generated: {title}")
                
                return {
                    "success": True,
                    "report": report_result,
                    "sections": len(sections)
                }
                
            except Exception as e:
                self.logger.error(f"Report generation failed: {e}")
                self.metrics.increment("report_generator.report_errors")
                return {
                    "success": False,
                    "error": str(e)
                }
    
    def _format_statistics(self, statistics: Dict) -> str:
        """Format statistics dictionary into readable text."""
        formatted = []
        for col, stats in statistics.items():
            formatted.append(f"\n**{col}**:")
            for stat_name, value in stats.items():
                formatted.append(f"  - {stat_name}: {value:.2f}")
        return "\n".join(formatted)
    
    def create_visualization_report(
        self,
        data,
        visualizations: List[Dict[str, str]],
        title: str = "Visualization Report"
    ) -> Dict[str, Any]:
        """Create a report with embedded visualizations."""
        with self.tracer.span("visualization_report"):
            try:
                sections = [{
                    "heading": title,
                    "content": "This report contains data visualizations.",
                    "level": 1
                }]
                
                viz_results = []
                for viz_config in visualizations:
                    viz_type = viz_config.get("type")
                    if viz_type == "bar_chart":
                        result = self.visualizer.create_bar_chart(
                            data=data,
                            x=viz_config.get("x"),
                            y=viz_config.get("y"),
                            title=viz_config.get("title", "Chart")
                        )
                    elif viz_type == "line_chart":
                        result = self.visualizer.create_line_chart(
                            data=data,
                            x=viz_config.get("x"),
                            y=viz_config.get("y"),
                            title=viz_config.get("title", "Chart")
                        )
                    else:
                        continue
                    
                    if result.get("success"):
                        viz_results.append(result)
                        sections.append({
                            "heading": viz_config.get("title", "Chart"),
                            "content": f"![Chart](data:image/png;base64,{result.get('image_base64', '')})",
                            "level": 2
                        })
                
                report_result = self.formatter.create_report(
                    title=title,
                    sections=sections,
                    format="html",
                    save=True
                )
                
                return {
                    "success": True,
                    "report": report_result,
                    "visualizations": len(viz_results)
                }
                
            except Exception as e:
                self.logger.error(f"Visualization report failed: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }

