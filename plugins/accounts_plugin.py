from typing import Optional
from semantic_kernel.functions import kernel_function

class AccountsPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_accounts(self, top: int = 5, region: Optional[str] = None, status: Optional[str] = None, sort_by: Optional[str] = None, sort_direction: Optional[str] = None) -> list[dict]:
        """
        List the top N accounts from Dataverse. Optional filters for region, status, and sorting. Status must be numeric code, 0 for active, 1 for inactive. If sort_by is provided, sort_direction must also be provided as 'asc' or 'desc'.
        """
        clauses = []
        if region:
            clauses.append(f"cs_accountsalesregion eq '{region}'")
        if status:
            clauses.append(f"statecode eq {status}")

        filter_str = ""
        if clauses:
            filter_str = "$filter=" + " and ".join(clauses)

        order_str = ""
        if sort_by:
            order_str = f"$orderby={sort_by} {sort_direction}"

        parts = [f"$top={top}"]
        if filter_str:
            parts.append(filter_str)
        if order_str:
            parts.append(order_str)

        odata_query = "&".join(parts)
        return self.dv.query("accounts", odata_query)

    @kernel_function
    async def get_account(self, account_id: str) -> dict:
        """
        Retrieve a single account by its ID.
        """
        return self.dv.retrieve("accounts", account_id)
    
    @kernel_function
    async def inspect_account_fields(self) -> list[str]:
        """
        Return the columns for an opportunity record
        """
        record = self.dv.query("accounts", "$top=1")[0]
        return list(record.keys())

