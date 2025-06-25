import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from mcp.server.stdio import stdio_server
from main import build_kernel

async def serve():
    kernel = await build_kernel()
    server = kernel.as_mcp_server(server_name="cs_assistant_sk")

    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(serve())
