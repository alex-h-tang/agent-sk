import os
import sys
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv

from fastmcp import FastMCP

from config import create_dataverse_client

from servers.accounts import create_accounts_plugin_server
from servers.leads import create_leads_plugin_server
from servers.opportunities import create_opportunities_plugin_server
from servers.orders import create_orders_plugin_server
from servers.products import create_products_plugin_server
from servers.quotes import create_quotes_plugin_server
from servers.users import create_users_plugin_server

load_dotenv()


@dataclass
class AppState:
    """A dataclass to hold shared application state."""

    dv_client: object


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppState]:
    """
    Manages the server's startup and shutdown lifecycle.
    Initializes the Dataverse client and mounts all plugins.
    """
    # print("initializing Dataverse client")
    dv_client = create_dataverse_client(os.getenv("DATAVERSE_URL"))

    # print("mounting plugins")
    server.mount(create_accounts_plugin_server(dv_client), prefix="Accounts")
    server.mount(create_leads_plugin_server(dv_client), prefix="Leads")
    server.mount(create_opportunities_plugin_server(dv_client), prefix="Opportunities")
    server.mount(create_orders_plugin_server(dv_client), prefix="Orders")
    server.mount(create_products_plugin_server(dv_client), prefix="Products")
    server.mount(create_quotes_plugin_server(dv_client), prefix="Quotes")
    server.mount(create_users_plugin_server(dv_client), prefix="Users")
    # print("plugins mounted")

    yield AppState(dv_client=dv_client)
    # print("server shutting down")


mcp = FastMCP(
    name="DataverseMCP",
    lifespan=app_lifespan,
)


@mcp.tool
def get_server_status() -> str:
    """Returns the operational status of the main server."""
    return "OK"


if __name__ == "__main__":
    # print("Starting FastMCP server on http://0.0.0.0:8000")
    if "--stdio" in sys.argv:
        mcp.run()
    else:
        mcp.run(transport="http")


@mcp.custom_route("/", methods=["GET"])
async def root(request: Request) -> JSONResponse:
    return JSONResponse({"message": "Server is running"})

# maybe fastapi instead
app = mcp.http_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)