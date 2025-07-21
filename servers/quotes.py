from typing import List, Dict, Any
from fastmcp import FastMCP

class QuotesPluginLogic:
    """Contains the business logic for quote-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    async def list_quotes(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N quotes from Dataverse."""
        odata_query = f"$top={top}"
        return await self.dv.query("quotes", odata_query)

    async def get_quote(self, quote_id: str) -> Dict[str, Any]:
        """Retrieve a single quote by its ID."""
        return await self.dv.retrieve("quotes", quote_id)

    async def inspect_quote_fields(self) -> List[str]:
        """Return the columns for a quote record."""
        records = await self.dv.query("quotes", "$top=1")
        return list(records[0].keys()) if records else []

def create_quotes_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Quotes 'plugin' server."""
    quotes_mcp = FastMCP(name="QuotesPlugin")
    plugin_logic = QuotesPluginLogic(dv_client)

    quotes_mcp.tool(plugin_logic.list_quotes)
    quotes_mcp.tool(plugin_logic.get_quote)
    quotes_mcp.tool(plugin_logic.inspect_quote_fields)

    return quotes_mcp
