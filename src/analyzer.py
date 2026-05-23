"""Claude-powered code analysis engine."""

import asyncio
import json
import os
from typing import Any

import anthropic

REVIEW_SYSTEM_PROMPT = """You are an expert code reviewer. Analyze the following code diff and identify:
1. Bugs or logic errors
2. Security vulnerabilities (injection, auth issues, data exposure)
3. Performance problems (N+1 queries, unnecessary allocations, blocking calls)
4. Error handling gaps

For each finding, respond with JSON:
{
  "findings": [
    {
      "line": <line_number>,
      "file": "<file_path>",
      "severity": "low" | "medium" | "high" | "critical",
      "category": "bug" | "security" | "performance" | "error_handling",
      "message": "<concise explanation>",
      "suggestion": "<fix suggestion>"
    }
  ]
}

Only report real issues. Do not flag style preferences or nitpicks."""

SEVERITY_MAP = {"low": 1, "medium": 2, "high": 3, "critical": 4}


async def analyze_single_chunk(client: anthropic.AsyncAnthropic, chunk: dict) -> list[dict]:
    diff_text = chunk["diff"]
    file_path = chunk["file"]

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=REVIEW_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"File: {file_path}\n\nDiff:\n```\n{diff_text}\n```"}],
    )

    try:
        result = json.loads(response.content[0].text)
        findings = result.get("findings", [])
        for f in findings:
            f["severity"] = SEVERITY_MAP.get(f.get("severity", "low"), 1)
        return findings
    except (json.JSONDecodeError, IndexError, KeyError):
        return []


async def analyze_chunks(chunks: list[dict], config: Any) -> list[dict]:
    client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    tasks = [analyze_single_chunk(client, chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    findings = []
    for result in results:
        if isinstance(result, list):
            findings.extend(result)

    return findings
