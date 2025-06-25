from semantic_kernel.functions import kernel_function

class OpportunitiesPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_opportunities(self, top: int = 5) -> list[dict]:
        """
        List the top N opportunities from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("opportunities", odata_query)

    @kernel_function
    async def get_opportunity(self, opportunity_id: str) -> dict:
        """
        Retrieve a single opportunity by its ID.
        """
        return self.dv.retrieve("opportunities", opportunity_id)

    # doesn't work 
    # @kernel_function
    # async def get_opportunity_by_account(self, account_id: str) -> list[dict]:
    #     """
    #     List opportunities associated with a specific account.
    #     """
    #     # odata_query = f"$filter=_customerid_value eq {account_id}"
    #     # return self.dv.query("opportunities", odata_query)
    #     params = {
    #         "$filter": f"_customerid_value eq {account_id}"
    #     }
    #     return self.dv.query_with_params("opportunities", params)
    
    @kernel_function
    async def inspect_opportunity_fields(self) -> list[str]:
        """
        Return the columns for an opportunity record
        """
        record = self.dv.query("opportunities", "$top=1")[0]
        return list(record.keys())
