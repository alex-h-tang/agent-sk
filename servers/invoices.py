from typing import List, Dict, Any
from fastmcp import FastMCP

class InvoicesPluginLogic:
    """Contains the business logic for invoice-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_invoices(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N invoices from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("invoices", odata_query)

    def get_invoice(self, invoice_number: str) -> Dict[str, Any]:
        """Retrieve a single invoice by its invoice number."""
        return self.dv.retrieve("invoices", invoice_number)

    def inspect_invoice_fields(self) -> List[str]:
        """Return the columns for an invoice record."""
        records = self.dv.query("invoices", "$top=1")
        return list(records[0].keys()) if records else []

def create_invoices_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the invoices 'plugin' server."""
    invoices_mcp = FastMCP(name="invoicesPlugin")
    plugin_logic = InvoicesPluginLogic(dv_client)

    invoices_mcp.tool(plugin_logic.list_invoices)
    invoices_mcp.tool(plugin_logic.get_invoice)
    invoices_mcp.tool(plugin_logic.inspect_invoice_fields)

    return invoices_mcp
