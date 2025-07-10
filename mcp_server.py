import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

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