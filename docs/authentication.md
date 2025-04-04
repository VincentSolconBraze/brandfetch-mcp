# Authentication Guide

This guide explains how to set up authentication for the Brandfetch MCP server.

## Obtaining API Credentials

To use the Brandfetch API, you need the following credentials:

1. **API Key**: Used for bearer authentication for the Brand API
2. **Client ID**: Used for the Brand Search API

You can obtain these by:

1. Creating an account on [Brandfetch](https://brandfetch.com/)
2. Navigating to the API section of your account
3. Generating the necessary credentials

## Setting Up Environment Variables

For security, we recommend storing your API credentials as environment variables rather than hardcoding them in your application.

### Option 1: .env File

1. Create a `.env` file in the root directory of your project:

```bash
cp .env.example .env
```

2. Add your API credentials to the `.env` file:

```
BRANDFETCH_API_KEY=your_api_key
BRANDFETCH_CLIENT_ID=your_client_id
```

### Option 2: Export in Shell

You can also export these variables in your shell:

```bash
export BRANDFETCH_API_KEY=your_api_key
export BRANDFETCH_CLIENT_ID=your_client_id
```

## Testing Authentication

To verify that your authentication is set up correctly, run the MCP server in development mode:

```bash
mcp dev brandfetch_server.py
```

Then try a simple brand search to confirm that the API connection works.