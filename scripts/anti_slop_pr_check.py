#!/usr/bin/env python3
"""
scripts/anti_slop_pr_check.py — Krittika-Shuddhi Engine

Project Krittika: Deterministic Pre-Flight Anti-Slop Constraint Checker for Open-Source PRs & Q&A.
Inspired by Lauren Tan's "All Code Is Slop (Except Mine)" (SpaceXSI / Grok Bot).
Enforces hard system constraints over prose instructions before any PR is submitted.
"""

import sys
import os
import re
import subprocess
import argparse

BANNED_DIFF_PATTERNS = [
    # Concurrency race condition masking
    (r"\bsetTimeout\s*\(", "anti-slop/no-masked-race-condition", "Ban on setTimeout() to mask async race conditions. Use deterministic promises, events, or state machine synchronization."),
    (r"\bsetInterval\s*\(", "anti-slop/no-masked-race-condition", "Ban on setInterval(). Use deterministic triggers."),
    (r"\btime\.sleep\s*\(\s*0?\.[0-9]+", "anti-slop/no-masked-race-condition", "Ban on arbitrary fractional time.sleep() to wait for async completion."),
    (r"\basyncio\.sleep\s*\(\s*0?\.[0-9]+", "anti-slop/no-masked-race-condition", "Ban on arbitrary asyncio.sleep() to wait for async tasks."),
    
    # Conversational AI commentary and stubs
    (r"(?i)//\s*this function (handles|implements|takes|returns)", "anti-slop/no-ai-commentary", "Conversational AI comment pattern detected. Code must be self-explanatory."),
    (r"(?i)#\s*this function (handles|implements|takes|returns)", "anti-slop/no-ai-commentary", "Conversational AI comment pattern detected. Code must be self-explanatory."),
    (r"(?i)//\s*helper function to", "anti-slop/no-ai-commentary", "Generic AI helper comment detected."),
    (r"(?i)#\s*helper function to", "anti-slop/no-ai-commentary", "Generic AI helper comment detected."),
    (r"(?i)\btodo:?\s*implement", "anti-slop/no-stubs", "Incomplete TODO stub detected in production code."),
    (r"(?i)\bfixme:?\s*", "anti-slop/no-stubs", "FIXME stub detected in production code."),
    
    # Silent error swallowing
    (r"except(\s+\w+)?:\s*pass\b", "anti-slop/no-empty-except", "Empty except block with pass detected. All exceptions must be logged or handled."),
    (r"catch\s*\([^)]*\)\s*\{\s*\}", "anti-slop/no-empty-catch", "Empty catch block detected. All errors must be logged or rethrown."),
    
    # Loose equality in JS/TS
    (r"\b==\b(?!=)", "anti-slop/strict-equality", "Loose equality (==) detected. Use strict equality (===)."),
    (r"\b!=\b(?!=)", "anti-slop/strict-equality", "Loose inequality (!=) detected. Use strict inequality (!==)."),
    
    # Emojis in code or comments
    (r"[\U00010000-\U0010ffff]", "anti-slop/zero-emojis", "Emoji detected in code, diff, or comment. Strict zero-emoji policy enforced."),
]

def check_diff(repo_dir, base_ref="main"):
    print(f"[ANTI-SLOP AUDIT] Auditing repository diff: {repo_dir} (against {base_ref})...")
    
    try:
        diff_cmd = ["git", "-C", repo_dir, "diff", f"{base_ref}...HEAD"]
        diff_output = subprocess.check_output(diff_cmd, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Fallback to local unstaged diff if no branch fork
        diff_cmd = ["git", "-C", repo_dir, "diff", "HEAD~1"]
        try:
            diff_output = subprocess.check_output(diff_cmd, text=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to run git diff: {e.stderr}", file=sys.stderr)
            return False, []

    violations = []
    lines = diff_output.split("\n")
    current_file = None
    line_number = 0
    test_files_touched = []

    for line in lines:
        if line.startswith("+++ b/"):
            current_file = line[6:]
            if "test" in current_file.lower():
                test_files_touched.append(current_file)
            continue

        if line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:]
            line_number += 1
            
            for pattern, rule, msg in BANNED_DIFF_PATTERNS:
                if re.search(pattern, added_content):
                    violations.append({
                        "file": current_file,
                        "rule": rule,
                        "line": line_number,
                        "snippet": added_content.strip()[:80],
                        "message": msg
                    })

    # Rule: Negative-Proof Regression Test must be present
    has_test = len(test_files_touched) > 0
    if not has_test and len(lines) > 20:
        violations.append({
            "file": "CHANGESET",
            "rule": "anti-slop/missing-negative-proof",
            "line": 1,
            "snippet": f"Touched files: {len(test_files_touched)} tests",
            "message": "Zero-Slop Invariant Violated: PR diff modifies code without including a test file proving reproduction."
        })

    return len(violations) == 0, violations

def main():
    parser = argparse.ArgumentParser(description="Krittika-Shuddhi: Pre-Flight Anti-Slop Linter for PR Contributions")
    parser.add_argument("--repo", default=".", help="Target git repository path")
    parser.add_argument("--base", default="main", help="Base git reference (default: main)")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
    clean, violations = check_diff(repo_path, args.base)

    if clean:
        print(f"[KRITTIKA-SHUDDHI: OK] 100% Anti-Slop Compliant! Zero banned patterns detected. Proof-driven invariants satisfied.")
        sys.exit(0)
    else:
        print(f"[KRITTIKA-SHUDDHI: REJECTED] Anti-Slop Linter blocked changeset with {len(violations)} violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  - [{v['rule']}] {v['file']}: {v['message']} (Snippet: '{v['snippet']}')", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
