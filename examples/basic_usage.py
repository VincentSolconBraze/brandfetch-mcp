#!/usr/bin/env python
"""
Basic example of using the Brandfetch MCP server.

This example demonstrates how to:
1. Search for brands by name
2. Get detailed brand information by identifier

Make sure to set up your environment variables:
- BRANDFETCH_API_KEY
- BRANDFETCH_CLIENT_ID

Or create a .env file with these variables.
"""
import asyncio
import os
import json
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Load environment variables
load_dotenv()

async def main():
    """Run the example."""
    # Server parameters for connecting to the Brandfetch MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["brandfetch_server.py"],
        env={
            "BRANDFETCH_API_KEY": os.environ.get("BRANDFETCH_API_KEY"),
            "BRANDFETCH_CLIENT_ID": os.environ.get("BRANDFETCH_CLIENT_ID"),
        },
    )

    print("Connecting to Brandfetch MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("Connected to Brandfetch MCP server")
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # List available prompts
            prompts = await session.list_prompts()
            print(f"Available prompts: {[prompt.name for prompt in prompts]}")
            
            # Search for a brand
            print("\nSearching for brand 'Apple'...")
            search_result = await session.call_tool(
                "search_brands", 
                arguments={"name": "Apple"}
            )
            print("Search results:")
            print(json.dumps(search_result, indent=2))
            
            # Get the first found brand's details
            if search_result and len(search_result) > 0:
                brand_domain = search_result[0].get("domain")
                if brand_domain:
                    print(f"\nGetting details for brand domain: {brand_domain}")
                    brand_info = await session.call_tool(
                        "get_brand_info",
                        arguments={"identifier": brand_domain}
                    )
                    
                    # Print selected information about the brand
                    print("Brand details:")
                    print(f"Name: {brand_info.get('name')}")
                    print(f"Domain: {brand_info.get('domain')}")
                    print(f"Description: {brand_info.get('description')}")
                    
                    # Print number of logos, colors, and fonts
                    print(f"Number of logos: {len(brand_info.get('logos', []))}")
                    print(f"Number of colors: {len(brand_info.get('colors', []))}")
                    print(f"Number of fonts: {len(brand_info.get('fonts', []))}")
                    
                    # Print social links
                    print("Social links:")
                    for link in brand_info.get("links", []):
                        print(f"  {link.get('name')}: {link.get('url')}")

if __name__ == "__main__":
    asyncio.run(main())