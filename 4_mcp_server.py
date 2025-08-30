import os
import urllib.request
from fastmcp import FastMCP
import xml.etree.ElementTree as ET
import re

mcp = FastMCP("Arxiv Mcp Server")

@mcp.tool
def fetch_arxiv_papers(topic: str, number_of_papers: int = 3) -> dict:
    """
    Retrieves the latest papers from arXiv matching a given topic.
    
    Args:
        topic (str): The search topic or keyword (e.g., "mcp", "machine learning").
        number_of_papers (int, optional): The number of latest papers to retrieve. Defaults to 3.
    
    Returns:
        dict: A structured response with the following keys:
            - 'status' (str): 'success' or 'error'.
            - 'data' (list): A list of dictionaries, each representing a paper with keys:
                - 'arxiv_id' (str): The arXiv identifier of the paper.
                - 'title' (str): The title of the paper.
                - 'authors' (list of str): List of author names.
                - 'published' (str): Publication date in ISO format.
                - 'pdf_link' (str): URL to the PDF of the paper.
            - 'message' (str): A message describing the result or error.
    """
    try:
        if not topic or not isinstance(topic, str):
            return {"status": "error", "data": [], "message": "Invalid topic provided."}
        if not isinstance(number_of_papers, int) or number_of_papers <= 0:
            return {"status": "error", "data": [], "message": "Invalid number_of_papers provided."}

        search_query = f"all:{topic}"
        url = f'http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={number_of_papers}&sortBy=submittedDate&sortOrder=descending'
        
        print(f"******* FUNCTION CALLED: Fetching papers from arXiv with URL: {url} *******")
    
        with urllib.request.urlopen(url) as resp:
            raw = resp.read()

        root = ET.fromstring(raw)
        papers = []
        for entry in root.findall(".//{*}entry"):
            full_id = entry.findtext("{*}id")
            arxiv_id = full_id.split("/")[-1] if full_id else None
            title = entry.findtext("{*}title")
            published = entry.findtext("{*}published")
            authors = [a.findtext("{*}name") for a in entry.findall("{*}author")]
            pdf_link = next((l.get("href") for l in entry.findall("{*}link") if l.get("type") == "application/pdf"), None)
            papers.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'published': published,
                'pdf_link': pdf_link
            })

        return {"status": "success", "data": papers, "message": f"Fetched {len(papers)} papers successfully."}
    except Exception as e:
        return {"status": "error", "data": [], "message": f"An error occurred: {e}"}
@mcp.tool
def get_arxiv_abstract(arxiv_id: str) -> dict:
    """
    Fetches and returns the abstract of a specific arXiv paper.
    
    Args:
        arxiv_id (str): The arXiv ID (e.g., "2301.12345"). Must be a valid arXiv identifier.
    
    Returns:
        dict: A structured response with the following keys:
            - 'status' (str): 'success' or 'error'.
            - 'data' (str): The abstract text of the paper, or None if not found.
            - 'message' (str): A message describing the result or error.
    """
    try:
        if not arxiv_id or not isinstance(arxiv_id, str):
            return {"status": "error", "data": None, "message": "Invalid arXiv ID provided."}

        url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
        print(f"******* FUNCTION CALLED: Fetching paper abstract from arXiv with URL: {url} *******")
        with urllib.request.urlopen(url) as resp:
            raw = resp.read()

        root = ET.fromstring(raw)
        entry = root.find(".//{*}entry")
        if entry is not None:
            abstract = entry.findtext("{*}summary")
            return {"status": "success", "data": abstract, "message": "Abstract fetched successfully."}
        else:
            return {"status": "error", "data": None, "message": "Paper not found."}
    except Exception as e:
        return {"status": "error", "data": None, "message": f"An error occurred: {e}"}
@mcp.tool
def save_md_to_file(text: str, filename: str) -> dict:
    """
    Saves the given Markdown-formatted text to a .md file in the ./reports folder.
    
    Args:
        text (str): The Markdown-formatted text to save.
        filename (str): The desired name of the file (e.g., "Model Context Protocols in Adaptive Transport Systems").
            Special characters will be replaced with hyphens, and '.md' will be appended if not present.
    
    Returns:
        dict: A structured response with the following keys:
            - 'status' (str): 'success' or 'error'.
            - 'data' (str): The path to the saved file, or None if an error occurred.
            - 'message' (str): A message describing the result or error.
    """
    try:
        if not text or not isinstance(text, str):
            return {"status": "error", "data": None, "message": "Invalid text provided."}
        if not filename or not isinstance(filename, str):
            return {"status": "error", "data": None, "message": "Invalid filename provided."}

        # Create reports folder if it doesn't exist
        os.makedirs("./reports", exist_ok=True)

        # Sanitize filename to avoid issues with special characters
        filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
        print(f"******* FUNCTION CALLED: Saving Markdown to file: {filename} *******")
        if not filename.endswith('.md'):
            filename += '.md'

        # Set path to ./reports
        filepath = os.path.join("./reports", filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        return {"status": "success", "data": filepath, "message": "File saved successfully."}
    except Exception as e:
        return {"status": "error", "data": None, "message": f"An error occurred: {e}"}

if __name__ == "__main__":
    mcp.run()

# USE COMMANDS:
# RUN
# "fastmcp run 4_mcp_server.py:mcp" or just "python 4_mcp_server.py"
# This command starts the MCP server defined in the file `mcp_server.py` with the instance `mcp`.
# It allows the server to register its tools and make them accessible for external clients.

# TEST
# "npx @modelcontextprotocol/inspector"
# This command connects to the MCP server and lists all available tools with their metadata. 
# It allows interactive testing and debugging of the server's tools.
