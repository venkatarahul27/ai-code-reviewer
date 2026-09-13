# AI Code Reviewer

A Python CLI prototype that retrieves GitHub pull-request diffs, sends chunks to Claude for analysis, filters findings by severity, and posts inline review comments.

## Current Status

The core review pipeline is implemented. Automated test cases and a GitHub Actions workflow have not been added yet.

- Reviews diff chunks for potential bugs, security issues, performance problems, and error-handling gaps.
- Uses a default minimum severity of medium when no configuration file is present.
- Posts findings as GitHub review comments. Running the CLI can create comments on the specified pull request.
- Configuration support is incomplete: focus areas, ignore patterns, and comment limits are not currently enforced by the review pipeline.
- Model errors can currently be omitted from the collected results. An empty result is not proof that a pull request is free of issues.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  GitHub PR   │────▶│  Diff Parser  │────▶│  Claude AI      │
│  CLI input   │     │  & Chunker    │     │  Analysis       │
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

The CLI reads `ANTHROPIC_API_KEY` and `GITHUB_TOKEN` from the environment. The GitHub token must have access to the selected repository and permission to submit review comments.

Use the default configuration by leaving `.codereview.yml` absent. The YAML configuration loader needs further validation before custom configuration can be relied on.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Engine | Claude via the Anthropic SDK; model configured in `src/analyzer.py` |
| Language | Python 3.11+ |
| GitHub Integration | PyGithub |

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
│   └── __init__.py        # Test package placeholder; test cases are planned
├── requirements.txt
└── README.md
```

## Development Roadmap

- [ ] Add unit tests for parsing, analysis, configuration, and comment construction.
- [ ] Validate model responses and distinguish API failures from clean reviews.
- [ ] Enforce configured ignore patterns, focus areas, and comment limits.
- [ ] Validate comment locations against the pull-request diff.
- [ ] Add a reproducible example and GitHub Actions integration.

## Contributing

Focused improvements are welcome. Include reproduction steps and relevant tests with behavior changes.

## License

[MIT](LICENSE)
