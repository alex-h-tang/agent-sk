from typing import List, Dict, Any, Optional, Literal
from fastmcp import FastMCP

class OpportunitiesPluginLogic:
    """Contains the business logic for opportunity-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_opportunities(
            self, 
            top: int = 5, 
            region: Optional[str] = None,
            status: Optional[Literal[0, 1, 2]] = None,
            owner_id: Optional[str] = None,
            min_revenue: Optional[float] = None,
            max_revenue: Optional[float] = None,
            est_close_date_start: Optional[str] = None,
            est_close_date_end: Optional[str] = None,
            sort_by: Optional[str] = None,
            sort_direction: Optional[Literal["asc", "desc"]] = None
            ) -> List[Dict[str, Any]]:
        """
        List the top N opportunities from Dataverse. 
        Optional filters for est_revenue, status, and sorting.
        Status must be a numeric code: 0 for open, 1 for won, 2 for lost.
        If region is provided, it filters by the specified region, must be one of the following: NAR, CALA, MEA, Europe, or APAC.
        If sort_by is provided, sort_direction must also be provided as 'asc' or 'desc'.
        """
        # TODO: implement est_revenue filtering
        clauses = []
        if region:
            clauses.append(f"cs_accountsalesregion eq '{region}'")
        if status:
            clauses.append(f"statecode eq {status}")
        if owner_id:
            clauses.append(f"_ownerid_value eq {owner_id}")
        if min_revenue:
            clauses.append(f"estimatedvalue ge {min_revenue}")
        if max_revenue:
            clauses.append(f"estimatedvalue le {max_revenue}")
        if est_close_date_start:
            clauses.append(f"estimatedclosedate ge {est_close_date_start}")
        if est_close_date_end:
            clauses.append(f"estimatedclosedate le {est_close_date_end}")

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
        return self.dv.query("opportunities", odata_query)
    
    def get_opportunity_account(self, opportunity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the parent account (company) record associated with a specific opportunity.
        Returns the account record or None if no account is linked.
        """
        odata_query = "$expand=parentaccountid"
        opportunity = self.dv.retrieve("opportunities", opportunity_id, odata_query)
        if not opportunity or "parentaccountid" not in opportunity:
            return None
        return opportunity.get("parentaccountid")

    def get_opportunity_contact(self, opportunity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the primary contact (person) record associated with a specific opportunity.
        Returns the contact record or None if no contact is linked.
        """
        odata_query = "$expand=parentcontactid"
        opportunity = self.dv.retrieve("opportunities", opportunity_id, odata_query)
        if not opportunity or "parentcontactid" not in opportunity:
            return None
        return opportunity.get("parentcontactid")
    
    

    def get_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """Retrieve a single opportunity by its ID."""
        return self.dv.retrieve("opportunities", opportunity_id)

    # def list_opportunities_by_owner(self, user_id: str) -> List[Dict[str, Any]]:
    #     """List opportunities owned by a specific user, based on user_id."""
    #     odata_query = f"$filter=_ownerid_value eq {user_id}"
    #     return self.dv.query("opportunities", odata_query)

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
    opportunities_mcp.tool(plugin_logic.get_opportunity_account)
    opportunities_mcp.tool(plugin_logic.get_opportunity_contact)
    # opportunities_mcp.tool(plugin_logic.list_opportunities_by_owner)
    opportunities_mcp.tool(plugin_logic.inspect_opportunity_fields)

    return opportunities_mcp
