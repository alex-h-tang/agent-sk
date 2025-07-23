from semantic_kernel.functions import kernel_function

class UsersPlugin:
    def __init__(self, dv_client):
        self.dv = dv_client
    
    @kernel_function
    async def list_users(self, top: int = 5) -> list[dict]:
        """
        List the top N users from Dataverse.
        """
        odata_query = f"$top={top}"
        return self.dv.query("systemusers", odata_query)
    
    @kernel_function
    async def get_user(self, user_id: str) -> dict:
        """
        Retrieve a single user by their GUID.
        """
        return self.dv.retrieve("systemusers", user_id)
    
    @kernel_function
    async def get_users_by_name(self, name: str) -> list[dict]:
        """
        Retrieve users by at least a substring of their name.
        """
        odata_query = f"$filter=contains(fullname, '{name}')"
        return self.dv.query("systemusers", odata_query)
    
    @kernel_function
    async def get_direct_reports(self, manager: str) -> list[dict]:
        """
        Retrieve users who report directly to a specified manager, based on manager GUID, which can be obtained as _parentsystemuserid_value from a user's json.
        """
        odata_query = f"$filter=_parentsystemuserid_value eq '{manager}'"
        return self.dv.query("systemusers", odata_query)
    
    @kernel_function
    async def get_business_unit_by_id(self, business_unit_id: str) -> dict:
        """
        Retrieve a business unit by its ID.
        """
        return self.dv.retrieve("businessunits", business_unit_id)
    
    @kernel_function
    async def inspect_user_fields(self) -> list[str]:
        """
        Return the columns for an user record
        """
        record = self.dv.query("systemusers", "$top=1")[0]
        return list(record.keys())
