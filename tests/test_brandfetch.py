"""
Tests for the Brandfetch MCP server.

These tests verify that the server correctly handles:
1. Brand search requests
2. Brand information requests with field filtering

Note: These tests use mocked responses to avoid making actual API calls.
"""
import asyncio
import pytest
import os
import httpx
from unittest.mock import patch, MagicMock, AsyncMock

# Add the parent directory to the path to import the server
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import brandfetch_server
from mcp.server.fastmcp import Context


@pytest.fixture
def mock_context():
    """Create a mock context for testing."""
    context = MagicMock(spec=Context)
    context.request_context = MagicMock()
    
    # Mock the lifespan context
    brandfetch_context = MagicMock()
    brandfetch_context.api_key = "test_api_key"
    brandfetch_context.client_id = "test_client_id"
    brandfetch_context.base_url = "https://api.brandfetch.io"
    brandfetch_context.http_client = AsyncMock(spec=httpx.AsyncClient)
    
    context.request_context.lifespan_context = brandfetch_context
    return context


@pytest.mark.asyncio
async def test_search_brands(mock_context):
    """Test the search_brands function."""
    # Create a mock response for the search API
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "icon": "https://example.com/icon.svg",
            "name": "Example Company",
            "domain": "example.com",
            "claimed": True,
            "brandId": "id_12345"
        }
    ]
    
    # Set up the mock client to return our mock response
    mock_context.request_context.lifespan_context.http_client.get.return_value = mock_response
    
    # Call the function
    result = await brandfetch_server.search_brands(mock_context, "Example")
    
    # Verify the result
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "Example Company"
    assert result[0]["domain"] == "example.com"
    
    # Verify the API was called correctly
    mock_context.request_context.lifespan_context.http_client.get.assert_called_once_with(
        "https://api.brandfetch.io/v2/search/Example",
        params={"c": "test_client_id"},
        headers={
            "Authorization": None,
            "Content-Type": "application/json",
        }
    )


@pytest.mark.asyncio
async def test_get_brand_info(mock_context):
    """Test the get_brand_info function."""
    # Create a mock response for the brand API
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "id_12345",
        "name": "Example Company",
        "domain": "example.com",
        "claimed": True,
        "description": "An example company",
        "logos": [
            {
                "type": "logo",
                "theme": "light",
                "formats": [
                    {
                        "src": "https://example.com/logo.svg",
                        "format": "svg",
                        "width": 200,
                        "height": 100
                    }
                ]
            }
        ]
    }
    
    # Set up the mock client to return our mock response
    mock_context.request_context.lifespan_context.http_client.get.return_value = mock_response
    
    # Call the function with field filtering
    result = await brandfetch_server.get_brand_info(
        mock_context, 
        "example.com", 
        fields=["name", "logos"]
    )
    
    # Verify the result
    assert isinstance(result, dict)
    assert result["name"] == "Example Company"
    assert len(result["logos"]) == 1
    assert result["logos"][0]["type"] == "logo"
    
    # Verify the API was called correctly
    mock_context.request_context.lifespan_context.http_client.get.assert_called_once_with(
        "https://api.brandfetch.io/v2/brands/example.com",
        params={"fields": "name,logos"},
        headers={
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json",
        }
    )


@pytest.mark.asyncio
async def test_get_brand_info_error_handling(mock_context):
    """Test that the get_brand_info function handles errors correctly."""
    # Create a mock response for a 404 error
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.text = "Brand not found"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", 
        request=httpx.Request("GET", "https://api.brandfetch.io/v2/brands/nonexistent.com"),
        response=mock_response
    )
    
    # Set up the mock client to return our mock response
    mock_context.request_context.lifespan_context.http_client.get.return_value = mock_response
    
    # Call the function and verify it raises the correct error
    with pytest.raises(ValueError) as excinfo:
        await brandfetch_server.get_brand_info(mock_context, "nonexistent.com")
    
    assert "Failed to get brand info: HTTP 404" in str(excinfo.value)
