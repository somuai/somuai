import json
import os
import subprocess
import tempfile
from unittest.mock import patch

from sync_accepted_answers import (
    format_accepted_table,
    format_row,
    get_accepted_answers,
    update_readme,
)


def test_format_row_standard():
    answer = {
        "discussion": {
            "title": "Storage: upload rejected with RLS violation that no policy can satisfy",
            "url": "https://github.com/supabase/supabase/discussions/50714",
            "number": 50714,
            "repository": {"nameWithOwner": "supabase/supabase"},
        },
        "url": "https://github.com/supabase/supabase/discussions/50714#discussioncomment-18551115",
        "createdAt": "2026-09-22T09:45:17Z",
    }
    row = format_row(answer)
    assert "**supabase/supabase**" in row
    assert "Storage: upload rejected with RLS violation that no policy can satisfy" in row
    assert "[#50714](https://github.com/supabase/supabase/discussions/50714#discussioncomment-18551115)" in row
    assert "`2026-09-22`" in row
    assert "Accepted_Answer-238636" in row


def test_format_row_escapes_pipe():
    answer = {
        "discussion": {
            "title": "Discussion with | pipe character | inside title",
            "url": "https://github.com/supabase/supabase/discussions/100",
            "number": 100,
            "repository": {"nameWithOwner": "supabase/supabase"},
        },
        "url": "https://github.com/supabase/supabase/discussions/100#discussioncomment-1",
        "createdAt": "2026-09-22T00:00:00Z",
    }
    row = format_row(answer)
    assert r"Discussion with \| pipe character \| inside title" in row


def test_format_row_missing_created_at():
    answer = {
        "discussion": {
            "title": "Some question",
            "url": "https://github.com/supabase/supabase/discussions/200",
            "number": 200,
            "repository": {"nameWithOwner": "supabase/supabase"},
        },
        "url": "https://github.com/supabase/supabase/discussions/200#discussioncomment-2",
        "createdAt": None,
    }
    row = format_row(answer)
    assert "`N/A`" in row


def test_format_accepted_table_under_top_k():
    answers = [
        {
            "discussion": {
                "title": f"Question {i}",
                "url": f"https://github.com/org/repo/discussions/{i}",
                "number": i,
                "repository": {"nameWithOwner": "org/repo"},
            },
            "url": f"https://github.com/org/repo/discussions/{i}#comment-{i}",
            "createdAt": "2026-09-20T00:00:00Z",
        }
        for i in range(1, 4)
    ]
    table = format_accepted_table(answers, top_k=5)
    assert "| Repository | Technical Discussion | Accepted Solution | Solved Date | Status |" in table
    assert "<details>" not in table
    assert "**org/repo**" in table
    assert "Question 1" in table
    assert "Question 2" in table
    assert "Question 3" in table


def test_format_accepted_table_exceeds_top_k():
    answers = [
        {
            "discussion": {
                "title": f"Question {i}",
                "url": f"https://github.com/org/repo/discussions/{i}",
                "number": i,
                "repository": {"nameWithOwner": "org/repo"},
            },
            "url": f"https://github.com/org/repo/discussions/{i}#comment-{i}",
            "createdAt": "2026-09-20T00:00:00Z",
        }
        for i in range(1, 8)
    ]
    table = format_accepted_table(answers, top_k=5)
    assert "<details>" in table
    assert "<summary><b>Show More Accepted Solutions (Expand 2 Additional Answers)</b></summary>" in table
    assert "</details>" in table
    assert "Question 5" in table
    assert "Question 6" in table
    assert "Question 7" in table


@patch("subprocess.check_output")
def test_get_accepted_answers_filters_personal_repos(mock_check_output):
    raw_response = {
        "data": {
            "user": {
                "repositoryDiscussionComments": {
                    "nodes": [
                        {
                            "id": "1",
                            "isAnswer": True,
                            "url": "https://github.com/supabase/supabase/discussions/50714#c1",
                            "createdAt": "2026-09-22T09:00:00Z",
                            "discussion": {
                                "title": "Storage RLS issue",
                                "url": "https://github.com/supabase/supabase/discussions/50714",
                                "number": 50714,
                                "repository": {"nameWithOwner": "supabase/supabase"},
                            },
                        },
                        {
                            "id": "2",
                            "isAnswer": True,
                            "url": "https://github.com/somuai/codexmap/discussions/2#c2",
                            "createdAt": "2026-09-01T09:00:00Z",
                            "discussion": {
                                "title": "AST parser setup",
                                "url": "https://github.com/somuai/codexmap/discussions/2",
                                "number": 2,
                                "repository": {"nameWithOwner": "somuai/codexmap"},
                            },
                        },
                        {
                            "id": "3",
                            "isAnswer": True,
                            "url": "https://github.com/community/community/discussions/208386#c3",
                            "createdAt": "2026-09-20T09:00:00Z",
                            "discussion": {
                                "title": "macOS fetch error",
                                "url": "https://github.com/community/community/discussions/208386",
                                "number": 208386,
                                "repository": {"nameWithOwner": "community/community"},
                            },
                        },
                    ]
                }
            }
        }
    }
    mock_check_output.return_value = json.dumps(raw_response)

    answers = get_accepted_answers()
    assert len(answers) == 2
    repo_names = [a["discussion"]["repository"]["nameWithOwner"] for a in answers]
    assert "supabase/supabase" in repo_names
    assert "community/community" in repo_names
    assert "somuai/codexmap" not in repo_names
    # Verify sorting by date descending
    assert answers[0]["discussion"]["repository"]["nameWithOwner"] == "supabase/supabase"
    assert answers[1]["discussion"]["repository"]["nameWithOwner"] == "community/community"


@patch("subprocess.check_output")
def test_get_accepted_answers_exception_handling(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, ["gh"])
    result = get_accepted_answers()
    assert result == []


def test_update_readme_success():
    sample_readme = "# Title\n\n<!-- ACCEPTED_ANSWERS_START -->\nOld Content\n<!-- ACCEPTED_ANSWERS_END -->\n"
    sample_answers = [
        {
            "discussion": {
                "title": "Storage RLS issue",
                "url": "https://github.com/supabase/supabase/discussions/50714",
                "number": 50714,
                "repository": {"nameWithOwner": "supabase/supabase"},
            },
            "url": "https://github.com/supabase/supabase/discussions/50714#c1",
            "createdAt": "2026-09-22T09:00:00Z",
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_accepted_answers.get_accepted_answers", return_value=sample_answers),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_accepted_answers.py")
            res = update_readme()
            assert res is True

        with open(readme_path, "r", encoding="utf-8") as f:
            updated = f.read()

        assert "supabase/supabase" in updated
        assert "#50714" in updated
        assert "Old Content" not in updated


def test_update_readme_no_markers():
    sample_readme = "# Title\n\nNo markers here\n"
    sample_answers = [
        {
            "discussion": {
                "title": "Some question",
                "url": "https://github.com/supabase/supabase/discussions/1",
                "number": 1,
                "repository": {"nameWithOwner": "supabase/supabase"},
            },
            "url": "https://github.com/supabase/supabase/discussions/1#c1",
            "createdAt": "2026-09-22T00:00:00Z",
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_accepted_answers.get_accepted_answers", return_value=sample_answers),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_accepted_answers.py")
            res = update_readme()
            assert res is False


def test_update_readme_file_missing():
    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("os.path.abspath") as mock_abspath,
    ):
        mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_accepted_answers.py")
        res = update_readme()
        assert res is False


def test_update_readme_no_answers():
    sample_readme = "<!-- ACCEPTED_ANSWERS_START -->\n<!-- ACCEPTED_ANSWERS_END -->\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_accepted_answers.get_accepted_answers", return_value=[]),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_accepted_answers.py")
            res = update_readme()
            assert res is False
