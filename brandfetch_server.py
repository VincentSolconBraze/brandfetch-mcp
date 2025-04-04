#!/usr/bin/env python
"""
Brandfetch API - MCP Server

This server connects to Brandfetch API to search for brands and retrieve
detailed brand information.

Capabilities:
- Search for brands by name
- Get detailed brand information by identifier (domain, brand ID, ISIN, stock symbol)
"""
import logging
import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import httpx
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP, Context

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger("brandfetch-mcp")


@dataclass
class BrandfetchContext:
    """Context for Brandfetch API operations."""
    api_key: str
    client_id: str
    base_url: str
    http_client: httpx.AsyncClient


@asynccontextmanager
async def brandfetch_lifespan(server: FastMCP) -> AsyncIterator[BrandfetchContext]:
    """Initialize and clean up Brandfetch API resources."""
    logger.info("Initializing Brandfetch lifespan...")
    
    # Get API credentials from environment or fail
    api_key = os.environ.get("BRANDFETCH_API_KEY")
    client_id = os.environ.get("BRANDFETCH_CLIENT_ID")
    
    if not api_key:
        logger.error("BRANDFETCH_API_KEY environment variable not set")
        raise ValueError("BRANDFETCH_API_KEY environment variable must be set")
        
    if not client_id:
        logger.error("BRANDFETCH_CLIENT_ID environment variable not set")
        raise ValueError("BRANDFETCH_CLIENT_ID environment variable must be set")
    
    logger.info("API credentials found")
    
    # Set base URL
    base_url = os.environ.get("BRANDFETCH_API_URL", "https://api.brandfetch.io")
    logger.info(f"Using Brandfetch API URL: {base_url}")
    
    # Create HTTP client
    http_client = httpx.AsyncClient(
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        timeout=30.0,  # Generous timeout for API operations
    )
    logger.info("HTTP client created")
    
    try:
        logger.info("Brandfetch lifespan initialization complete")
        yield BrandfetchContext(
            api_key=api_key,
            client_id=client_id,
            base_url=base_url,
            http_client=http_client,
        )
    finally:
        # Clean up resources
        logger.info("Cleaning up HTTP client")
        await http_client.aclose()


# Create the MCP server with our lifespan
mcp = FastMCP(
    "Brandfetch API", 
    lifespan=brandfetch_lifespan,
    dependencies=["httpx", "python-dotenv"],
    version="0.1.0"
)


# Helper function to access Brandfetch context
def get_brandfetch_context(ctx: Context) -> BrandfetchContext:
    """Get the Brandfetch context from the request context."""
    logger.info("Retrieving Brandfetch context")
    
    if not ctx:
        logger.error("Context is None")
        raise ValueError("Context is None")
        
    if not hasattr(ctx, 'request_context'):
        logger.error("request_context not found in Context")
        raise ValueError("request_context not found in Context")
    
    if not hasattr(ctx.request_context, 'lifespan_context'):
        logger.error("lifespan_context not found in request_context")
        raise ValueError("lifespan_context not found in request_context")
    
    logger.info("Successfully retrieved Brandfetch context")
    return ctx.request_context.lifespan_context


@mcp.tool(name="search_brands")
async def search_brands(
    ctx: Context,
    name: str,
    client_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for brands by name using the Brandfetch Search API.
    
    Args:
        name: The name of the company you are searching for.
        client_id: Optional client ID for the API. If not provided, will use the one from environment.
    
    Returns:
        A list of matching brands with their icon, name, domain, claimed status, and brand ID.
        Example:
        [
            {
                "icon": "https://example.com/icon.svg",
                "name": "Example Company",
                "domain": "example.com",
                "claimed": true,
                "brandId": "id_12345"
            }
        ]
    """
    brandfetch = get_brandfetch_context(ctx)
    logger.info(f"Searching for brands with name: {name}")
    
    # Use provided client_id or fall back to the one from environment
    client_id_param = client_id or brandfetch.client_id
    
    try:
        # The search endpoint doesn't use bearer token, it uses client_id as a query parameter
        response = await brandfetch.http_client.get(
            f"{brandfetch.base_url}/v2/search/{name}",
            params={"c": client_id_param},
            headers={
                # Remove the bearer token for this specific request
                "Authorization": None,
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Found {len(result)} brands")
        return result
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during brand search: {e.response.status_code}")
        logger.error(f"Response: {e.response.text}")
        raise ValueError(f"Failed to search brands: HTTP {e.response.status_code}")
    except Exception as e:
        logger.error(f"Exception during brand search: {str(e)}")
        raise ValueError(f"Failed to search brands: {str(e)}")


@mcp.tool(name="get_brand_info")
async def get_brand_info(
    ctx: Context,
    identifier: str,
    fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Get detailed brand information by identifier using the Brandfetch Brand API.
    
    Args:
        identifier: Identifier to retrieve brand data. Accepted formats:
                    - Domain: nike.com
                    - Brand ID: id_0dwKPKT
                    - ISIN: US6541061031
                    - Stock Symbol: NKE
        fields: Optional list of fields to include in the response.
                If None, returns all fields.
    
    Returns:
        Detailed brand information, optionally filtered by the 'fields' parameter.
        The response includes detailed brand assets such as:
        - Brand name and description
        - Logos in various formats
        - Brand colors
        - Fonts used by the brand
        - Social media links
        - Company information
    """
    brandfetch = get_brandfetch_context(ctx)
    logger.info(f"Getting brand info for identifier: {identifier}")
    
    # Build query parameters
    params = {}
    if fields:
        params["fields"] = ",".join(fields)
    
    try:
        # The brand endpoint uses bearer token authentication
        response = await brandfetch.http_client.get(
            f"{brandfetch.base_url}/v2/brands/{identifier}",
            params=params,
            headers={
                "Authorization": f"Bearer {brandfetch.api_key}",
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Successfully retrieved brand info for {identifier}")
        return result
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during brand info retrieval: {e.response.status_code}")
        logger.error(f"Response: {e.response.text}")
        raise ValueError(f"Failed to get brand info: HTTP {e.response.status_code}")
    except Exception as e:
        logger.error(f"Exception during brand info retrieval: {str(e)}")
        raise ValueError(f"Failed to get brand info: {str(e)}")


@mcp.prompt(name="search_prompt")
def search_prompt() -> str:
    """Create a template for searching brands by name."""
    return """Help me search for information about a company or brand using Brandfetch.

To search for a brand, I need:
1. The name of the company or brand I'm looking for
2. Optionally, a specific client ID (if not provided, the default from environment variables will be used)

Please help me format my search to find information about the brand I'm interested in.
"""


@mcp.prompt(name="brand_info_prompt")
def brand_info_prompt() -> str:
    """Create a template for getting detailed brand information."""
    return """Help me get detailed information about a specific brand using Brandfetch.

To retrieve brand details, I need:
1. An identifier for the brand, which can be one of:
   - Domain (e.g., nike.com)
   - Brand ID (e.g., id_0dwKPKT)
   - ISIN (e.g., US6541061031)
   - Stock Symbol (e.g., NKE)

2. Optionally, I can specify which fields I want to retrieve:
   - id
   - name
   - domain
   - claimed
   - description
   - longDescription
   - links
   - logos
   - colors
   - fonts
   - images
   - company (includes employees, industries, location, etc.)

Please help me format my request to get the brand information I need.
"""


# Run the server when executed directly
if __name__ == "__main__":
    logger.info("Starting Brandfetch API server...")
    mcp.run()
    logger.info("Server shutdown")