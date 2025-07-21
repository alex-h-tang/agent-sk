from typing import List, Dict, Any
from fastmcp import FastMCP

class ProductsPluginLogic:
    """Contains the business logic for product-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    async def list_products(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N products from Dataverse."""
        odata_query = f"$top={top}"
        return await self.dv.query("products", odata_query)

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        """Retrieve a single product by its ID."""
        return await self.dv.retrieve("products", product_id)

def create_products_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Products 'plugin' server."""
    products_mcp = FastMCP(name="ProductsPlugin")
    plugin_logic = ProductsPluginLogic(dv_client)

    products_mcp.tool(plugin_logic.list_products)
    products_mcp.tool(plugin_logic.get_product)

    return products_mcp
