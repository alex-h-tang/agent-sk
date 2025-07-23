from semantic_kernel.functions import kernel_function

class OrdersPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_orders(self, top: int = 5) -> list[dict]:
        """
        List the top N orders from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("salesorders", odata_query)

    @kernel_function
    async def get_order(self, order_number: str) -> dict:
        """
        Retrieve a single order by its order number.
        """
        return self.dv.retrieve("salesorders", order_number)
    
    @kernel_function
    async def inspect_order_fields(self) -> list[str]:
        """
        Return the columns for an order record.
        """
        record = self.dv.query("salesorders", "$top=1")[0]
        return list(record.keys())