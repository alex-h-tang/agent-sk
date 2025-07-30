from typing import List, Dict, Any
from fastmcp import FastMCP

class CompetitorsPluginLogic:
    """Contains the business logic for competitor-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_competitors(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N competitors from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("competitors", odata_query)

    def get_competitor(self, competitor_id: str) -> Dict[str, Any]:
        """Retrieve a single competitor by its ID."""
        return self.dv.retrieve("competitors", competitor_id)

    def inspect_competitor_fields(self) -> List[str]:
        """Return the columns for a competitor record."""
        records = self.dv.query("competitors", "$top=1")
        return list(records[0].keys()) if records else []

def create_competitors_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the competitors 'plugin' server."""
    competitors_mcp = FastMCP(name="CompetitorsPlugin")
    plugin_logic = CompetitorsPluginLogic(dv_client)

    competitors_mcp.tool(plugin_logic.list_competitors)
    competitors_mcp.tool(plugin_logic.get_competitor)
    competitors_mcp.tool(plugin_logic.inspect_competitor_fields)

    return competitors_mcp
