
import hashlib
import os
import uvicorn

from fastmcp import FastMCP
from fastmcp.server.dependencies import CurrentHeaders
from typing import Annotated

mcp = FastMCP("Exam Challenge Server")
EMAIL = "23f2000505@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge(
    headers: Annotated[dict[str, str], CurrentHeaders()]
) -> str:
    """Compute the answer from this call's HTTP challenge header."""
    challenge = headers.get("x-exam-challenge")
    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


class AcceptHeaderMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if (
            scope["type"] == "http"
            and scope["method"] == "POST"
            and scope["path"].rstrip("/") == "/mcp"
        ):
            scope = dict(scope)
            headers = [
                (k, v) for k, v in scope["headers"]
                if k.lower() != b"accept"
            ]
            headers.append((
                b"accept",
                b"application/json, text/event-stream"
            ))
            scope["headers"] = headers

        await self.app(scope, receive, send)


app = AcceptHeaderMiddleware(mcp.http_app(path="/mcp"))

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
