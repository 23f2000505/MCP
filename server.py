
import os
import hashlib
from typing import Annotated

import uvicorn
from fastmcp import FastMCP
from fastmcp.server.dependencies import CurrentHeaders

mcp = FastMCP("Exam Challenge Server")
EMAIL = "23f2000505@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge(
    headers: Annotated[dict[str, str], CurrentHeaders()]
) -> str:
    """Hash the challenge supplied in the current HTTP request."""
    challenge = headers.get("x-exam-challenge")
    if not challenge:
        raise ValueError("Missing X-Exam-Challenge")

    value = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


class AcceptMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["method"] == "POST":
            scope = dict(scope)
            headers = [
                (key, value)
                for key, value in scope["headers"]
                if key.lower() != b"accept"
            ]
            headers.append((
                b"accept",
                b"application/json, text/event-stream",
            ))
            scope["headers"] = headers

        await self.app(scope, receive, send)


app = AcceptMiddleware(mcp.http_app(path="/"))

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
