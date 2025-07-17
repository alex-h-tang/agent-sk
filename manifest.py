import inspect
import json
from typing import get_type_hints

from plugins.accounts_plugin import AccountsPlugin
from plugins.opportunities_plugin import OpportunitiesPlugin
from plugins.products_plugin import ProductsPlugin
from plugins.leads_plugin import LeadsPlugin
from plugins.orders_plugin import OrdersPlugin
from plugins.quotes_plugin import QuotesPlugin
from plugins.users_plugin import UsersPlugin

def generate_mcp_manifest(plugin_classes, manifest_path=".mcp.json", server_name="SalesDataverseServer"):
    tools = []

    for plugin_class in plugin_classes:
        class_name = plugin_class.__name__

        for method_name, method_obj in inspect.getmembers(plugin_class, predicate=inspect.isfunction):
            if method_name.startswith("_"):
                continue
            
            sig = inspect.signature(method_obj)
            doc = inspect.getdoc(method_obj) or ""

            parameters = []
            for param_name, param in sig.parameters.items():
                if param_name == "self":
                    continue

                param_type = "string"
                if param.annotation != inspect.Parameter.empty:
                    ann = param.annotation
                    if ann is int:
                        param_type = "integer"
                    elif ann is float:
                        param_type = "number"
                    elif ann is bool:
                        param_type = "boolean"
                    elif ann is list or ann is list[str] or ann is list[dict]:
                        param_type = "array"
                    else:
                        param_type = "string"

                param_schema = {
                    "title": param_name.replace("_", " ").capitalize(),
                    "type": param_type
                }
                if param.default != inspect.Parameter.empty:
                    param_schema["default"] = param.default

                parameters.append((param_name, param_schema))

            input_properties = {}
            required_params = []
            for name, schema in parameters:
                input_properties[name] = schema
                if "default" not in schema:
                    required_params.append(name)

            tool = {
                "name": f"{class_name}_{method_name}",
                "title": f"{class_name} {method_name.replace('_', ' ').capitalize()}",
                "description": doc,
                "inputSchema": {
                    "title": f"{method_name}Input",
                    "type": "object",
                    "properties": input_properties,
                    "required": required_params,
                },
            }
            tools.append(tool)

    manifest = {
        "name": server_name,
        "schema_version": "1.0",
        "tools": tools
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

plugin_classes = [
    AccountsPlugin,
    OpportunitiesPlugin,
    ProductsPlugin,
    LeadsPlugin,
    OrdersPlugin,
    QuotesPlugin,
    UsersPlugin
]

generate_mcp_manifest(plugin_classes)
