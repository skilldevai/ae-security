# hardened_server.py  –  Lab 3b: Defense in Depth
#
# Layers multiple security controls on top of JWT auth:
#   - Rate limiting (per-client)
#   - Input validation (block dangerous patterns in tool arguments)
#   - Output sanitization (redact sensitive data before returning)
#   - Audit logging (track all security-relevant events)

import json
import re
import time
import warnings
from collections import defaultdict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt, JWTError

from fastmcp import FastMCP
import uvicorn

warnings.filterwarnings("ignore", category=DeprecationWarning)

# ─── JWT settings (must match auth_server.py) ────────────────────
SECRET_KEY = "mcp-lab-secret"
ALGORITHM  = "HS256"
AUDIENCE   = "mcp-lab"


# ═══════════════════════════════════════════════════════════════
# Rate Limiting Configuration
# ═══════════════════════════════════════════════════════════════
RATE_LIMIT_MAX    = 5       # max tool calls per window
RATE_LIMIT_WINDOW = 60      # window in seconds
_request_log = defaultdict(list)


def _check_rate_limit(client_id: str) -> tuple[bool, int]:
    """Returns (allowed, remaining_requests). Always allows in skeleton."""
    return True, RATE_LIMIT_MAX


# ═══════════════════════════════════════════════════════════════
# Input Validation
# ═══════════════════════════════════════════════════════════════
BLOCKED_PATTERNS = [
]


def _validate_tool_args(args: dict) -> tuple[bool, str]:
    """Validate all string arguments in a tool call. Passes all in skeleton."""
    return True, ""


# ═══════════════════════════════════════════════════════════════
# Output Sanitization
# ═══════════════════════════════════════════════════════════════
SENSITIVE_PATTERNS = [
]


def _sanitize_output(text: str) -> str:
    """Remove sensitive data patterns from tool output. No-op in skeleton."""
    return text


# ═══════════════════════════════════════════════════════════════
# Fake Customer Database (for demonstrating output sanitization)
# ═══════════════════════════════════════════════════════════════
_FAKE_CUSTOMERS = {
    "alice": {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "555-0101",
        "ssn": "123-45-6789",
        "card": "4111111111111111",
        "notes": "Premium customer since 2019"
    },
    "bob": {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "555-0102",
        "ssn": "987-65-4321",
        "card": "5500000000000004",
        "notes": "Temp credentials – password: bob_secret_123"
    }
}


# ═══════════════════════════════════════════════════════════════
# MCP Server + Middleware
# ═══════════════════════════════════════════════════════════════
mcp = FastMCP("Hardened Server")
app = mcp.http_app(path="/mcp", transport="streamable-http")


class HardenedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/mcp"):
            return await call_next(request)

        # ── Step 1: JWT Authentication ──
        auth = request.headers.get("authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse(status_code=401,
                                content={"detail": "Missing token"})

        token_str = auth.removeprefix("Bearer ").strip()
        try:
            claims = jwt.decode(token_str, SECRET_KEY,
                                algorithms=[ALGORITHM], audience=AUDIENCE)
        except JWTError as exc:
            return JSONResponse(status_code=401,
                                content={"detail": f"Token invalid: {exc}"})

        client_id = claims.get("sub", "unknown")

        # ── Step 2: Rate Limiting ──
        # (rate limiting logic goes here)

        # ── Step 3: Input Validation (for tool calls) ──
        # (input validation logic goes here)

        return await call_next(request)


app.add_middleware(HardenedMiddleware)


# ═══════════════════════════════════════════════════════════════
# Tools
# ═══════════════════════════════════════════════════════════════
@mcp.tool(description="Add two numbers")
async def add(a: int, b: int) -> int:
    return a + b


@mcp.tool(description="Look up customer information by name")
async def lookup_customer(name: str) -> str:
    """Returns customer info. Sensitive data should be sanitized."""
    customer = _FAKE_CUSTOMERS.get(name.lower())
    if not customer:
        return f"No customer found: {name}"
    raw = (
        f"Name: {customer['name']}\n"
        f"Email: {customer['email']}\n"
        f"Phone: {customer['phone']}\n"
        f"SSN: {customer['ssn']}\n"
        f"Card: {customer['card']}\n"
        f"Notes: {customer['notes']}"
    )
    return raw


@mcp.tool(description="Search customer notes")
async def search_notes(query: str) -> str:
    """Search through customer notes for matching text."""
    results = []
    for cid, cust in _FAKE_CUSTOMERS.items():
        if query.lower() in cust["notes"].lower():
            results.append(f"{cust['name']}: {cust['notes']}")
    if not results:
        return f"No notes matching: {query}"
    return "\n".join(results)


if __name__ == "__main__":
    print("Hardened MCP Server starting...")
    print(f"  Rate limit: {RATE_LIMIT_MAX} tool calls per {RATE_LIMIT_WINDOW}s")
    print(f"  Input validation patterns: {len(BLOCKED_PATTERNS)}")
    print(f"  Output sanitization patterns: {len(SENSITIVE_PATTERNS)}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
