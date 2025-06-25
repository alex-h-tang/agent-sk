import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from config import create_dataverse_client
from plugins.accounts_plugin import AccountsPlugin
from plugins.opportunities_plugin import OpportunitiesPlugin
from plugins.products_plugin import ProductsPlugin

load_dotenv()

async def build_kernel() -> Kernel:
    k = Kernel()

    k.add_service(
        AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    )

    dv = create_dataverse_client(os.getenv("DATAVERSE_URL"))

    k.add_plugin(AccountsPlugin(dv), plugin_name="Accounts")
    k.add_plugin(OpportunitiesPlugin(dv), plugin_name="Opportunities")
    k.add_plugin(ProductsPlugin(dv), plugin_name="Products")

    return k

async def main():
    kernel = await build_kernel()

    result = await kernel.invoke(
        plugin_name="Accounts",
        function_name="list_accounts",
        top=3
    )

    accounts = result.value
    print("Top 3 accounts:", accounts)

if __name__ == "__main__":
    asyncio.run(main())
