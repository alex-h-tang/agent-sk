from semantic_kernel.functions import kernel_function

class ProductsPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client

    @kernel_function
    async def list_products(self, top: int = 5) -> list[dict]:
        """
        List the top N products from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("products", odata_query)

    @kernel_function
    async def get_product(self, product_id: str) -> dict:
        """
        Retrieve a single product by its ID.
        """
        return self.dv.retrieve("products", product_id)
