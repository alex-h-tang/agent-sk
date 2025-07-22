import asyncio
import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.contents import ChatHistory

load_dotenv()

async def run_agent():
    """
    Initializes and runs a Semantic Kernel agent that connects to a local
    FastMCP server script via STDIO and uses its tools to answer questions.
    """
    kernel = Kernel()

    kernel.add_service(AzureChatCompletion(
        service_id="chat",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    ))

    async with MCPStdioPlugin(
        name="DataverseServer",
        description="A server with tools for accessing sales data from Dataverse.",
        command="python",
        args=["fastmcp_server.py", "--stdio"]
    ) as mcp_plugin:

        kernel.add_plugin(mcp_plugin)
        print("Successfully launched and connected to MCP server via stdio.")

        agent = ChatCompletionAgent(
            service=kernel.get_service("chat"),
            kernel=kernel,
            name="SalesAssistant"
        )

        chat_history = ChatHistory(
            system_message=(
                "You are a helpful sales data assistant. Your job is to answer user questions "
                "by selecting and using the correct tools from the DataverseServer plugin. "
                "You must use the tools to answer questions about data. Do not ask for clarification "
                "if a tool can provide the answer. Be precise."
                "WHENEVER YOU RUN INTO AN ERROR, RETURN THE ERROR MESSAGE AS PART OF YOUR RESPONSE."
            )
        )
        
        print("\nSales Assistant is ready. Type 'exit' to end the session.")
        print("How can I help you today?")

        while True:
            try:
                user_input = input("> ").strip()
                if not user_input or user_input.lower() == "exit":
                    print("Ending session. Goodbye!")
                    break

                chat_history.add_user_message(user_input)

                full_response = ""
                print("Sales Assistant: ", end="", flush=True)
                async for message in agent.invoke(chat_history):
                    if message.role == "tool":
                        print(f"\n...Calling tool: {message.name}({message.tool_input}) -> {message.content}\n")
                        print("Sales Assistant: ", end="", flush=True)
                    elif message.content:
                        content_str = str(message.content)
                        print(content_str, end="", flush=True)
                        full_response += content_str
                    
                print()

                if full_response:
                    chat_history.add_assistant_message(full_response)

            except Exception as e:
                print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run_agent())
