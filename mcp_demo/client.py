# import requests

# url = "http://127.0.0.1:8000/mcp"

# headers = {
#     'Accept': "application/json, text/event-stream"
# }

# body = {
#     "jsonrpc": "2.0",
#     "id": 1,
#     "params":{},
#     "method": "tools/list"
# }

# response = requests.post(url=url, headers=headers, json=body)
# print(response.text)

# for line in response.iter_lines():
#     if line:
#         print(line)

from mcp import ClientSession, types
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client
import asyncio
import json
from pydantic import AnyUrl

class MCPClient:
    def __init__(self, url):
        self.url = url
        self.stack = AsyncExitStack()
        self._sess = None

    async def __aenter__(self):
        read, write, _ = await self.stack.enter_async_context(streamablehttp_client(self.url))

        self._sess = await self.stack.enter_async_context(ClientSession(read, write))
        await self._sess.initialize()
        return self

    async def list_tools(self):
        tools = await self._sess.list_tools()
        return tools

    async def list_resources(self, uri):
        resources = await self._sess.list_resources()
        # print("RESOURCES: ", resources.__dict__)
        if isinstance(resources, types.TextResourceContents):
            res = json.load(resources)
            return res
        return resources
    
    async def read_resource(self, uri, doc_id) -> types.ReadResourceResult:
        doc_uri = uri + doc_id
        resource = await self._sess.read_resource(AnyUrl(doc_uri))
        return resource

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stack.aclose()

async def main():
    async with MCPClient(url="http://localhost:8000/mcp/") as client:
        tools = await client.list_tools()
        print("Tools : ", tools)
        resources = await client.list_resources(" ")
        print("\n Resources: ", resources)
        resource = await client.read_resource("docs://documents/", 'report.pdf')
        print("\n Resource Content: ", resource)

asyncio.run(main())