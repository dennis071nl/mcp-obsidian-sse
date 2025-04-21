# MCP Server with SSE endpoint for Obsidian

This is a simple MCP server with a SSE endpoint for Obsidian. I use this to connect my obsidian vault to my self-hosted n8n. Before running this, you need to install the [Obsidian API](https://github.com/obsidianmd/obsidian-api) on your obsidian vault.

## Usage

```bash
git clone https://github.com/mcp-server/mcp-obsidian-sse.git
uv --directory mcp-obsidian-sse uvicorn main:app --reload
```

## Credit
This project is based on the [mcp-server](https://github.com/mcp-server/mcp-server) project.