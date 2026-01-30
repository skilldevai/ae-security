# hardened_client.py  –  Lab 3b: Defense in Depth
# Tests the hardened MCP server's security controls.

import asyncio
import httpx
from fastmcp import Client

AUTH_SERVER   = "http://127.0.0.1:9000/token"
MCP_ENDPOINT  = "http://127.0.0.1:8000/mcp/"


async def get_token() -> str:
    """Obtain a JWT from the authorization server."""
    async with httpx.AsyncClient() as h:
        r = await h.post(AUTH_SERVER, data={
            "username": "demo-client",
            "password": "demopass"
        })
        r.raise_for_status()
        return r.json()["access_token"]


async def main():
    token = await get_token()
    print("Token acquired from auth server.\n")

    # ── Scenario 1: Normal tool call ──
    print("=" * 50)
    print("Scenario 1: Normal Tool Call")
    print("=" * 50)
    async with Client(MCP_ENDPOINT, auth=token) as c:
        tools = await c.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        result = await c.call_tool("add", {"a": 3, "b": 4})
        print(f"add(3, 4) = {result}")

    # ── Scenario 2: Customer lookup ──
    print("\n" + "=" * 50)
    print("Scenario 2: Customer Lookup")
    print("=" * 50)
    async with Client(MCP_ENDPOINT, auth=token) as c:
        result = await c.call_tool("lookup_customer", {"name": "alice"})
        print(f"Customer lookup result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
