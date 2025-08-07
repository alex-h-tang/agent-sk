from typing import Optional, Literal, List, Dict, Any
from fastmcp import FastMCP


class AccountsPluginLogic:
    """Contains the business logic for account-related operations."""

    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_accounts(
            self,
            top: int = 5,
            region: Optional[str] = None,
            status: Optional[Literal[0, 1]] = None,
            business_unit_id: Optional[str] = None,
            sort_by: Optional[str] = None,
            sort_direction: Optional[Literal["asc", "desc"]] = None
    ) -> List[Dict[str, Any]]:
        """
        List the top N accounts from Dataverse. Optional filters for region, status, business unit, and sorting.
        If region is provided, it filters by the specified region, must be one of the following: NAR, CALA, MEA, Europe, or APAC.
        Status must be a numeric code: 0 for active, 1 for inactive.
        If business_unit_id is provided, it filters accounts by the owning business unit's GUID.
        If sort_by is provided, sort_direction must also be provided as 'asc' or 'desc'.
        """
        clauses = []
        if region:
            clauses.append(f"cs_accountsalesregion eq '{region}'")
        if status:
            clauses.append(f"statecode eq {status}")
        if business_unit_id:
            clauses.append(f"_owningbusinessunit_value eq {business_unit_id}")

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
        return self.dv.query("accounts", odata_query)

    def get_account(
            self,
            account_id: str
    ) -> Dict[str, Any]:
        """Retrieve a single account by its ID."""
        return self.dv.retrieve("accounts", account_id)

    def search_accounts_by_name(
            self,
            search_query: str,
            top: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Performs a fuzzy search for accounts, based off a query keyword (for the account name), tolerating typos and misspellings.
        Returns top N results are ranked by relevance.
        """
        search_endpoint = "/api/search/v1.0/query"
        payload = {
            "search": search_query,
            "entities": ["account"],
            "top": top,
            "fuzzy": True
        }
        response = self.dv.post(search_endpoint, payload)
        # records = [item.get('@search.entity')
        #            for item in response.get('value', []) if item.get('@search.entity')]
        # return records
        return response

    def list_account_opportunities(
            self,
            account_id: str,
            status: Optional[Literal[0, 1, 2]] = None
    ) -> List[Dict[str, Any]]:
        """
        Lists all sales opportunities for a specific account.
        Can optionally filter by opportunity status (0=Open, 1=Won, 2=Lost).
        """
        filter_clauses = [f"_parentaccountid_value eq {account_id}"]

        if status is not None:
            filter_clauses.append(f"statecode eq {status}")

        filter_str = " and ".join(filter_clauses)
        odata_query = f"$filter={filter_str}"

        return self.dv.query("opportunities", odata_query)
    
    def list_account_orders(
            self,
            account_id: str,
            status: Optional[Literal[0, 1, 2, 3, 4]] = None
    ) -> List[Dict[str, Any]]:
        """
        Lists all sales orders for a specific account.
        Can optionally filter by order status (0=Active, 1=Submitted, 2=Cancelled, 3=Fulfilled, 4=Invoiced).
        """
        filter_clauses = [f"_parentaccountid_value eq {account_id}"]
        # TODO: all of it lol

    def get_account_deal_summary(
            self,
            account_id: str
    ) -> Dict[str, Any]:
        """
        Summarizes open, won, and lost opportunities and revenues for a given account's GUID.
        """
        summary = {
            "open_revenue": 0,
            "open_deal_count": 0,
            "won_revenue": 0,
            "won_deal_count": 0,
            "lost_revenue": 0,
            "lost_deal_count": 0
        }

        open_query = (
            f"$apply=filter(_parentaccountid_value eq {account_id} and statecode eq 0)/"
            f"aggregate($count as open_deal_count, estimatedvalue with sum as open_revenue)"
        )
        
        won_query = (
            f"$apply=filter(_parentaccountid_value eq {account_id} and statecode eq 1)/"
            f"aggregate($count as won_deal_count, actualvalue with sum as won_revenue)"
        )

        lost_query = (
            f"$apply=filter(_parentaccountid_value eq {account_id} and statecode eq 2)/"
            f"aggregate($count as lost_deal_count, actualvalue with sum as lost_revenue)"
        )

        open_result = self.dv.query("opportunities", open_query)
        if open_result:
            summary.update(open_result[0])

        won_result = self.dv.query("opportunities", won_query)
        if won_result:
            summary.update(won_result[0])

        lost_result = self.dv.query("opportunities", lost_query)
        if lost_result:
            summary.update(lost_result[0])

        return summary
        

    def inspect_account_fields(self) -> List[str]:
        """Return the columns for an account record."""
        records = self.dv.query("accounts", "$top=1")
        return list(records[0].keys()) if records else []


def create_accounts_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Accounts 'plugin' server."""
    accounts_mcp = FastMCP(name="AccountsPlugin")
    plugin_logic = AccountsPluginLogic(dv_client)

    accounts_mcp.tool(plugin_logic.list_accounts)
    accounts_mcp.tool(plugin_logic.get_account)
    accounts_mcp.tool(plugin_logic.search_accounts_by_name)
    accounts_mcp.tool(plugin_logic.list_account_opportunities)
    accounts_mcp.tool(plugin_logic.get_account_deal_summary)
    accounts_mcp.tool(plugin_logic.inspect_account_fields)

    return accounts_mcp
