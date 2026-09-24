#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys


def get_accepted_answers():
    query = """
    query {
      user(login: "somuai") {
        repositoryDiscussionComments(first: 50, onlyAnswers: true) {
          nodes {
            id
            isAnswer
            url
            createdAt
            discussion {
              title
              url
              number
              repository {
                nameWithOwner
              }
            }
          }
        }
      }
    }
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for attempt in range(3):
        try:
            res = subprocess.check_output(cmd, text=True)
            data = json.loads(res)
            nodes = data.get("data", {}).get("user", {}).get("repositoryDiscussionComments", {}).get("nodes", [])
            # Filter out personal repository discussions
            external_answers = [
                a for a in nodes if not a["discussion"]["repository"]["nameWithOwner"].startswith("somuai/")
            ]
            # Sort by createdAt descending
            external_answers.sort(key=lambda a: a.get("createdAt") or "", reverse=True)
            return external_answers
        except Exception as e:
            if attempt < 2:
                import time

                time.sleep(2)
                continue
            print(f"Error fetching accepted answers: {e}", file=sys.stderr)
            return []


def format_row(answer):
    repo = answer["discussion"]["repository"]["nameWithOwner"]
    title = answer["discussion"]["title"].replace("|", "\\|")
    url = answer["url"]
    num = answer["discussion"]["number"]
    date = answer["createdAt"][:10] if answer.get("createdAt") else "N/A"
    status_badge = (
        '<img src="https://img.shields.io/badge/Accepted_Answer-238636?style=flat-square&logo=github&logoColor=white"'
        ' alt="Accepted Answer" />'
    )
    return f"| **{repo}** | {title} | [#{num}]({url}) | `{date}` | {status_badge} |"


def format_accepted_table(answers, top_k=5):
    header = [
        "| Repository | Technical Discussion | Accepted Solution | Solved Date | Status |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    if len(answers) <= top_k:
        lines = list(header)
        for a in answers:
            lines.append(format_row(a))
        return "\n".join(lines)

    top_lines = list(header)
    for a in answers[:top_k]:
        top_lines.append(format_row(a))

    more_lines = list(header)
    for a in answers[top_k:]:
        more_lines.append(format_row(a))

    remaining = len(answers) - top_k
    details_block = (
        f"<details>\n"
        f"<summary><b>Show More Accepted Solutions (Expand {remaining} Additional Answers)</b></summary>\n"
        f"<br />\n\n"
        f"{chr(10).join(more_lines)}\n\n"
        f"</details>"
    )

    return "\n".join(top_lines) + "\n\n" + details_block


def update_readme():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    readme_path = os.path.join(repo_dir, "README.md")

    if not os.path.exists(readme_path):
        print(f"README not found at {readme_path}", file=sys.stderr)
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    answers = get_accepted_answers()
    if not answers:
        print("No external accepted answers retrieved.")
        return False

    new_table = format_accepted_table(answers)
    pattern = r"(<!-- ACCEPTED_ANSWERS_START -->)(.*?)(<!-- ACCEPTED_ANSWERS_END -->)"

    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(
            pattern,
            f"\\1\n\n{new_table}\n\n\\3",
            content,
            flags=re.DOTALL,
        )
    else:
        print("Markers <!-- ACCEPTED_ANSWERS_START --> not found.")
        return False

    if updated_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("README.md updated with latest accepted answers.")
        return True
    else:
        print("README.md already up to date.")
        return False


if __name__ == "__main__":
    update_readme()
