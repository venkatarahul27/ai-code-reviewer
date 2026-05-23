"""
AI Code Reviewer — Main orchestrator.
Pulls a GitHub PR diff, sends it through Claude for analysis,
and posts inline review comments back on the PR.
"""

import asyncio
import argparse
import os

from .diff_parser import parse_diff, chunk_hunks
from .analyzer import analyze_chunks
from .commenter import post_review_comments
from .config import load_config


async def review_pr(repo: str, pr_number: int, config_path: str = ".codereview.yml"):
    config = load_config(config_path)
    github_token = os.environ["GITHUB_TOKEN"]

    hunks = parse_diff(repo, pr_number, github_token)
    chunks = chunk_hunks(hunks, max_tokens=2048)

    findings = await analyze_chunks(chunks, config)

    filtered = [
        f for f in findings
        if f["severity"] >= config.severity_threshold
    ]

    if filtered:
        post_review_comments(repo, pr_number, filtered, github_token)
        print(f"Posted {len(filtered)} review comments on PR #{pr_number}")
    else:
        print(f"No issues found above threshold for PR #{pr_number}")

    return filtered


def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, type=int, help="PR number")
    parser.add_argument("--config", default=".codereview.yml", help="Config file path")
    args = parser.parse_args()

    findings = asyncio.run(review_pr(args.repo, args.pr, args.config))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
