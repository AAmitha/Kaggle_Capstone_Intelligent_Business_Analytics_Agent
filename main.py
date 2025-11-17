"""Main entry point for the Intelligent Business Analytics Agent."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.coordinator import CoordinatorAgent
from src.memory.session_manager import SessionManager
from src.utils.helpers import create_sample_data, format_output
from src.observability import setup_logger, get_metrics_collector

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger("main")


def main():
    """Main function to run the agent."""
    print("=" * 60)
    print("Intelligent Business Analytics Agent")
    print("=" * 60)
    print()
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        sys.exit(1)
    
    try:
        # Initialize coordinator
        logger.info("Initializing Coordinator Agent...")
        coordinator = CoordinatorAgent(user_id="demo_user", api_key=api_key)
        
        # Interactive mode
        print("Agent initialized successfully!")
        print("\nYou can now ask questions about your data.")
        print("Example queries:")
        print("  - 'Analyze the sales data in data/sample_data.csv'")
        print("  - 'Generate a report on revenue trends'")
        print("  - 'Compare sales by region'")
        print("\nType 'exit' to quit, 'help' for more options\n")
        
        while True:
            try:
                query = input("Query: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if query.lower() == 'help':
                    print_help()
                    continue
                
                if query.lower() == 'sample':
                    create_sample_data()
                    print("Sample data created at data/sample_data.csv")
                    continue
                
                if query.lower() == 'metrics':
                    metrics = get_metrics_collector().get_summary()
                    print("\nMetrics Summary:")
                    import json
                    print(json.dumps(metrics, indent=2))
                    continue
                
                # Extract data file if mentioned
                data_file = None
                if 'data/' in query or '.csv' in query or '.json' in query:
                    # Simple extraction - in production, use better parsing
                    words = query.split()
                    for word in words:
                        if word.endswith('.csv') or word.endswith('.json'):
                            data_file = word
                            break
                        if 'data/' in word:
                            data_file = word
                            break
                
                # Run analysis
                print("\nProcessing...")
                result = coordinator.analyze(query, data_file)
                
                # Display results
                output = format_output(result, "console")
                print("\n" + output + "\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}", exc_info=True)
                print(f"\nError: {e}\n")
        
        # Print final metrics
        print("\n" + "=" * 60)
        print("Session Summary")
        print("=" * 60)
        metrics = get_metrics_collector().get_summary()
        print(f"Total requests: {metrics.get('counters', {}).get('coordinator.analysis_requests', 0)}")
        print(f"Successful: {metrics.get('counters', {}).get('coordinator.analysis_success', 0)}")
        print(f"Errors: {metrics.get('counters', {}).get('coordinator.analysis_errors', 0)}")
        
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        print(f"ERROR: {e}")
        sys.exit(1)


def print_help():
    """Print help information."""
    help_text = """
Available commands:
  - Type any natural language query to analyze data
  - 'sample' - Create sample data file
  - 'metrics' - Show performance metrics
  - 'help' - Show this help message
  - 'exit' - Quit the application

Example queries:
  - "Analyze sales data in data/sample_data.csv"
  - "Generate a report on revenue trends"
  - "Compare sales performance by region"
  - "What are the key insights from the data?"
    """
    print(help_text)


if __name__ == "__main__":
    main()

