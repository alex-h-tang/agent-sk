from typing import List, Dict, Any
from fastmcp import FastMCP

class ContactsPluginLogic:
    """Contains the business logic for contact-related operations."""
    def __init__(self, dv_client: Any):
        self.dv = dv_client

    def list_contacts(self, top: int = 5) -> List[Dict[str, Any]]:
        """List the top N contacts from Dataverse."""
        odata_query = f"$top={top}"
        return self.dv.query("contacts", odata_query)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Retrieve a single contact by its contact id."""
        return self.dv.retrieve("contacts", contact_id)

    def inspect_contact_fields(self) -> List[str]:
        """Return the columns for an contact record."""
        records = self.dv.query("contacts", "$top=1")
        return list(records[0].keys()) if records else []

def create_contacts_plugin_server(dv_client: Any) -> FastMCP:
    """Factory function to create and configure the contacts 'plugin' server."""
    contacts_mcp = FastMCP(name="contactsPlugin")
    plugin_logic = ContactsPluginLogic(dv_client)

    contacts_mcp.tool(plugin_logic.list_contacts)
    contacts_mcp.tool(plugin_logic.get_contact)
    contacts_mcp.tool(plugin_logic.inspect_contact_fields)

    return contacts_mcp
