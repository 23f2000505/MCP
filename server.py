
import os
import hashlib

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

mcp = FastMCP("Exam Challenge Server")

EMAIL = "23f2000505@ds.study.iitm.ac.in".strip().lower()


@mcp.tool()
def solve_challenge() -> str:
    """Return the hash derived from the current HTTP challenge header."""
    headers = get_http_headers()
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        path="/",
    )
