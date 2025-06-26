from semantic_kernel.functions import kernel_function

class QuotesPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_quotes(self, top: int = 5) -> list[dict]:
        """
        List the top N quotes from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("quotes", odata_query) 
    
    @kernel_function
    async def get_quote(self, quote_id: str) -> dict:
        """
        Retrieve a single quote by its ID.
        """
        return self.dv.retrieve("quotes", quote_id)
    
    