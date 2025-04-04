# Brandfetch MCP Server Examples

This directory contains examples of how to use the Brandfetch MCP server.

## Prerequisites

Before running these examples, make sure you have:

1. Set up your environment variables:
   - `BRANDFETCH_API_KEY`
   - `BRANDFETCH_CLIENT_ID`

2. Installed the required dependencies:
   ```bash
   pip install "mcp[cli]" httpx python-dotenv
   ```

## Available Examples

### Basic Usage

The `basic_usage.py` example demonstrates:
- Connecting to the Brandfetch MCP server
- Searching for brands by name
- Getting detailed brand information

To run:
```bash
python examples/basic_usage.py
```

### Advanced Usage

The `advanced_usage.py` example demonstrates:
- Filtering brand information by specific fields
- Processing and displaying logo information
- Processing and displaying color information

To run:
```bash
python examples/advanced_usage.py
```

## Customizing Examples

You can modify these examples to suit your specific needs:

- Change the brand search term
- Request different fields from the brand API
- Process different types of brand information