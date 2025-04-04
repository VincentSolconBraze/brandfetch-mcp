# Brandfetch MCP Server

<div align="center">

<strong>Model Context Protocol (MCP) server for Brandfetch API</strong>

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

</div>

## Overview

This MCP server provides a bridge between LLM applications and the Brandfetch API, allowing AI assistants to search for brands and retrieve comprehensive brand information.

## Features

- Search for brands by name
- Retrieve detailed brand information including logos, colors, fonts, and company data
- Filter brand information by specific fields
- Interactive prompts for guiding usage

## Installation

### Prerequisites

- Python 3.9 or higher
- Brandfetch API credentials

### Using uv (recommended)

```bash
# Create a new project
uv init brandfetch-mcp
cd brandfetch-mcp

# Add dependencies
uv add "mcp[cli]" httpx python-dotenv
```

### Using pip

```bash
pip install "mcp[cli]" httpx python-dotenv
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

## Usage

### Running with Claude Desktop

```bash
mcp install brandfetch_server.py
```

### Testing with MCP Inspector

```bash
mcp dev brandfetch_server.py
```

### Direct Execution

```bash
python brandfetch_server.py
```

## Documentation

For detailed usage examples and API reference, see the [documentation](docs/api_reference.md).

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Security

Please review our [Security Policy](SECURITY.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.