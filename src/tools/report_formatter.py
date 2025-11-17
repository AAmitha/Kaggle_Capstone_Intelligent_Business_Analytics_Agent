"""Tool for formatting reports in various formats."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class ReportFormatterTool:
    """Tool for formatting analysis results into reports."""
    
    def __init__(self, output_dir: str = "outputs/reports"):
        self.name = "report_formatter"
        self.description = "Formats analysis results into reports"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def format_markdown(self, title: str, sections: List[Dict[str, str]], metadata: Optional[Dict] = None) -> str:
        """
        Format content as markdown.
        
        Args:
            title: Report title
            sections: List of sections with 'heading' and 'content' keys
            metadata: Optional metadata
            
        Returns:
            Formatted markdown string
        """
        md = f"# {title}\n\n"
        
        if metadata:
            md += f"**Generated:** {metadata.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n"
        
        for section in sections:
            heading = section.get('heading', '')
            content = section.get('content', '')
            level = section.get('level', 2)
            
            md += f"{'#' * level} {heading}\n\n"
            md += f"{content}\n\n"
        
        return md
    
    def format_html(self, title: str, sections: List[Dict[str, str]], metadata: Optional[Dict] = None) -> str:
        """Format content as HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        .metadata {{ color: #888; font-size: 0.9em; }}
        .section {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
"""
        
        if metadata:
            timestamp = metadata.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            html += f'    <div class="metadata">Generated: {timestamp}</div>\n'
        
        for section in sections:
            heading = section.get('heading', '')
            content = section.get('content', '')
            level = section.get('level', 2)
            
            html += f'    <div class="section">\n'
            html += f'        <h{level}>{heading}</h{level}>\n'
            html += f'        <p>{content.replace(chr(10), "<br>")}</p>\n'
            html += f'    </div>\n'
        
        html += """</body>
</html>"""
        
        return html
    
    def save_report(self, content: str, filename: str, format: str = "markdown") -> Dict[str, Any]:
        """Save report to file."""
        try:
            if format == "markdown":
                filepath = self.output_dir / f"{filename}.md"
            elif format == "html":
                filepath = self.output_dir / f"{filename}.html"
            else:
                return {
                    "success": False,
                    "error": f"Unsupported format: {format}"
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "filepath": str(filepath),
                "format": format
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_report(self, title: str, sections: List[Dict[str, str]], format: str = "markdown", save: bool = True) -> Dict[str, Any]:
        """Create and optionally save a report."""
        metadata = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if format == "markdown":
            content = self.format_markdown(title, sections, metadata)
        elif format == "html":
            content = self.format_html(title, sections, metadata)
        else:
            return {
                "success": False,
                "error": f"Unsupported format: {format}"
            }
        
        result = {
            "success": True,
            "content": content,
            "format": format
        }
        
        if save:
            filename = title.lower().replace(" ", "_")
            save_result = self.save_report(content, filename, format)
            result["filepath"] = save_result.get("filepath")
        
        return result
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a formatting action."""
        if action == "format_markdown":
            return {"success": True, "content": self.format_markdown(**kwargs)}
        elif action == "format_html":
            return {"success": True, "content": self.format_html(**kwargs)}
        elif action == "create_report":
            return self.create_report(**kwargs)
        elif action == "save_report":
            return self.save_report(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }

