"""Coordinator Agent that orchestrates the multi-agent system."""

import os
import google.generativeai as genai
import pandas as pd
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

from .agents.data_analyst import DataAnalystAgent
from .agents.report_generator import ReportGeneratorAgent
from .tools.data_loader import DataLoaderTool
from .memory.session_manager import SessionManager, Session
from .memory.memory_bank import MemoryBank
from .observability import (
    setup_logger,
    get_logger,
    get_tracer,
    get_metrics_collector
)

# Load environment variables
load_dotenv()


class CoordinatorAgent:
    """
    Main coordinator agent that orchestrates the multi-agent system.
    
    This agent:
    - Manages workflow and delegates tasks
    - Coordinates between specialized agents
    - Maintains session state
    - Integrates with memory system
    """
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Coordinator Agent.
        
        Args:
            session_id: Existing session ID (creates new if None)
            user_id: User identifier
            api_key: Gemini API key (uses env var if None)
        """
        # Setup observability
        self.logger = setup_logger("coordinator_agent")
        self.tracer = get_tracer()
        self.metrics = get_metrics_collector()
        
        # Get API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize session management
        self.session_manager = SessionManager()
        if session_id:
            self.session = self.session_manager.get_session(session_id)
            if not self.session:
                raise ValueError(f"Session {session_id} not found")
        else:
            self.session = self.session_manager.create_session(
                user_id or "default_user"
            )
        
        # Initialize memory bank
        self.memory_bank = MemoryBank()
        
        # Initialize specialized agents
        self.data_analyst = DataAnalystAgent(api_key=self.api_key)
        self.report_generator = ReportGeneratorAgent(api_key=self.api_key)
        
        # Initialize tools
        self.data_loader = DataLoaderTool()
        
        # Initialize Gemini model for coordination
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.logger.info(f"Coordinator Agent initialized with session {self.session.id}")
        self.metrics.increment("coordinator.initializations")
    
    def analyze(self, query: str, data_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point for analysis requests.
        
        This method:
        1. Understands the user query
        2. Loads data if needed
        3. Delegates to appropriate agents
        4. Generates comprehensive report
        5. Stores insights in memory
        
        Args:
            query: Natural language query
            data_file: Optional path to data file
            
        Returns:
            Complete analysis results
        """
        with self.tracer.span("coordinator.analyze", {"query": query}):
            self.metrics.increment("coordinator.analysis_requests")
            start_time = pd.Timestamp.now()
            
            try:
                # Update session with user query
                self.session_manager.update_session(
                    self.session.id,
                    "user",
                    query
                )
                
                # Step 1: Understand query and plan workflow
                workflow = self._plan_workflow(query, data_file)
                self.logger.info(f"Workflow planned: {workflow}")
                
                # Step 2: Load data if needed
                data = None
                if data_file or workflow.get("needs_data"):
                    data = self._load_data(data_file or workflow.get("data_file"))
                    if data is None:
                        return {
                            "success": False,
                            "error": "Failed to load data"
                        }
                
                # Step 3: Perform analysis using Data Analyst Agent
                analysis_results = {}
                if workflow.get("perform_analysis"):
                    self.logger.info("Delegating to Data Analyst Agent")
                    analysis_results = self.data_analyst.analyze_data(data, query)
                    
                    # Store insights in memory
                    if analysis_results.get("success") and "insights" in analysis_results:
                        self.memory_bank.store_insight(
                            analysis_results["insights"],
                            metadata={
                                "query": query,
                                "session_id": self.session.id
                            }
                        )
                
                # Step 4: Generate report using Report Generator Agent
                report_results = {}
                if workflow.get("generate_report"):
                    self.logger.info("Delegating to Report Generator Agent")
                    report_title = workflow.get("report_title", "Business Analytics Report")
                    report_results = self.report_generator.generate_report(
                        title=report_title,
                        analysis_results=analysis_results,
                        format="markdown"
                    )
                
                # Step 5: Compile final response
                response = self._compile_response(
                    query,
                    analysis_results,
                    report_results,
                    workflow
                )
                
                # Update session with response
                self.session_manager.update_session(
                    self.session.id,
                    "assistant",
                    str(response)
                )
                
                # Record metrics
                duration = (pd.Timestamp.now() - start_time).total_seconds()
                self.metrics.record_timing("coordinator.analysis_duration", duration)
                self.metrics.increment("coordinator.analysis_success")
                
                self.logger.info(f"Analysis completed in {duration:.2f}s")
                
                return response
                
            except Exception as e:
                self.logger.error(f"Analysis failed: {e}", exc_info=True)
                self.metrics.increment("coordinator.analysis_errors")
                return {
                    "success": False,
                    "error": str(e)
                }
    
    def _plan_workflow(self, query: str, data_file: Optional[str] = None) -> Dict[str, Any]:
        """Plan the workflow based on the query."""
        prompt = f"""
        Analyze this query and determine the workflow:
        Query: {query}
        Data file: {data_file or "Not specified"}
        
        Determine:
        1. Does this need data loading? (needs_data: true/false)
        2. Does this need statistical analysis? (perform_analysis: true/false)
        3. Does this need a report? (generate_report: true/false)
        4. What should the report title be? (report_title: string)
        
        Respond in a structured format that can be parsed.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple parsing - in production, use structured output
            workflow = {
                "needs_data": data_file is not None or "data" in query.lower(),
                "perform_analysis": True,
                "generate_report": "report" in query.lower() or "analyze" in query.lower(),
                "report_title": "Business Analytics Report"
            }
            return workflow
        except Exception as e:
            self.logger.warning(f"Workflow planning failed, using defaults: {e}")
            return {
                "needs_data": data_file is not None,
                "perform_analysis": True,
                "generate_report": True,
                "report_title": "Business Analytics Report"
            }
    
    def _load_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load data from file."""
        with self.tracer.span("data_loading", {"file": file_path}):
            try:
                if file_path.endswith('.csv'):
                    result = self.data_loader.load_csv(file_path)
                elif file_path.endswith('.json'):
                    result = self.data_loader.load_json(file_path)
                else:
                    self.logger.error(f"Unsupported file format: {file_path}")
                    return None
                
                if result.get("success"):
                    data = pd.DataFrame(result["data"])
                    self.logger.info(f"Data loaded: {data.shape}")
                    return data
                else:
                    self.logger.error(f"Data loading failed: {result.get('error')}")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Data loading error: {e}")
                return None
    
    def _compile_response(
        self,
        query: str,
        analysis_results: Dict[str, Any],
        report_results: Dict[str, Any],
        workflow: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile final response from all agent outputs."""
        response = {
            "success": True,
            "query": query,
            "session_id": self.session.id,
            "workflow": workflow
        }
        
        if analysis_results.get("success"):
            response["analysis"] = {
                "insights": analysis_results.get("insights"),
                "statistics": analysis_results.get("statistics")
            }
        
        if report_results.get("success"):
            response["report"] = {
                "filepath": report_results.get("report", {}).get("filepath"),
                "format": report_results.get("report", {}).get("format")
            }
        
        # Add trace summary
        trace_summary = self.tracer.get_trace_summary()
        response["trace"] = trace_summary
        
        # Add metrics summary
        metrics_summary = self.metrics.get_summary()
        response["metrics"] = metrics_summary
        
        return response
    
    def get_session_context(self) -> Dict[str, Any]:
        """Get current session context."""
        return {
            "session_id": self.session.id,
            "user_id": self.session.user_id,
            "message_count": len(self.session.messages),
            "context": self.session.get_context()
        }
    
    def get_memory_insights(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve recent insights from memory bank."""
        insights = self.memory_bank.search(category="insight")
        return [
            {
                "key": entry.key,
                "value": entry.value,
                "timestamp": entry.timestamp.isoformat()
            }
            for entry in insights[-limit:]
        ]

