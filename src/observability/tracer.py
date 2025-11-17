"""Execution tracing for agent workflows."""

import time
from contextlib import contextmanager
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TraceSpan:
    """Represents a single trace span."""
    name: str
    start_time: float
    end_time: Optional[float] = None
    metadata: Dict = field(default_factory=dict)
    children: List['TraceSpan'] = field(default_factory=list)
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate span duration in seconds."""
        if self.end_time:
            return self.end_time - self.start_time
        return None


class Tracer:
    """Tracer for tracking agent execution flow."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.spans: List[TraceSpan] = []
        self.active_spans: List[TraceSpan] = []
    
    @contextmanager
    def span(self, name: str, metadata: Optional[Dict] = None):
        """Create a trace span context manager."""
        if not self.enabled:
            yield
            return
        
        span = TraceSpan(
            name=name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        
        # Add as child of active span if exists
        if self.active_spans:
            self.active_spans[-1].children.append(span)
        else:
            self.spans.append(span)
        
        self.active_spans.append(span)
        
        try:
            yield span
        finally:
            span.end_time = time.time()
            self.active_spans.pop()
    
    def get_trace_summary(self) -> Dict:
        """Get summary of all traces."""
        if not self.enabled:
            return {}
        
        def summarize_span(span: TraceSpan) -> Dict:
            return {
                "name": span.name,
                "duration": span.duration,
                "metadata": span.metadata,
                "children": [summarize_span(c) for c in span.children]
            }
        
        return {
            "spans": [summarize_span(s) for s in self.spans],
            "total_spans": len(self.spans),
            "timestamp": datetime.now().isoformat()
        }


# Global tracer instance
_global_tracer = Tracer()


def trace_execution(name: str, metadata: Optional[Dict] = None):
    """Decorator for tracing function execution."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with _global_tracer.span(name, metadata):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def get_tracer() -> Tracer:
    """Get the global tracer instance."""
    return _global_tracer

