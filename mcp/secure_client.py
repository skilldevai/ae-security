# secure_client.py  –  Lab 4: Auth + Per-Tool Scopes
# Demonstrates per-tool scope enforcement with different client identities.

import asyncio
import httpx
from fastmcp import Client

AUTH_SERVER  = "http://127.0.0.1:9000/token"
MCP_ENDPOINT = "http://127.0.0.1:8000/mcp/"


async def get_token(client_id: str, client_secret: str) -> str:
    """Obtain a JWT from the authorization server."""
    async with httpx.AsyncClient() as h:
        r = await h.post(AUTH_SERVER, data={
            "username": client_id,
            "password": client_secret
        })
        r.raise_for_status()
        return r.json()["access_token"]


async def test_client(name: str, token: str):
    """Test MCP tool access with the given token."""
    print(f"\n{'='*50}")
    print(f"Testing as: {name}")
    print(f"{'='*50}")

    async with Client(MCP_ENDPOINT, auth=token) as c:
        tools = await c.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        result = await c.call_tool("add", {"a": 7, "b": 5})
        print(f"add(7, 5) = {result}")


async def main():
    # Test with full-client
    full_token = await get_token("full-client", "fullpass")
    await test_client("full-client", full_token)


if __name__ == "__main__":
    asyncio.run(main())
