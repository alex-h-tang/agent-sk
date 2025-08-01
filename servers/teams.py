from typing import List, Dict, Any
from fastmcp import FastMCP

class TeamsPluginLogic:
    """Contains the business logic for team-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_teams(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N teams from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("teams", odata_query)

    def get_team(self, team_id: str) -> Dict[str, Any]:
        """Retrieve a single team by its team id."""
        return self.dv.retrieve("teams", team_id)

    def inspect_team_fields(self) -> List[str]:
        """Return the columns for an team record."""
        records = self.dv.query("teams", "$top=1")
        return list(records[0].keys()) if records else []

def create_teams_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the teams 'plugin' server."""
    teams_mcp = FastMCP(name="teamsPlugin")
    plugin_logic = TeamsPluginLogic(dv_client)

    teams_mcp.tool(plugin_logic.list_teams)
    teams_mcp.tool(plugin_logic.get_team)
    teams_mcp.tool(plugin_logic.inspect_team_fields)

    return teams_mcp
