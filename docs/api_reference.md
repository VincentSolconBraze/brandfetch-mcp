# Brandfetch MCP API Reference

This document describes the tools available in the Brandfetch MCP server.

## Brand Search

### `search_brands`

Search for brands by name using the Brandfetch Search API.

**Parameters:**

- `name` (string, required): The name of the company you are searching for.
- `client_id` (string, optional): Optional client ID for the API. If not provided, will use the one from environment.

**Returns:**

A list of matching brands with their icon, name, domain, claimed status, and brand ID.

**Example:**

```json
[
    {
        "icon": "https://example.com/icon.svg",
        "name": "Example Company",
        "domain": "example.com",
        "claimed": true,
        "brandId": "id_12345"
    }
]
```

## Brand Information

### `get_brand_info`

Get detailed brand information by identifier using the Brandfetch Brand API.

**Parameters:**

- `identifier` (string, required): Identifier to retrieve brand data. Accepted formats:
  - Domain: nike.com
  - Brand ID: id_0dwKPKT
  - ISIN: US6541061031
  - Stock Symbol: NKE
- `fields` (list of strings, optional): Optional list of fields to include in the response. If None, returns all fields.

**Returns:**

Detailed brand information, optionally filtered by the 'fields' parameter.
The response includes detailed brand assets such as:
- Brand name and description
- Logos in various formats
- Brand colors
- Fonts used by the brand
- Social media links
- Company information

## Prompts

### `search_prompt`

A prompt to help users search for brands with the proper formatting.

### `brand_info_prompt`

A prompt to help users retrieve brand information with the proper formatting and filtering options.