
import os
import hashlib
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.server.dependencies import CurrentHeaders

mcp = FastMCP("Exam Challenge Server")

EMAIL = "23f2000505@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge(
    headers: Annotated[dict, CurrentHeaders()]
) -> str:
    """Solve the exam challenge from the HTTP request header."""
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    text = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        path="/",
    )
