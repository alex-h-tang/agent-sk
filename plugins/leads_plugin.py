from semantic_kernel.functions import kernel_function

class LeadsPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_leads(self, top: int = 5) -> list[dict]:
        """
        List the top N leads from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("leads", odata_query)

    @kernel_function
    async def get_lead(self, lead_id: str) -> dict:
        """
        Retrieve a single lead by its ID.
        """
        return self.dv.retrieve("leads", lead_id)