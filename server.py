"""MCP server that lets an AI assistant query a sample dataset of job postings.

Run with the Inspector:  mcp dev server.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

from app import tools  # noqa: E402
from app.data import load_postings  # noqa: E402

POSTINGS = load_postings()
mcp = MCPServer("job-postings")


@mcp.tool()
def search_postings_by_skill(skill: str, limit: int = 10) -> list[dict]:
    """Find job postings that ask for a given skill.

    Args:
        skill: One skill name, case-insensitive, for example 'python'.
        limit: Maximum number of postings to return, from 1 to 50.
    """
    try:
        return tools.search_by_skill(POSTINGS, skill, limit)
    except ValueError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def count_postings_by_company(top_n: int = 10) -> dict[str, int]:
    """Count job postings per company, largest first.

    Args:
        top_n: How many companies to return, from 1 to 100.
    """
    try:
        return tools.count_by_company(POSTINGS, top_n)
    except ValueError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def get_posting(posting_id: int) -> dict:
    """Get the full record of one posting by its numeric id.

    Args:
        posting_id: The id of the posting, for example 17.
    """
    try:
        return tools.get_by_id(POSTINGS, posting_id)
    except ValueError as e:
        raise ToolError(str(e)) from e


if __name__ == "__main__":
    mcp.run()