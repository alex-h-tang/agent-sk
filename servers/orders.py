from typing import List, Dict, Any
from fastmcp import FastMCP

class OrdersPluginLogic:
    """Contains the business logic for order-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_orders(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N orders from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("salesorders", odata_query)

    def get_order(self, order_number: str) -> Dict[str, Any]:
        """Retrieve a single order by its order number."""
        return self.dv.retrieve("salesorders", order_number)
    
    def get_orders_by_account(self, account_id: str) -> List[Dict[str, Any]]:
        """Retrieve orders associated with a specific account ID."""
        odata_query = f"$filter=_customerid_value eq {account_id}"
        return self.dv.query("salesorders", odata_query)

    def inspect_order_fields(self) -> List[str]:
        """Return the columns for an order record."""
        records = self.dv.query("salesorders", "$top=1")
        return list(records[0].keys()) if records else []

def create_orders_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the Orders 'plugin' server."""
    orders_mcp = FastMCP(name="OrdersPlugin")
    plugin_logic = OrdersPluginLogic(dv_client)

    orders_mcp.tool(plugin_logic.list_orders)
    orders_mcp.tool(plugin_logic.get_order)
    orders_mcp.tool(plugin_logic.get_orders_by_account)
    orders_mcp.tool(plugin_logic.inspect_order_fields)

    return orders_mcp
