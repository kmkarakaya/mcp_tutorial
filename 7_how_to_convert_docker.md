# How to Run MCP Server in Docker and Gemini Agent Locally

This document explains how to set up and run the MCP server in a Docker container, while running the Gemini agent locally on your host machine. This approach keeps the server containerized for portability, while allowing the agent to run natively for easier interaction.

## Architecture Overview

This setup uses a **hybrid architecture**:

1. **Docker Container**: Runs the MCP server (`8_mcp_docker_server.py`) with HTTP transport on port 1923
2. **Local Host**: Runs the Gemini agent (`6_mcp_gemini_agent.py`) which connects to the Dockerized server
3. **Volume Mount**: The `./reports` directory is shared between container and host for file persistence

### Why Two Server Files?

- **`4_mcp_server.py`**: For development and testing locally with stdio transport (faster, simpler)
- **`8_mcp_docker_server.py`**: For production Docker deployment with HTTP transport (network-accessible, containerized)

This approach provides the best of both worlds: easy local development and robust containerized deployment.

## Quick Start Commands

### For Local Development:

```bash
# Test locally with stdio transport
fastmcp run 4_mcp_server.py:mcp
npx @modelcontextprotocol/inspector
```

### For Docker Deployment:

````bash
```bash
# Build and run Docker container with custom name
docker build -t arxiv-mcp-server .
docker run -d --name mcp-arxiv-server -p 1923:1923 -v ${PWD}/reports:/app/reports arxiv-mcp-server

# Test Docker container
npx @modelcontextprotocol/inspector --transport streamable-http --url http://localhost:1923
````

---

## 1. Prerequisites

Before proceeding, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10+**: For local testing before containerization.
- **Pip**: To manage Python dependencies.

---

## 2. Prepare the Project Directory

Ensure the following files are in the same directory:

- `8_mcp_docker_server.py`: Docker-optimized MCP server with HTTP transport
- `requirements.txt`: Python dependencies (includes uvicorn for HTTP server)
- `Dockerfile`: Docker container configuration

**Note**: The `9_mcp_docker_gemini_agent.py` script runs locally on the host and connects to the Dockerized MCP server.

### Example `requirements.txt`:

```plaintext
fastmcp==2.11.3
google-genai==1.17.0
uvicorn[standard]==0.30.1
```

**Note**: The `uvicorn` dependency is required for the HTTP server in the Docker container.

### Environment Variables

The Gemini agent requires a Google API key to function. Set the `GOOGLE_API_KEY` environment variable:

- For local testing: Export it in your shell: `export GOOGLE_API_KEY=your_api_key_here`
- For Docker: Pass it when running the container: `docker run -e GOOGLE_API_KEY=your_api_key_here ...`

---

## 3. Create the Dockerfile

Create a file named `Dockerfile` (with no file extension) in the project directory. This file contains instructions for Docker to build the container image.

### Dockerfile Content:

```dockerfile
# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the MCP server script to the container
COPY 8_mcp_docker_server.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for reports
RUN mkdir -p /app/reports

# Expose the port the MCP server will run on
EXPOSE 1923

# Default command to run the MCP server
CMD ["python", "8_mcp_docker_server.py"]
```

### Detailed Explanation of Each Line:

- **`FROM python:3.10-slim`**: This specifies the base image. We're using Python 3.10 in a slim version (smaller size) from Docker Hub. This provides the Python runtime needed for our scripts.
- **`WORKDIR /app`**: Sets the working directory inside the container to `/app`. All subsequent commands will run from this directory, and files will be copied here.

- **`COPY 8_mcp_docker_server.py /app/`**: Copies the Docker-optimized MCP server script from your host machine to the `/app` directory in the container.
- **`COPY requirements.txt /app/`**: Copies the dependencies file to the container.

- **`RUN pip install --no-cache-dir -r requirements.txt`**: Installs the Python packages listed in `requirements.txt`. The `--no-cache-dir` flag reduces the image size by not storing cache files.

- **`RUN mkdir -p /app/reports`**: Creates the `reports` directory inside the container where generated reports will be saved.

- **`EXPOSE 1923`**: Informs Docker that the container will listen on port 1923. This is for documentation; it doesn't actually open the port (that's done with `-p` when running).

- **`CMD ["python", "8_mcp_docker_server.py"]`**: Specifies the default command to run when the container starts. This runs the Docker-optimized MCP server script using Python.

### Tips for Beginners:

- **File Naming**: The file must be named exactly `Dockerfile` (capital D, no extension). Docker looks for this name by default.
- **Location**: Place it in the same directory as your Python scripts and `requirements.txt`.
- **Editing**: Use a plain text editor (e.g., Notepad, VS Code) to create the file. Do not use Word or rich text editors.
- **Why Docker?**: This file automates the setup of a consistent environment, so your app runs the same way everywhere, without needing to install dependencies manually on each machine.

---

## 4. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t arxiv-mcp-server .
```

This creates a Docker image named `arxiv-mcp-server`.

---

## 5. Run the MCP Server in a Container

To run the MCP server in a Docker container, use the following command:

```bash
docker run -d --name mcp-arxiv-server -p 1923:1923 -v ${PWD}/reports:/app/reports arxiv-mcp-server
```

**Note for Windows PowerShell**: Use `${PWD}` instead of `$(pwd)` for the current directory path.

### Explanation:

- **`--name mcp-arxiv-server`**: Assigns a custom name to the container (instead of a random name like "condescending_wright")
- **`-d`**: Runs the container in detached mode (in the background)
- **`-p 1923:1923`**: Maps port 1923 of the container to port 1923 on the host.
- **`-v ${PWD}/reports:/app/reports`**: Maps the `reports` directory inside the container to the `reports` directory on the host, ensuring that generated reports are accessible outside the container.

### About Container Naming:

Docker assigns random names to containers when you don't specify one (like "condescending_wright", "clever_haibt", etc.). While this works, using custom names makes it easier to:

- **Identify containers**: `docker ps` shows meaningful names instead of random ones
- **Manage containers**: `docker stop mcp-arxiv-server` is clearer than `docker stop condescending_wright`
- **Reference in scripts**: Custom names are more reliable in automation

**Tip**: Always use `--name` when running containers for production or long-term use!

---

## 6. Test the MCP Server

Since the MCP server is now running in a Docker container, the testing approach differs from local testing. Here are the correct methods to test your containerized server:

### Using `npx @modelcontextprotocol/inspector` (Recommended):

The MCP inspector can connect to your Dockerized server using StreamableHTTP transport. Run the following command:

```bash
npx @modelcontextprotocol/inspector --transport streamable-http --url http://localhost:1923
```

This will connect to the MCP server running in the Docker container on port 1923 and display all available tools and their metadata.

**Note**: Make sure your Docker container is running (from Step 5) before running this command.

### Alternative Testing Methods:

#### 1. Using `curl` for Basic Connectivity:

Test if the server is responding (note: this will show expected errors for MCP protocol):

```bash
curl http://localhost:1923
```

**Expected Response** (indicating the server is working correctly):

```
{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Not Acceptable: Client must accept text/event-stream"}}
```

These errors are **normal** - they show the server is running and properly rejecting invalid requests (which is good behavior for MCP servers).

#### 2. Local Testing (Before Docker):

If you want to test the server locally before containerizing it, use the original stdio version:

```bash
fastmcp run 4_mcp_server.py:mcp
```

**Important**: This command runs the server locally with stdio transport and won't work when the server is in Docker. Use the inspector method above for Docker testing.

### Troubleshooting Connection Issues:

- **Connection Refused**: Ensure the Docker container is running with `docker ps`
- **Port Issues**: Verify the port mapping with `docker ps` (should show `0.0.0.0:1923->1923/tcp`)
- **Firewall**: Make sure port 1923 is not blocked by your firewall
- **Container Logs**: Check container logs with `docker logs <container_id>` for any server errors

---

## 7. Run the Gemini Agent Locally (Connecting to Dockerized MCP Server)

Since the MCP server is running in a Docker container, you can run the Gemini agent locally on your host machine and connect it to the containerized server.

### Prerequisites for Local Agent:

- Ensure Python 3.10+ is installed on your host.
- Install dependencies: `pip install -r requirements.txt`
- Set the Google API key: `export GOOGLE_API_KEY=your_api_key_here`

### Understanding the Server Files:

- **`4_mcp_server.py`**: Original version with stdio transport for local development
- **`8_mcp_docker_server.py`**: Docker-optimized version with HTTP transport for containerization

The Docker version (`8_mcp_docker_server.py`) includes:

- HTTP server setup using FastMCP's `create_streamable_http_app()`
- Uvicorn ASGI server for running the HTTP application
- Proper host binding (`0.0.0.0`) for container networking

### Modify the Gemini Agent for Network Connection

The current agent code loads the MCP server module directly. To connect to the Dockerized server, modify `6_mcp_gemini_agent.py` to use a network connection.

**Updated `9_mcp_docker_gemini_agent.py` (Current Implementation)**:

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from google import genai
import asyncio

# Connect to the MCP server running in Docker on localhost:1923
# For HTTP transport, we need to create a StreamableHttpTransport
transport = StreamableHttpTransport("http://localhost:1923")
mcp_client = Client(transport)
gemini_client = genai.Client()

async def create_gemini_agent():
    """
    Creates and returns a Gemini chat agent with access to MCP tools.

    Returns:
        chat (genai.aio.chats.Chat): The Gemini chat object configured with MCP tools.
    """
    try:
        # Note: MCP client context is now managed in main() function
        # Save the existing prompts as samples
        tools_list = await mcp_client.list_tools()


        system_instruction = (
            "You are an assistant with access to MCP tools. Use them to answer user queries. "
            f"The tools: {tools_list}"
        )

        chat = gemini_client.aio.chats.create(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],
                system_instruction=system_instruction
            ),
        )
        return chat

# ... rest of the code remains the same
```

**Note**: FastMCP supports HTTP transport for network connections, as demonstrated by the MCP inspector connection method. The example code above shows how to connect to the Dockerized server.

### Run the Agent Locally

With the MCP server running in Docker (from Step 5), run the agent on your host:

```bash
python 9_mcp_docker_gemini_agent.py
```

This setup allows the agent to connect to the Dockerized MCP server over the network.

---

## 8. Accessing Generated Reports

All reports generated by the MCP server or Gemini agent will be saved in the `reports` directory inside the container. Since this directory is mapped to the host, you can access the reports directly from the `reports` directory on your host machine.

---

## 9. Stopping the Container

To stop the running container, use the following command:

```bash
docker ps
```

Find the container ID and stop it:

```bash
docker stop <container_id>
```

---

## 11. Troubleshooting

### Common Issues:

- **"docker: invalid reference format"**:

  - This often occurs on Windows PowerShell due to incorrect path syntax. Use `${PWD}` instead of `$(pwd)` for the current directory in volume mounts.

- **Random container names**:

  - Docker assigns random names when you don't specify `--name`. Use `--name your-container-name` for easier management.
  - Example: `docker run -d --name mcp-arxiv-server ...`

- **"Not Acceptable: Client must accept text/event-stream" or "Bad Request: Missing session ID"**:

  - These are **expected responses** from a working MCP server. They indicate the server is running correctly and rejecting invalid requests (which is good behavior).
  - Use the MCP inspector for proper testing: `npx @modelcontextprotocol/inspector --transport streamable-http --url http://localhost:1923`

- **Agent Cannot Connect to Dockerized Server**:

  - Ensure the MCP server container is running and accessible on `localhost:1923`.
  - Test the connection using the MCP inspector: `npx @modelcontextprotocol/inspector --transport streamable-http --url http://localhost:1923`
  - Verify the container's port mapping with `docker ps` (should show `0.0.0.0:1923->1923/tcp`).
  - Check container logs for any server errors: `docker logs <container_id>`.

- **API Key Errors**:

  - Ensure the `GOOGLE_API_KEY` is set correctly on the host when running the agent locally.

- **Port Already in Use**:

  - If port 1923 is busy, change it to another port (e.g., `-p 1924:1923`).

- **Reports Not Saving**:
  - Check that the `reports` directory exists on the host and has write permissions.

If you encounter other issues, check the Docker logs with `docker logs <container_id>`.

---

## Conclusion

By following this guide, you can containerize and run the MCP server and Gemini agent in Docker. This setup ensures portability, scalability, and easy access to generated reports.

**Important Notes**:

- **File Structure**:
  - Use `4_mcp_server.py` for local development with stdio transport
  - Use `8_mcp_docker_server.py` for Docker deployment with HTTP transport
- Ensure you have a valid Google API key for the Gemini agent.
- The MCP server and Gemini agent are designed to work together; running the agent will internally connect to the MCP server.
- For production use, consider securing the API key and using Docker secrets or environment files.
- The Docker container exposes the MCP server on port 1923 with HTTP transport, allowing external connections from the local Gemini agent.
