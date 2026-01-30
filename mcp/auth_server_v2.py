# auth_server.py  –  Lab 3b: Defense in Depth
#
# This is the same auth server pattern from Lab 3, configured for the
# hardened server's tools.  It is provided complete – the focus of this
# lab is the hardened_server.py and hardened_client.py files.

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import uvicorn

SECRET_KEY = "mcp-lab-secret"
ALGORITHM  = "HS256"
AUDIENCE   = "mcp-lab"
EXPIRES_IN = 3600

_fake_clients = {
    "demo-client": {
        "client_secret": "demopass",
        "scopes": [
            "tools:add",
            "tools:lookup_customer",
            "tools:search_notes",
            "tools:get_audit_log"
        ]
    }
}

app = FastAPI(title="MCP Lab – Auth Server (Lab 3b)")


def _create_access_token(sub: str, scopes: list[str]) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "scope": " ".join(scopes),
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + timedelta(seconds=EXPIRES_IN),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token")
def token(form: OAuth2PasswordRequestForm = Depends()):
    client = _fake_clients.get(form.username)
    if not client or client["client_secret"] != form.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid client credentials")
    access_token = _create_access_token(form.username, client["scopes"])
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": EXPIRES_IN
    }


@app.post("/introspect")
def introspect(token: str = Body(..., embed=True)):
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[ALGORITHM], audience=AUDIENCE)
    except JWTError:
        return {"active": False}
    return {
        "active": True,
        "sub": payload["sub"],
        "scope": payload.get("scope", ""),
        "exp": payload["exp"]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
