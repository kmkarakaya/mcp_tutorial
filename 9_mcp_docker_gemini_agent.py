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
    except Exception as e:
        print(f"Failed to create Gemini agent: {e}")
        raise

async def main():
    """
    Main function to interact with the Gemini agent in a loop.
    """
    try:
        # Keep MCP client session open for the entire duration
        async with mcp_client:

            chat = await create_gemini_agent()
            print("Gemini agent is ready. Type 'exit' to quit.")
            
            while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Exiting the chat. Goodbye!")
                    break
                
                try:
                    response = await chat.send_message(user_input)
                    print("Gemini: ", response.text)
                except Exception as e:
                    print(f"Sorry, I encountered an error processing your message: {e}")
                    
    except Exception as e:
        print("Failed to connect to MCP server. Please ensure it's running on http://localhost:1923")

if __name__ == "__main__":
    asyncio.run(main())
    
    sample_prompts = [
    "list the available tools in the mcp server you can access",
    "prepare a report based on 3 latest papers published at arXiv website about the RAG and MCP security risks. Provide the detailed citations and URLs."
    ]