# Usage Examples

This document provides examples of how to use the Brandfetch MCP server with LLM applications.

## Searching for Brands

### Example 1: Basic Brand Search

In this example, we'll search for information about Apple Inc.

```
Use the Brandfetch MCP server to search for brands related to "Apple".
```

The LLM will use the `search_brands` tool to query the Brandfetch API and return a list of matching brands, including their icons, names, domains, and IDs.

### Example 2: Filtering Brand Results

If you want to find a specific brand, you can be more precise in your query:

```
Search for the brand "Tesla Motors" using Brandfetch.
```

## Retrieving Brand Details

### Example 1: Getting Complete Brand Information

To get comprehensive information about a brand using its domain:

```
Use Brandfetch to get detailed information about tesla.com
```

The LLM will use the `get_brand_info` tool with the domain as the identifier to fetch comprehensive brand information.

### Example 2: Filtering Brand Information Fields

If you're only interested in specific aspects of a brand:

```
Get only the logo and colors for the brand Apple using Brandfetch.
```

The LLM will use the `get_brand_info` tool with the `fields` parameter set to retrieve only the logo and color information.

### Example 3: Using Different Identifiers

You can also retrieve brand information using other identifiers:

```
Get information about the brand with stock symbol AAPL using Brandfetch.
```

## Using Prompts

### Example 1: Using the Search Prompt

If you're not sure how to structure your search:

```
I want to search for brands related to coffee. Help me format this correctly.
```

The LLM will use the `search_prompt` to help format your query properly for searching brands.

### Example 2: Using the Brand Info Prompt

If you need guidance on retrieving specific brand information:

```
I want to get logo information for Nike, but I'm not sure how to structure the request.
```

The LLM will use the `brand_info_prompt` to guide you through the proper format for retrieving specific brand information.