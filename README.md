# AI Code Reviewer

Automated code review assistant powered by Claude AI. Analyzes pull requests for bugs, security vulnerabilities, performance issues, and code quality — then posts inline review comments directly on GitHub.

## Features

- **Multi-dimensional Analysis** — checks for bugs, security flaws, performance bottlenecks, and style issues in a single pass
- **Inline PR Comments** — posts findings as GitHub review comments on the exact lines that need attention
- **Context-Aware** — understands the full diff context, not just individual lines
- **Configurable Rules** — customize severity thresholds, ignore patterns, and focus areas via `.codereview.yml`
- **CI/CD Ready** — runs as a GitHub Action or standalone CLI tool

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  GitHub PR   │────▶│  Diff Parser  │────▶│  Claude AI      │
│  Webhook     │     │  & Chunker    │     │  Analysis       │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                          ┌────────▼────────┐
                                          │  Review Builder  │
                                          │  & PR Commenter  │
                                          └─────────────────┘
```

## Quick Start

```bash
# Clone the repo
git clone https://github.com/venkatarahul27/ai-code-reviewer.git
cd ai-code-reviewer

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY=your_key
export GITHUB_TOKEN=your_token

# Run on a PR
python -m src.reviewer --repo owner/repo --pr 42
```

## Configuration

Create a `.codereview.yml` in your repo root:

```yaml
severity_threshold: medium
focus_areas:
  - security
  - performance
  - error_handling
ignore_patterns:
  - "*.test.py"
  - "docs/**"
max_comments: 15
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Engine | Claude 3.5 (Anthropic SDK) |
| Language | Python 3.11+ |
| API Framework | FastAPI |
| GitHub Integration | PyGithub |
| Testing | pytest + pytest-asyncio |

## Project Structure

```
ai-code-reviewer/
├── src/
│   ├── __init__.py
│   ├── reviewer.py        # Main review orchestrator
│   ├── diff_parser.py     # Git diff parsing & chunking
│   ├── analyzer.py        # Claude AI analysis engine
│   ├── commenter.py       # GitHub PR comment builder
│   └── config.py          # Configuration loader
├── tests/
│   ├── test_reviewer.py
│   ├── test_diff_parser.py
│   └── test_analyzer.py
├── .codereview.yml
├── requirements.txt
└── README.md
```

## License

MIT
