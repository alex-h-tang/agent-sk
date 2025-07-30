from typing import List, Dict, Any, Optional, Literal
from fastmcp import FastMCP


class ProductsPluginLogic:
    """Contains the business logic for product-related operations."""

    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_products(
        self,
        top: int = 5,
        status: Optional[Literal[0, 1, 2, 3]] = None,
        min_list_price: Optional[float] = None,
        max_list_price: Optional[float] = None,
        min_current_cost: Optional[float] = None,
        max_current_cost: Optional[float] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[Literal["asc", "desc"]] = None
    ) -> List[Dict[str, Any]]:
        """
        List the top N products from Dataverse. Optional filter for status, pricing (how much product sells for), and sorting.
        Status must be a numeric code: 0 for active, 1 for retired, 2 for draft, 3 for under revision.
        If sort_by is provided, sort_direction must also be provided as 'asc' or 'desc'.
        """
        # TODO: actual implementation
        clauses = []
        if status:
            clauses.append(f"statecode eq {status}")
        if min_list_price:
            clauses.append(f"price ge {min_list_price}")
        if max_list_price:
            clauses.append(f"price le {max_list_price}")
        if min_current_cost:
            clauses.append(f"currentcost ge {min_current_cost}")
        if max_current_cost:
            clauses.append(f"currentcost le {max_current_cost}")

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
        return self.dv.query("products", odata_query)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Retrieve a single product by its ID."""
        return self.dv.retrieve("products", product_id)

    def get_product_details(
        self,
        product_id: Optional[str] = None,
        product_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve product details, such as cost, list price, quantity available, etc. for a product.
        Queriable by its unique ID (Dataverse GUID) OR by its product number (code within CommScope).
        """

        select_fields = ["productnumber", "name", "description", "price",
                         "standardcost", "quantityonhand", "stockvolume", 
                         "statecode", "cs_issalesenabled", "cs_productgroup",
                         "cs_itemtype"]
        select_query = f"$select={','.join(select_fields)}"

        if not product_id and not product_number:
            raise ValueError(
                "Either product_id or product_number must be provided.")

        elif product_id:
            product_data = self.dv.retrieve(
                "products", product_id, select_query)
            return product_data

        elif product_number:
            filter_query = f"$filter=productnumber eq '{product_number}'"
            odata_query = f"{filter_query}&{select_query}"
            results = self.dv.query("products", odata_query)
            return results[0] if results else {}

    def inspect_product_fields(self) -> List[str]:
        """Return the columns for a product record."""
        records = self.dv.query("products", "$top=1")
        return list(records[0].keys()) if records else []


def create_products_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Products 'plugin' server."""
    products_mcp = FastMCP(name="ProductsPlugin")
    plugin_logic = ProductsPluginLogic(dv_client)

    products_mcp.tool(plugin_logic.list_products)
    products_mcp.tool(plugin_logic.get_product)
    products_mcp.tool(plugin_logic.get_product_details)
    products_mcp.tool(plugin_logic.inspect_product_fields)

    return products_mcp
