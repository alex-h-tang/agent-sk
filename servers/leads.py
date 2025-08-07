from typing import List, Dict, Any
from fastmcp import FastMCP

class LeadsPluginLogic:
    """Contains the business logic for lead-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_leads(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N leads from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("leads", odata_query)

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """Retrieve a single lead by its ID."""
        return self.dv.retrieve("leads", lead_id)

    def inspect_lead_fields(self) -> List[str]:
        """Return the columns for a lead record."""
        records = self.dv.query("leads", "$top=1")
        return list(records[0].keys()) if records else []

def create_leads_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Leads 'plugin' server."""
    leads_mcp = FastMCP(name="LeadsPlugin")
    plugin_logic = LeadsPluginLogic(dv_client)

    leads_mcp.tool(plugin_logic.list_leads)
    leads_mcp.tool(plugin_logic.get_lead)
    leads_mcp.tool(plugin_logic.inspect_lead_fields)

    return leads_mcp
