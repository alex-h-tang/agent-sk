from urllib.parse import urlparse
from azure.identity import AzureDeveloperCliCredential, ManagedIdentityCredential, ChainedTokenCredential, DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient

# managed identity

import requests


def create_dataverse_client(api_url: str):
    parsed = urlparse(api_url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    cred = ChainedTokenCredential(DefaultAzureCredential(
    ), AzureDeveloperCliCredential(), ManagedIdentityCredential())

    token = cred.get_token(f"{root}/.default").token

    headers = {"Authorization": f"Bearer {token}", "OData-MaxVersion": "4.0", "OData-Version": "4.0",
               "Accept": "application/json", "Content-Type": "application/json; charset=utf-8"}

    class DataverseClient:
        def __init__(self, base_url: str, headers: dict[str, str]):
            self.base_url = base_url.rstrip("/")
            self.root_url = self.base_url.rsplit('/api', 1)[0]
            self.headers = headers

        def query(self, table: str, odata_query: str = ""):
            resp = requests.get(
                f"{self.base_url}/{table}?{odata_query}", headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("value", [])

        def retrieve(self, table: str, record_id: str):
            resp = requests.get(
                f"{self.base_url}/{table}({record_id})", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

        def query_with_params(self, table: str, params: dict) -> list[dict]:
            url = f"{self.base_url}/{table}"
            resp = requests.get(url, headers=self.headers,
                                params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()

        def post(self, endpoint: str, payload: dict) -> dict:
            url = f"{self.root_url}/{endpoint.lstrip('/')}"
            resp = requests.post(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    return DataverseClient(api_url, headers)
