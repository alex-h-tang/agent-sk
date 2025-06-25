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
