from typing import List, Dict, Any
from fastmcp import FastMCP

class OpportunitiesPluginLogic:
    """Contains the business logic for opportunity-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_opportunities(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N opportunities from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("opportunities", odata_query)

    def get_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """Retrieve a single opportunity by its ID."""
        return self.dv.retrieve("opportunities", opportunity_id)

    def list_opportunities_by_owner(self, user_id: str) -> List[Dict[str, Any]]:
        """List opportunities owned by a specific user, based on user_id."""
        odata_query = f"$filter=_ownerid_value eq {user_id}"
        return self.dv.query("opportunities", odata_query)

    def inspect_opportunity_fields(self) -> List[str]:
        """Return the columns for an opportunity record."""
        records = self.dv.query("opportunities", "$top=1")
        return list(records[0].keys()) if records else []

def create_opportunities_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Opportunities 'plugin' server."""
    opportunities_mcp = FastMCP(name="OpportunitiesPlugin")
    plugin_logic = OpportunitiesPluginLogic(dv_client)

    opportunities_mcp.tool(plugin_logic.list_opportunities)
    opportunities_mcp.tool(plugin_logic.get_opportunity)
    opportunities_mcp.tool(plugin_logic.list_opportunities_by_owner)
    opportunities_mcp.tool(plugin_logic.inspect_opportunity_fields)

    return opportunities_mcp
