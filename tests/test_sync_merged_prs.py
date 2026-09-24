import json
import os
import subprocess
import tempfile
from unittest.mock import patch

from sync_merged_prs import (
    format_merged_table,
    format_row,
    get_merged_prs,
    update_readme,
)


def test_format_row_standard():
    pr = {
        "repository": {"nameWithOwner": "open-telemetry/opentelemetry-python-contrib"},
        "title": "fix: prevent duplicate exception events on server spans",
        "url": "https://github.com/open-telemetry/opentelemetry-python-contrib/pull/5078",
        "closedAt": "2026-09-18T18:00:00Z",
        "number": 5078,
    }
    row = format_row(pr)
    assert "**open-telemetry/opentelemetry-python-contrib**" in row
    assert "fix: prevent duplicate exception events on server spans" in row
    assert "[#5078](https://github.com/open-telemetry/opentelemetry-python-contrib/pull/5078)" in row
    assert "`2026-09-18`" in row
    assert "Merged-8957e5" in row


def test_format_row_escapes_pipe():
    pr = {
        "repository": {"nameWithOwner": "google/adk-go"},
        "title": "fix: resolve nil pointer | handle context cancellation",
        "url": "https://github.com/google/adk-go/pull/1465",
        "closedAt": "2026-09-01T12:00:00Z",
        "number": 1465,
    }
    row = format_row(pr)
    assert r"resolve nil pointer \| handle context cancellation" in row


def test_format_row_missing_closed_at():
    pr = {
        "repository": {"nameWithOwner": "vllm-project/vllm"},
        "title": "feat: optimize attention kernel",
        "url": "https://github.com/vllm-project/vllm/pull/1234",
        "closedAt": None,
        "number": 1234,
    }
    row = format_row(pr)
    assert "`N/A`" in row


def test_format_merged_table_under_top_k():
    prs = [
        {
            "repository": {"nameWithOwner": f"repo/item-{i}"},
            "title": f"Contribution {i}",
            "url": f"https://github.com/repo/item-{i}/pull/{i}",
            "closedAt": "2026-09-01T00:00:00Z",
            "number": i,
        }
        for i in range(1, 4)
    ]
    table = format_merged_table(prs, top_k=5)
    assert "| Repository | Contribution Highlight | Pull Request | Merged Date | Status |" in table
    assert "<details>" not in table
    assert "**repo/item-1**" in table
    assert "**repo/item-2**" in table
    assert "**repo/item-3**" in table


def test_format_merged_table_exceeds_top_k():
    prs = [
        {
            "repository": {"nameWithOwner": f"repo/item-{i}"},
            "title": f"Contribution {i}",
            "url": f"https://github.com/repo/item-{i}/pull/{i}",
            "closedAt": "2026-09-01T00:00:00Z",
            "number": i,
        }
        for i in range(1, 8)
    ]
    table = format_merged_table(prs, top_k=5)
    assert "<details>" in table
    assert "<summary><b>Show More Merged Contributions (Expand 2 Additional Merged PRs)</b></summary>" in table
    assert "</details>" in table
    assert "**repo/item-5**" in table
    assert "**repo/item-6**" in table
    assert "**repo/item-7**" in table


@patch("subprocess.check_output")
def test_get_merged_prs_filters_personal_repos(mock_check_output):
    raw_prs = [
        {
            "repository": {"nameWithOwner": "open-telemetry/opentelemetry-python"},
            "title": "Add GenAI token attributes",
            "url": "https://github.com/open-telemetry/opentelemetry-python/pull/5673",
            "closedAt": "2026-09-18T10:00:00Z",
            "number": 5673,
        },
        {
            "repository": {"nameWithOwner": "somuai/somuai"},
            "title": "Update README",
            "url": "https://github.com/somuai/somuai/pull/1",
            "closedAt": "2026-09-15T10:00:00Z",
            "number": 1,
        },
        {
            "repository": {"nameWithOwner": "somuai/codexmap"},
            "title": "Initial setup",
            "url": "https://github.com/somuai/codexmap/pull/1",
            "closedAt": "2026-09-10T10:00:00Z",
            "number": 1,
        },
        {
            "repository": {"nameWithOwner": "google/adk-go"},
            "title": "Support structured streaming",
            "url": "https://github.com/google/adk-go/pull/1493",
            "closedAt": "2026-09-05T10:00:00Z",
            "number": 1493,
        },
    ]
    mock_check_output.return_value = json.dumps(raw_prs)

    filtered = get_merged_prs()
    assert len(filtered) == 2
    repo_names = [p["repository"]["nameWithOwner"] for p in filtered]
    assert "open-telemetry/opentelemetry-python" in repo_names
    assert "google/adk-go" in repo_names
    assert "somuai/somuai" not in repo_names
    assert "somuai/codexmap" not in repo_names


@patch("subprocess.check_output")
def test_get_merged_prs_exception_handling(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, ["gh"])
    result = get_merged_prs()
    assert result == []


def test_update_readme_success():
    sample_readme = "# Title\n\n<!-- MERGED_PRS_START -->\nOld Table Content\n<!-- MERGED_PRS_END -->\n\n## Footer\n"
    sample_prs = [
        {
            "repository": {"nameWithOwner": "huggingface/transformers"},
            "title": "Fix rotary embedding dtype cast",
            "url": "https://github.com/huggingface/transformers/pull/48598",
            "closedAt": "2026-09-17T00:00:00Z",
            "number": 48598,
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_merged_prs.get_merged_prs", return_value=sample_prs),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_merged_prs.py")
            res = update_readme()
            assert res is True

        with open(readme_path, "r", encoding="utf-8") as f:
            updated = f.read()

        assert "huggingface/transformers" in updated
        assert "#48598" in updated
        assert "Old Table Content" not in updated


def test_update_readme_no_markers():
    sample_readme = "# Title\n\nNo markers present\n"
    sample_prs = [
        {
            "repository": {"nameWithOwner": "huggingface/transformers"},
            "title": "Fix rotary embedding dtype cast",
            "url": "https://github.com/huggingface/transformers/pull/48598",
            "closedAt": "2026-09-17T00:00:00Z",
            "number": 48598,
        }
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_merged_prs.get_merged_prs", return_value=sample_prs),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_merged_prs.py")
            res = update_readme()
            assert res is False


def test_update_readme_file_missing():
    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("os.path.abspath") as mock_abspath,
    ):
        mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_merged_prs.py")
        res = update_readme()
        assert res is False


def test_update_readme_no_prs():
    sample_readme = "<!-- MERGED_PRS_START -->\n<!-- MERGED_PRS_END -->\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(sample_readme)

        with (
            patch("sync_merged_prs.get_merged_prs", return_value=[]),
            patch("os.path.abspath") as mock_abspath,
        ):
            mock_abspath.return_value = os.path.join(tmpdir, "scripts", "sync_merged_prs.py")
            res = update_readme()
            assert res is False
