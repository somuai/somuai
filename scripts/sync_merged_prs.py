#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys


def get_merged_prs():
    try:
        cmd = [
            "gh",
            "search",
            "prs",
            "--author",
            "somuai",
            "--merged",
            "--limit",
            "50",
            "--json",
            "repository,title,url,closedAt,number",
        ]
        res = subprocess.check_output(cmd, text=True)
        prs = json.loads(res)
    except Exception as e:
        print(f"Error fetching merged PRs: {e}", file=sys.stderr)
        return []

    # Filter out personal repository PRs
    external_prs = [
        p for p in prs if not p["repository"]["nameWithOwner"].startswith("somuai/")
    ]
    return external_prs


def format_merged_table(prs):
    lines = [
        "| Repository | Contribution Highlight | Pull Request | Merged Date | Status |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for p in prs:
        repo = p["repository"]["nameWithOwner"]
        title = p["title"].replace("|", "\\|")
        url = p["url"]
        num = p["number"]
        date = p["closedAt"][:10] if p.get("closedAt") else "N/A"
        status_badge = '<img src="https://img.shields.io/badge/Merged-8957e5?style=flat-square&logo=git&logoColor=white" alt="Merged" />'
        lines.append(f"| **{repo}** | {title} | [#{num}]({url}) | `{date}` | {status_badge} |")
    return "\n".join(lines)


def update_readme():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    readme_path = os.path.join(repo_dir, "README.md")

    if not os.path.exists(readme_path):
        print(f"README not found at {readme_path}", file=sys.stderr)
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    prs = get_merged_prs()
    if not prs:
        print("No external merged PRs retrieved.")
        return False

    new_table = format_merged_table(prs)
    pattern = r"(<!-- MERGED_PRS_START -->)(.*?)(<!-- MERGED_PRS_END -->)"

    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(
            pattern,
            f"\\1\n\n{new_table}\n\n\\3",
            content,
            flags=re.DOTALL,
        )
    else:
        print("Markers <!-- MERGED_PRS_START --> not found.")
        return False

    if updated_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("README.md updated with latest merged pull requests.")
        return True
    else:
        print("README.md already up to date.")
        return False


if __name__ == "__main__":
    update_readme()
