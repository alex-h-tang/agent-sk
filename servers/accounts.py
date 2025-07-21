from typing import Optional, Literal, List, Dict, Any
from fastmcp import FastMCP

class AccountsPluginLogic:
    """Contains the business logic for account-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    async def list_accounts(
        self,
        top: int = 5,
        region: Optional[str] = None,
        status: Optional[Literal[0, 1]] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[Literal["asc", "desc"]] = None
    ) -> List[Dict[str, Any]]:
        """
        List the top N accounts from Dataverse. Optional filters for region, status, and sorting.
        Status must be a numeric code: 0 for active, 1 for inactive.
        If sort_by is provided, sort_direction must also be provided as 'asc' or 'desc'.
        """
        clauses = []
        if region:
            clauses.append(f"cs_accountsalesregion eq '{region}'")
        if status is not None:
            clauses.append(f"statecode eq {status}")

        filter_str = ""
        if clauses:
            filter_str = "$filter=" + " and ".join(clauses)

        order_str = ""
        if sort_by and sort_direction:
            order_str = f"$orderby={sort_by} {sort_direction}"

        parts = [f"$top={top}"]
        if filter_str:
            parts.append(filter_str)
        if order_str:
            parts.append(order_str)

        odata_query = "&".join(parts)
        return await self.dv.query("accounts", odata_query)

    async def get_account(self, account_id: str) -> Dict[str, Any]:
        """Retrieve a single account by its ID."""
        return await self.dv.retrieve("accounts", account_id)

    async def inspect_account_fields(self) -> List[str]:
        """Return the columns for an account record."""
        records = await self.dv.query("accounts", "$top=1")
        return list(records[0].keys()) if records else []

def create_accounts_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Accounts 'plugin' server."""
    accounts_mcp = FastMCP(name="AccountsPlugin")
    plugin_logic = AccountsPluginLogic(dv_client)

    accounts_mcp.tool(plugin_logic.list_accounts)
    accounts_mcp.tool(plugin_logic.get_account)
    accounts_mcp.tool(plugin_logic.inspect_account_fields)

    return accounts_mcp
