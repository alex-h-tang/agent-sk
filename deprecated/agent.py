import asyncio
import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
# from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.functions import KernelArguments

load_dotenv()

async def run_agent():
    kernel = Kernel()

    kernel.add_service(AzureChatCompletion(
        service_id="chat",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    ))

    mcp_plugin = MCPSsePlugin(
        name="DataverseServer",
        description="Dataverse-backed tools for sales",
        url="http://localhost:8000" 
    )

    kernel.add_plugin(mcp_plugin)

    agent = ChatCompletionAgent(
        service=kernel.get_service("chat"),
        name="SalesAssistant",
        instructions=(
            "You are a sales-data assistant. Use the right plugins to answer questions. "
            "When a request is made involving names, be sure to split the names up, and check if the substrings return results."
        ),
        plugins=[mcp_plugin],
        arguments=KernelArguments()
    )

    thread = None
    print("How can I help you today?")

    while True:
        user_input = input().strip()
        if not user_input or user_input.lower() == "exit":
            break

        if thread is None:
            response = await agent.get_response(user_input)
        else:
            response = await agent.get_response(user_input, thread=thread)

        print(response.content)
        thread = response.thread

if __name__ == "__main__":
    asyncio.run(run_agent())
