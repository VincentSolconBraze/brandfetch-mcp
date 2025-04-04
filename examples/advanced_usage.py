#!/usr/bin/env python
"""
Advanced example of using the Brandfetch MCP server.

This example demonstrates how to:
1. Get filtered brand information (only logos and colors)
2. Process and display logo information
3. Process and display color information

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
            
            # First, search for a brand
            brand_name = "Google"
            print(f"\nSearching for brand '{brand_name}'...")
            search_result = await session.call_tool(
                "search_brands", 
                arguments={"name": brand_name}
            )
            
            if not search_result or len(search_result) == 0:
                print(f"No brands found for '{brand_name}'")
                return
            
            # Get the first found brand's domain
            brand_domain = search_result[0].get("domain")
            if not brand_domain:
                print("Domain not found in search results")
                return
            
            print(f"Found brand: {search_result[0].get('name')} ({brand_domain})")
            
            # Get only logos and colors for the brand
            print(f"\nGetting logos and colors for {brand_domain}...")
            brand_info = await session.call_tool(
                "get_brand_info",
                arguments={
                    "identifier": brand_domain,
                    "fields": ["logos", "colors"]
                }
            )
            
            # Process logos
            logos = brand_info.get("logos", [])
            print(f"\nFound {len(logos)} logo assets:")
            
            for i, logo in enumerate(logos, 1):
                logo_type = logo.get("type", "unknown")
                theme = logo.get("theme", "unknown")
                formats = logo.get("formats", [])
                
                print(f"Logo {i}: Type={logo_type}, Theme={theme}")
                print(f"  Available formats:")
                
                for j, fmt in enumerate(formats, 1):
                    format_type = fmt.get("format", "unknown")
                    src = fmt.get("src", "N/A")
                    width = fmt.get("width", "N/A")
                    height = fmt.get("height", "N/A")
                    
                    print(f"    Format {j}: {format_type} ({width}x{height})")
                    print(f"      URL: {src}")
            
            # Process colors
            colors = brand_info.get("colors", [])
            print(f"\nFound {len(colors)} color assets:")
            
            for i, color in enumerate(colors, 1):
                hex_code = color.get("hex", "unknown")
                color_type = color.get("type", "unknown")
                brightness = color.get("brightness", "N/A")
                
                print(f"Color {i}: {hex_code} (Type={color_type}, Brightness={brightness})")

            print("\nThis example demonstrates retrieving filtered brand information.")
            print("You can specify any combination of fields to retrieve only what you need.")

if __name__ == "__main__":
    asyncio.run(main())