import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments

from plugins.accounts_plugin import AccountsPlugin
from plugins.opportunities_plugin import OpportunitiesPlugin
from plugins.products_plugin import ProductsPlugin
from config import create_dataverse_client

async def run_agent():
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(
        service_id="chat",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    ))
    
    dv = create_dataverse_client(os.getenv("DATAVERSE_URL"))

    accounts = AccountsPlugin(dv)
    opps = OpportunitiesPlugin(dv)
    products = ProductsPlugin(dv)

    agent = ChatCompletionAgent(
        service=kernel.get_service("chat"),
        name="SalesAssistant",
        instructions="You are a sales-data assistant. Use the right plugins to answer questions.",
        plugins=[accounts, opps, products],
        arguments=KernelArguments()
    )

    # test
    answer = await agent.get_response("Show me the top 3 accounts")
    print(answer.content)

if __name__ == "__main__":
    asyncio.run(run_agent())
