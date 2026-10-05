"""The logic of each tool, as plain Python functions.

There is no MCP code in this file. Keeping the logic separate from the server
makes it easy to read and easy to test.
"""
from collections import Counter

MAX_LIMIT = 50
MAX_TOP_N = 100


def summarize(posting: dict) -> dict:
    """A short version of a posting, so the AI is not given more than it needs."""
    return {
        "id": posting["id"],
        "title": posting["title"],
        "company": posting["company"],
        "location": posting["location"],
        "skills": posting["skills"],
    }


def search_by_skill(postings: list[dict], skill: str, limit: int = 10) -> list[dict]:
    """Return up to `limit` postings that list the given skill."""
    skill = skill.strip().lower()
    if not skill:
        raise ValueError("skill must not be empty. Example: 'python'.")
    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}.")
    hits = [p for p in postings if skill in [s.lower() for s in p["skills"]]]
    return [summarize(p) for p in hits[:limit]]


def count_by_company(postings: list[dict], top_n: int = 10) -> dict[str, int]:
    """Return the `top_n` companies with the most postings."""
    if not 1 <= top_n <= MAX_TOP_N:
        raise ValueError(f"top_n must be between 1 and {MAX_TOP_N}.")
    counts = Counter(p["company"] for p in postings)
    return dict(counts.most_common(top_n))


def get_by_id(postings: list[dict], posting_id: int) -> dict:
    """Return one full posting, or raise an error that says what ids exist."""
    for p in postings:
        if p["id"] == posting_id:
            return p
    raise ValueError(
        f"No posting with id {posting_id}. Valid ids are 1 to {len(postings)}."
    )
