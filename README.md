# Intelligent Business Analytics Agent

## Overview

The **Intelligent Business Analytics Agent** is an enterprise-grade multi-agent system designed to automate business data analysis, generate insights, and create comprehensive reports. This agent system helps businesses make data-driven decisions by providing intelligent analysis of sales, revenue, customer, and operational data.

## Problem Statement

Businesses generate vast amounts of data daily, but extracting meaningful insights requires significant time and expertise. Data analysts spend hours:
- Cleaning and processing data
- Performing statistical analysis
- Generating visualizations
- Writing reports
- Identifying trends and anomalies

This manual process is time-intensive, error-prone, and doesn't scale well with growing data volumes.

## Solution

Our multi-agent system automates the entire analytics workflow:
- **Coordinator Agent**: Orchestrates the analysis workflow and delegates tasks
- **Data Analyst Agent**: Performs statistical analysis and identifies patterns
- **Report Generator Agent**: Creates comprehensive reports with visualizations
- **Memory System**: Maintains context across sessions for personalized insights
- **Custom Tools**: Specialized tools for data processing, visualization, and reporting

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Coordinator Agent (Orchestrator)           │
│         - Manages workflow                              │
│         - Delegates tasks to specialized agents         │
│         - Maintains session state                       │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┴────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐  ┌──────▼──────┐  ┌───────▼────────┐
│ Data Analyst│  │Report Gen.  │  │ Custom Tools │
│   Agent     │  │   Agent     │  │ - Data Loader  │
│             │  │             │  │ - Visualizer   │
│ - Statistical│ │ - Report    │  │ - Calculator   │
│   Analysis  │ │   Builder    │  │ - Trend Finder │
│ - Pattern   │ │ - Formatter  │  │                │
│   Detection │ │              │  │                │
└─────────────┘  └─────────────┘  └────────────────┘
       │                 │                  │
       └─────────────────┴──────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Memory Bank        │
              │  - Session History  │
              │  - User Preferences │
              │  - Context Storage  │
              └─────────────────────┘
```

## Key Features

### 1. Multi-Agent System ✓
- **Coordinator Agent**: Orchestrates the entire workflow
- **Data Analyst Agent**: Specialized in statistical analysis
- **Report Generator Agent**: Creates formatted reports
- **Parallel Processing**: Agents can work simultaneously on different tasks

### 2. Custom Tools ✓
- **DataLoaderTool**: Loads and preprocesses CSV/JSON data
- **StatisticalAnalysisTool**: Performs statistical computations
- **VisualizationTool**: Generates charts and graphs
- **TrendAnalysisTool**: Identifies trends and patterns
- **ReportFormatterTool**: Formats output as markdown/HTML

### 3. Sessions & Memory ✓
- **InMemorySessionService**: Manages conversation context
- **Memory Bank**: Stores long-term insights and preferences
- **Context Compaction**: Efficiently manages large conversation histories

### 4. Observability ✓
- **Structured Logging**: Comprehensive logging at all levels
- **Tracing**: Track agent execution flow
- **Metrics**: Performance and usage metrics

### 5. Agent Evaluation ✓
- Built-in evaluation framework for agent performance
- Quality metrics for generated reports

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Cloud account with Gemini API access
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "Kaggle Capstone - Intelligent Business Analytics Agent"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Run the agent:
```bash
python main.py
```

## Usage

### Basic Usage

```python
from src.coordinator import CoordinatorAgent
from src.memory.session_manager import SessionManager

# Initialize session
session_manager = SessionManager()
session = session_manager.create_session("user_123")

# Initialize coordinator
coordinator = CoordinatorAgent(session_id=session.id)

# Analyze data
result = coordinator.analyze(
    "Analyze the sales data in sales_data.csv and generate a report"
)
print(result)
```

### Example Queries

1. **Data Analysis**:
   ```
   "Analyze the revenue trends in Q4 2024"
   ```

2. **Report Generation**:
   ```
   "Generate a comprehensive report on customer behavior patterns"
   ```

3. **Comparative Analysis**:
   ```
   "Compare sales performance between regions A and B"
   ```

## Project Structure

```
Kaggle Capstone - Intelligent Business Analytics Agent/
├── src/
│   ├── __init__.py
│   ├── coordinator.py          # Main coordinator agent
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── data_analyst.py     # Data analysis agent
│   │   └── report_generator.py # Report generation agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── data_loader.py      # Data loading tool
│   │   ├── statistical.py      # Statistical analysis tool
│   │   ├── visualization.py     # Visualization tool
│   │   └── report_formatter.py # Report formatting tool
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── session_manager.py   # Session management
│   │   └── memory_bank.py       # Long-term memory
│   ├── observability/
│   │   ├── __init__.py
│   │   ├── logger.py            # Structured logging
│   │   ├── tracer.py             # Execution tracing
│   │   └── metrics.py           # Performance metrics
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Utility functions
├── data/
│   └── sample_data.csv          # Sample data for testing
├── tests/
│   ├── __init__.py
│   ├── test_coordinator.py
│   ├── test_agents.py
│   └── test_tools.py
├── main.py                       # Entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## Key Concepts Demonstrated

### 1. Multi-Agent System ✓
- Coordinator agent orchestrates workflow
- Specialized agents (Data Analyst, Report Generator) work in parallel
- Sequential agent chains for complex workflows

### 2. Custom Tools ✓
- DataLoaderTool for CSV/JSON processing
- StatisticalAnalysisTool for computations
- VisualizationTool for chart generation
- ReportFormatterTool for output formatting

### 3. Sessions & Memory ✓
- InMemorySessionService for conversation context
- Memory Bank for long-term storage
- Context compaction for efficiency

### 4. Observability ✓
- Structured logging with different levels
- Execution tracing across agents
- Performance metrics collection

### 5. Agent Evaluation ✓
- Quality metrics for generated reports
- Performance benchmarking

## Technical Implementation

### Agent Framework
Built using Google's Agent Development Kit (ADK) with Gemini models for natural language understanding and generation.

### Data Processing
- Pandas for data manipulation
- NumPy for numerical computations
- Matplotlib/Plotly for visualizations

### Memory Management
- In-memory session storage for active conversations
- Persistent memory bank for long-term insights
- Context compaction to manage large histories

## Evaluation Metrics

- **Response Time**: Average time to generate analysis
- **Accuracy**: Quality of insights and recommendations
- **User Satisfaction**: Feedback on report quality
- **Memory Efficiency**: Context management performance

## Future Enhancements

- [ ] Database integration for real-time data
- [ ] Advanced visualization options
- [ ] Multi-language support
- [ ] Cloud deployment with Agent Engine
- [ ] A2A Protocol implementation
- [ ] Enhanced evaluation framework

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Amitha Akepati - Data Scientist | AI/ML Expert

## Acknowledgments

- Google AI Studio for Gemini API
- Agent Development Kit (ADK) team
- Kaggle for hosting the competition
