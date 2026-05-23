"""GitHub PR comment builder and poster."""

from github import Github


def post_review_comments(repo: str, pr_number: int, findings: list[dict], token: str):
    gh = Github(token)
    pull = gh.get_repo(repo).get_pull(pr_number)
    commit = pull.get_commits().reversed[0]

    comments = []
    for finding in findings:
        severity_label = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}.get(
            finding["severity"], "Info"
        )
        category = finding.get("category", "general").replace("_", " ").title()

        body = (
            f"**[{severity_label}] {category}**\n\n"
            f"{finding['message']}\n\n"
        )
        if finding.get("suggestion"):
            body += f"**Suggestion:** {finding['suggestion']}\n"

        comments.append({
            "path": finding["file"],
            "line": finding["line"],
            "body": body,
        })

    if comments:
        pull.create_review(
            commit=commit,
            body=f"AI Code Review: found {len(comments)} issue(s)",
            comments=comments,
            event="COMMENT",
        )
