import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
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

def register_plugins(mcp_server: FastMCP, plugin_classes):
    for plugin_class in plugin_classes:
        for method_name, method_object in inspect.getmembers(plugin_class, predicate=inspect.isfunction):
            if method_name.startswith('_'):
                continue
            def create_tool_executor(p_class, m_name):
                original_method = getattr(p_class, m_name)
                def tool_executor(**kwargs):
                    ctx = mcp_server.get_context()
                    dv_client = ctx.request_context.lifespan_context.dv_client
                    plugin_instance = p_class(dv_client)
                    return getattr(plugin_instance, m_name)(**kwargs)
                tool_executor.__signature__ = inspect.signature(original_method)
                tool_executor.__doc__ = inspect.getdoc(original_method)
                return tool_executor
            tool_function = create_tool_executor(plugin_class, method_name)
            tool_name = f"{plugin_class.__name__}_{method_name}"
            mcp_server.tool(name=tool_name)(tool_function)

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