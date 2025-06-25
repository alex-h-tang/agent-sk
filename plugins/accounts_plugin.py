from semantic_kernel.functions import kernel_function
class AccountsPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_accounts(self, top: int = 5) -> list[dict]:
        """
        List the top N accounts from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("accounts", odata_query)

    @kernel_function
    async def get_account(self, account_id: str) -> dict:
        """
        Retrieve a single account by its ID.
        """
        return self.dv.retrieve("accounts", account_id)
