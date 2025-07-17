import os
import asyncio
from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
import inspect

from config import create_dataverse_client
from plugins.accounts_plugin import AccountsPlugin
from plugins.opportunities_plugin import OpportunitiesPlugin
from plugins.products_plugin import ProductsPlugin
from plugins.leads_plugin import LeadsPlugin
from plugins.orders_plugin import OrdersPlugin
from plugins.quotes_plugin import QuotesPlugin
from plugins.users_plugin import UsersPlugin

load_dotenv()

@dataclass
class AppContext:
    dv_client: object

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    # print("Initializing Dataverse client")
    dv_client = create_dataverse_client(os.getenv("DATAVERSE_URL"))
    yield AppContext(dv_client=dv_client)
    # print("Server shutting down")

mcp = FastMCP("DataverseServer", lifespan=app_lifespan)

def register_plugins(mcp_server: FastMCP, plugin_classes: list):
    for plugin_class in plugin_classes:
        for method_name, method_object in inspect.getmembers(plugin_class, predicate=inspect.isfunction):
            if method_name.startswith('_'):
                continue

            def create_tool_function(p_class, m_name):

                original_method = getattr(p_class, m_name)

                async def tool_function(**kwargs):
                    ctx = get_context()
                    dv_client = ctx.lifespan_context.dv_client
                    plugin_instance = p_class(dv_client)
                    result = getattr(plugin_instance, m_name)(**kwargs)
                    if inspect.isawaitable(result):
                        return await result
                    return result

                original_sig = inspect.signature(original_method)
                params_without_self = [p for name, p in original_sig.parameters.items() if name != 'self']
                tool_function.__signature__ = original_sig.replace(parameters=params_without_self)
                tool_function.__doc__ = inspect.getdoc(original_method)
                
                return tool_function

            tool_func = create_tool_function(plugin_class, method_name)
            tool_name = f"{plugin_class.__name__}_{method_name}"
            
            mcp_server.tool(name=tool_name)(tool_func)

plugins = [
    AccountsPlugin,
    OpportunitiesPlugin,
    ProductsPlugin,
    LeadsPlugin,
    OrdersPlugin,
    QuotesPlugin,
    UsersPlugin
]

register_plugins(mcp, plugins)

# async def print_tools():
#     tools = await mcp.list_tools()
#     for tool_name in tools:
#         print("  -", tool_name)

# asyncio.run(print_tools())

# app = mcp.sse_app

# if __name__ == "__main__":
#     mcp.run()