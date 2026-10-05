"""Tests for the tool logic. Run from the project folder with:  pytest"""
import pytest

from app import tools

POSTINGS = [
    {"id": 1, "title": "Backend Engineer", "company": "A", "location": "Nairobi",
     "date": "2026-09-01", "skills": ["Python", "sql"]},
    {"id": 2, "title": "Data Analyst", "company": "A", "location": "Remote",
     "date": "2026-09-02", "skills": ["sql"]},
    {"id": 3, "title": "ML Engineer", "company": "B", "location": "Lagos",
     "date": "2026-09-03", "skills": ["python"]},
]


def test_search_ignores_case_and_spaces():
    result = tools.search_by_skill(POSTINGS, "  PYTHON ")
    assert [p["id"] for p in result] == [1, 3]


def test_search_respects_limit():
    assert len(tools.search_by_skill(POSTINGS, "sql", limit=1)) == 1


def test_search_returns_summary_without_date():
    assert "date" not in tools.search_by_skill(POSTINGS, "sql")[0]


def test_search_empty_skill_is_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        tools.search_by_skill(POSTINGS, "   ")


@pytest.mark.parametrize("bad_limit", [0, -1, 51])
def test_search_bad_limit_is_rejected(bad_limit):
    with pytest.raises(ValueError, match="limit"):
        tools.search_by_skill(POSTINGS, "sql", limit=bad_limit)


def test_count_by_company_is_largest_first():
    assert tools.count_by_company(POSTINGS) == {"A": 2, "B": 1}


def test_count_bad_top_n_is_rejected():
    with pytest.raises(ValueError, match="top_n"):
        tools.count_by_company(POSTINGS, top_n=0)


def test_get_posting_found():
    assert tools.get_by_id(POSTINGS, 2)["title"] == "Data Analyst"


def test_get_posting_unknown_id_names_valid_range():
    with pytest.raises(ValueError, match="1 to 3"):
        tools.get_by_id(POSTINGS, 99)
