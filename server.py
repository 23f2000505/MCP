
import os
from typing import Annotated
import hashlib

from fastmcp import FastMCP
from fastmcp.server.dependencies import CurrentHeaders

mcp = FastMCP("Exam Challenge Server")
EMAIL = "23f2000505@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge(
    headers: Annotated[dict[str, str], CurrentHeaders()]
) -> str:
    """Return the SHA-256 challenge response."""
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge")

    payload = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        path="/",
    )
