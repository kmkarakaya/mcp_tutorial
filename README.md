# MCP Tutorial

## Overview

This repository demonstrates a small MCP (Model Context Protocol) ecosystem built around FastMCP. It contains a sample MCP server exposing tools (arXiv fetch, abstract retrieval, save-markdown) and example clients: a simple FastMCP client and a Google Gemini-integrated agent. The code is intended as a practical tutorial and reference for running and testing an MCP server locally, integrating it with LLMs (Gemini), and using the MCP Inspector for interactive exploration.

Key points:

- Server uses the `fastmcp` library to define and expose tools.
- Client examples show how to call tools programmatically and how to attach an LLM (Gemini) to MCP tools.
- Includes Docker-ready server and agent examples for containerized testing.

## Quick start

1. Clone and install dependencies:

   ```powershell
   git clone https://github.com/kmkarakaya/mcp_tutorial.git; cd mcp_tutorial
   pip install -r requirements.txt
   ```

2. Start the MCP server (local):

   ```powershell
   python 4_mcp_server.py
   ```

   The server exposes tools and listens for client connections (default behavior provided by FastMCP).

## Usage and examples

- Inspect available tools with the official MCP Inspector (requires Node.js and npm or Corepack installed):

  ```powershell
  npx @modelcontextprotocol/inspector
  ```

  Note: `npx` comes with npm (or use Corepack on newer Node versions). Install Node.js from https://nodejs.org/ if you don't have `node`/`npm` on your system.

- Run the example client to call a tool programmatically:

  ```powershell
  python 5_mcp_client.py
  ```

- Start an interactive Gemini-based agent that can call MCP tools (requires Google GenAI credentials):

  ```powershell
  python 6_mcp_gemini_agent.py
  ```

  When using the Gemini agent, set your environment variables per `google-genai` docs (e.g., `GOOGLE_API_KEY` or equivalent) before running.

## Docker

Dockerfiles/examples are included. Example build/run:

```powershell
docker build -t mcp_server .
docker run -p 8000:8000 mcp_server
```

## Tools implemented in the server

- `fetch_arxiv_papers(topic: str, number_of_papers: int = 3)` — fetches recent arXiv papers for a topic.
- `get_arxiv_abstract(arxiv_id: str)` — retrieves an arXiv paper abstract.
- `save_md_to_file(text: str, filename: str)` — saves given markdown to `./reports`.

## Dependencies

See `requirements.txt`. Important packages:

- fastmcp
- google-genai (for Gemini integration)
- uvicorn (if you run the server via ASGI)

## Notes

- The server file (`4_mcp_server.py`) prints helpful messages when functions are called and includes a `mcp.run()` entry point.
- Use the MCP Inspector to verify tool metadata and try calls interactively.

## Author

Murat Karakaya  
[Website](https://www.muratkarakaya.net/)  
[LinkedIn](https://www.linkedin.com/in/muratkarakaya/)  
[YouTube](https://www.youtube.com/c/muratkarakayaakademi)

## Acknowledgments

Based on MCP work and examples; thanks to Anthropic, OpenAI, and contributors to the MCP ecosystem.
