"""Metrics collection for agent performance monitoring."""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import time


@dataclass
class Metric:
    """Represents a single metric."""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collects and stores performance metrics."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.metrics: List[Metric] = []
        self.counters: Dict[str, int] = defaultdict(int)
        self.timers: Dict[str, List[float]] = defaultdict(list)
    
    def increment(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        if not self.enabled:
            return
        
        self.counters[name] += value
        self.metrics.append(
            Metric(
                name=f"{name}.count",
                value=self.counters[name],
                tags=tags or {}
            )
        )
    
    def record_timing(self, name: str, duration: float, tags: Optional[Dict[str, str]] = None):
        """Record a timing metric."""
        if not self.enabled:
            return
        
        self.timers[name].append(duration)
        self.metrics.append(
            Metric(
                name=f"{name}.duration",
                value=duration,
                tags=tags or {}
            )
        )
    
    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a gauge metric."""
        if not self.enabled:
            return
        
        self.metrics.append(
            Metric(
                name=name,
                value=value,
                tags=tags or {}
            )
        )
    
    def get_summary(self) -> Dict:
        """Get summary of collected metrics."""
        if not self.enabled:
            return {}
        
        summary = {
            "counters": dict(self.counters),
            "timers": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Calculate timer statistics
        for name, timings in self.timers.items():
            if timings:
                summary["timers"][name] = {
                    "count": len(timings),
                    "min": min(timings),
                    "max": max(timings),
                    "avg": sum(timings) / len(timings),
                    "total": sum(timings)
                }
        
        return summary
    
    def clear(self):
        """Clear all collected metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.timers.clear()


# Global metrics collector
_global_metrics = MetricsCollector()


def collect_metric(name: str, value: float, metric_type: str = "gauge", tags: Optional[Dict[str, str]] = None):
    """Convenience function to collect a metric."""
    if metric_type == "counter":
        _global_metrics.increment(name, int(value), tags)
    elif metric_type == "timer":
        _global_metrics.record_timing(name, value, tags)
    else:
        _global_metrics.gauge(name, value, tags)


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector."""
    return _global_metrics

