# Brandfetch MCP Server

<div align="center">

<strong>Model Context Protocol (MCP) server for Brandfetch API</strong>

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

</div>

## Overview

This MCP server provides a bridge between Large Language Model (LLM) applications and the Brandfetch API, allowing AI assistants to search for brands and retrieve comprehensive brand information. By implementing the Model Context Protocol, this server enables seamless integration of Brandfetch's brand data capabilities into LLM-powered applications.

## Features

- **Brand Search**: Search for brands by name and get basic information
- **Detailed Brand Information**: Retrieve comprehensive brand data including logos, colors, fonts, and company details
- **Field Filtering**: Request only specific information to optimize response size and processing
- **Interactive Prompts**: Built-in prompts to guide users on proper API usage
- **Type-safe Implementation**: Fully typed Python codebase with modern async support
- **Robust Error Handling**: Comprehensive error handling and logging

## Installation

### Prerequisites

- Python 3.9 or higher
- Brandfetch API credentials (API key and Client ID)

### Using uv (recommended)

```bash
# Create and navigate to a new project directory
uv init brandfetch-mcp
cd brandfetch-mcp

# Clone this repository
git clone https://github.com/VincentSolconBraze/brandfetch-mcp.git .

# Add dependencies
uv add "mcp[cli]" httpx python-dotenv

# For development
uv add --dev pytest pytest-asyncio pytest-cov ruff pyright pre-commit
```

### Using pip

```bash
# Clone this repository
git clone https://github.com/VincentSolconBraze/brandfetch-mcp.git
cd brandfetch-mcp

# Install dependencies
pip install "mcp[cli]" httpx python-dotenv

# For development
pip install pytest pytest-asyncio pytest-cov ruff pyright pre-commit
```

## Configuration

1. Create a `.env` file based on the example:

```bash
cp .env.example .env
```

2. Add your Brandfetch API credentials to the `.env` file:

```
BRANDFETCH_API_KEY=your_api_key
BRANDFETCH_CLIENT_ID=your_client_id
```

You can obtain these credentials by creating an account on [Brandfetch](https://brandfetch.com/) and navigating to the API section.

## Usage

### Running with Claude Desktop

The server can be installed directly in Claude Desktop for seamless integration:

```bash
mcp install brandfetch_server.py
```

### Testing with MCP Inspector

To debug and test the server locally with the MCP Inspector tool:

```bash
mcp dev brandfetch_server.py
```

### Direct Execution

You can also run the server directly:

```bash
python brandfetch_server.py
```

## Available Tools

### search_brands

Search for brands by name using the Brandfetch Search API.

**Parameters:**
- `name`: The name of the company you are searching for.
- `client_id` (optional): Client ID for the API. If not provided, will use the one from environment.

**Example:**
```
Search for brands related to "Nike"
```

### get_brand_info

Get detailed brand information by identifier using the Brandfetch Brand API.

**Parameters:**
- `identifier`: Brand identifier (domain, brand ID, ISIN, or stock symbol)
- `fields` (optional): List of specific fields to include in the response

**Example:**
```
Get detailed information about nike.com with only logos and colors
```

## Examples

The `examples` directory contains sample code demonstrating how to interact with the server:

- **basic_usage.py**: Simple brand search and information retrieval
- **advanced_usage.py**: Advanced usage with field filtering and result processing

To run the examples:

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

## Testing

Run the test suite to verify the server functionality:

```bash
pytest
```

For coverage reporting:

```bash
pytest --cov=./ --cov-report=term
```

## Documentation

More detailed documentation is available in the following files:

- [Authentication Guide](docs/authentication.md)
- [API Reference](docs/api_reference.md)
- [Usage Examples](docs/examples.md)

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Security

Please review our [Security Policy](SECURITY.md) for information on reporting security vulnerabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
