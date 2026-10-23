#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time

PROXY_URL = "http://127.0.0.1:8989"
os.environ["HTTPS_PROXY"] = PROXY_URL
os.environ["HTTP_PROXY"] = PROXY_URL

SOMUAI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SOMUAI_DIR, "scripts")
README_PATH = os.path.join(SOMUAI_DIR, "README.md")
SUBMIT_SCRIPT = "/Users/soumyajitghosh/.gemini/antigravity/brain/90b42fc2-87e1-4474-8e11-836bc37ee834/scratch/submit_connector_pr.sh"

TRACKED_PRS = [
    {"repo": "topoteretes/cognee-community", "number": 348, "name": "Apache Iceberg Connector"},
    {"repo": "topoteretes/cognee-community", "number": 351, "name": "OpenLineage Connector"},
    {"repo": "topoteretes/cognee-community", "number": 378, "name": "Honeycomb Connector"},
    {"repo": "kestra-io/blueprints", "number": 1299, "name": "DeepEval GenAI Quality Gate"},
    {"repo": "open-telemetry/opentelemetry-python-genai", "number": 836, "name": "OTel GenAI Event Decoupling"},
    {"repo": "open-telemetry/opentelemetry-python-genai", "number": 913, "name": "OTel GenAI Qwen-Agent Tuple Inputs"},
    {
        "repo": "open-telemetry/opentelemetry-python",
        "number": 5626,
        "name": "OTel SDK MultiSpanProcessor Exception Guard",
    },
    {"repo": "modelcontextprotocol/servers", "number": 4742, "name": "MCP Server Non-Root Docker Execution"},
    {"repo": "BerriAI/litellm", "number": 38277, "name": "LiteLLM Vertex Rerank"},
    {"repo": "anthropics/claude-agent-sdk-python", "number": 1428, "name": "Claude Agent SDK Compaction UUID Remapping"},
    {"repo": "langchain-ai/deepagents", "number": 7143, "name": "LangChain DeepAgents Reftable Branch Fallback"},
    {"repo": "vllm-project/vllm", "number": 57504, "name": "vLLM InternLM2 Split Opening Marker"},
    {"repo": "vllm-project/vllm", "number": 55371, "name": "vLLM Responses API Boundary Split"},
    {"repo": "vllm-project/vllm", "number": 55362, "name": "vLLM MTP Num Speculative Tokens Default"},
]

TRACKED_COGNEE_ISSUES = [
    {"issue": 5424, "target": "prometheus", "name": "Prometheus Connector"},
    {"issue": 4773, "target": "redshift", "name": "Amazon Redshift Connector"},
]


def run_cmd(cmd, cwd=None, retries=3):
    env = dict(os.environ)
    env["HTTPS_PROXY"] = PROXY_URL
    env["HTTP_PROXY"] = PROXY_URL
    for attempt in range(1, retries + 1):
        try:
            res = subprocess.check_output(cmd, cwd=cwd, env=env, stderr=subprocess.STDOUT, text=True)
            return res.strip()
        except subprocess.CalledProcessError as e:
            if attempt < retries:
                time.sleep(2 * attempt)
                continue
            print(f"[ERROR] Command {' '.join(cmd)} failed after {retries} attempts: {e.output}", file=sys.stderr)
            return None


def check_pr_status(repo, number):
    cmd = ["gh", "pr", "view", str(number), "--repo", repo, "--json", "state,mergedAt,url"]
    out = run_cmd(cmd)
    if not out:
        return None
    try:
        return json.loads(out)
    except Exception:
        return None


def check_cognee_assignment(issue_number):
    cmd = ["gh", "issue", "view", str(issue_number), "--repo", "topoteretes/cognee", "--json", "assignees,state"]
    out = run_cmd(cmd)
    if not out:
        return []
    try:
        data = json.loads(out)
        return [a["login"].lower() for a in data.get("assignees", [])]
    except Exception:
        return []


def audit_portfolio():
    print("=" * 60)
    print(f"PORTFOLIO AUDIT START: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 60)

    # 1. Audit Tracked PRs
    any_merged = False
    print("\n[STEP 1] Auditing Tracked PRs...")
    for item in TRACKED_PRS:
        pr_info = check_pr_status(item["repo"], item["number"])
        if pr_info:
            state = pr_info.get("state", "UNKNOWN")
            print(f"  - {item['name']} ({item['repo']}#{item['number']}): [{state}]")
            if state == "MERGED":
                any_merged = True
        else:
            print(f"  - {item['name']} ({item['repo']}#{item['number']}): [FAILED TO QUERY]")

    # 2. If any PR merged, trigger sync_merged_prs.py
    if any_merged:
        print("\n[ACTION] Detected MERGED PR. Synchronizing merged PRs feed in README...")
        sync_merged_cmd = ["/usr/bin/python3", os.path.join(SCRIPTS_DIR, "sync_merged_prs.py")]
        run_cmd(sync_merged_cmd, cwd=SOMUAI_DIR)
    else:
        # Run sync_merged_prs.py anyway to ensure feed matches upstream state
        sync_merged_cmd = ["/usr/bin/python3", os.path.join(SCRIPTS_DIR, "sync_merged_prs.py")]
        run_cmd(sync_merged_cmd, cwd=SOMUAI_DIR)

    # 3. Check Cognee Assignments & Instant PR Trigger
    print("\n[STEP 2] Auditing Cognee Connector Assignments...")
    for item in TRACKED_COGNEE_ISSUES:
        assignees = check_cognee_assignment(item["issue"])
        print(f"  - {item['name']} (topoteretes/cognee#{item['issue']}): assignees={assignees}")
        if "somuai" in assignees:
            print(f"  [TRIGGER] Issue #{item['issue']} is assigned to @somuai! Opening upstream PR...")
            if os.path.exists(SUBMIT_SCRIPT):
                res = run_cmd([SUBMIT_SCRIPT, item["target"]])
                print(f"  [SUBMIT RESULT] {res}")

    # 4. Check Accepted Answers ("Mark for answer")
    print("\n[STEP 3] Auditing Accepted Discussion Answers...")
    sync_answers_cmd = ["/usr/bin/python3", os.path.join(SCRIPTS_DIR, "sync_accepted_answers.py")]
    run_cmd(sync_answers_cmd, cwd=SOMUAI_DIR)

    # 5. Check if README.md was modified and commit/push
    print("\n[STEP 4] Checking for README.md changes...")
    diff_out = run_cmd(["git", "diff", "--name-only", "README.md"], cwd=SOMUAI_DIR)
    if diff_out and "README.md" in diff_out:
        print("  [UPDATE] README.md has changed. Committing and pushing...")
        commit_msg = "docs: sync profile with latest merged contributions and accepted answers [skip ci]"
        run_cmd(["git", "add", "README.md"], cwd=SOMUAI_DIR)
        run_cmd(["git", "commit", "-s", "-m", commit_msg], cwd=SOMUAI_DIR)
        push_out = run_cmd(["git", "-c", f"http.proxy={PROXY_URL}", "push", "origin", "main"], cwd=SOMUAI_DIR)
        print(f"  [PUSH] {push_out}")
    else:
        print("  [OK] Profile README is up to date. Zero changes pending.")

    print("\n" + "=" * 60)
    print(f"PORTFOLIO AUDIT COMPLETE: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 60)


if __name__ == "__main__":
    audit_portfolio()
