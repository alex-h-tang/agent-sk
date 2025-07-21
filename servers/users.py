# plugins_mcp/users.py
from typing import List, Dict, Any
from fastmcp import FastMCP

class UsersPluginLogic:
    """Contains the business logic for user-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    async def list_users(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N users from Dataverse."""
        odata_query = f"$top={top}"
        return await self.dv.query("systemusers", odata_query)

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Retrieve a single user by their GUID."""
        return await self.dv.retrieve("systemusers", user_id)

    async def get_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Retrieve users by at least a substring of their name."""
        odata_query = f"$filter=contains(fullname, '{name}')"
        return await self.dv.query("systemusers", odata_query)

    async def get_direct_reports(self, manager: str) -> List[Dict[str, Any]]:
        """Retrieve users who report directly to a specified manager, based on manager GUID."""
        odata_query = f"$filter=_parentsystemuserid_value eq '{manager}'"
        return await self.dv.query("systemusers", odata_query)

    async def get_business_unit_by_id(self, business_unit_id: str) -> Dict[str, Any]:
        """Retrieve a business unit by its ID."""
        return await self.dv.retrieve("businessunits", business_unit_id)

    async def inspect_user_fields(self) -> List[str]:
        """Return the columns for a user record."""
        records = await self.dv.query("systemusers", "$top=1")
        return list(records[0].keys()) if records else []

def create_users_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Users 'plugin' server."""
    users_mcp = FastMCP(name="UsersPlugin")
    plugin_logic = UsersPluginLogic(dv_client)

    users_mcp.tool(plugin_logic.list_users)
    users_mcp.tool(plugin_logic.get_user)
    users_mcp.tool(plugin_logic.get_users_by_name)
    users_mcp.tool(plugin_logic.get_direct_reports)
    users_mcp.tool(plugin_logic.get_business_unit_by_id)
    users_mcp.tool(plugin_logic.inspect_user_fields)

    return users_mcp
