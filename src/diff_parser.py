"""Git diff parsing and chunking utilities."""

from dataclasses import dataclass

from github import Github


@dataclass
class DiffHunk:
    file: str
    start_line: int
    end_line: int
    diff: str
    language: str


EXTENSION_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".cs": "csharp", ".java": "java", ".go": "go", ".rs": "rust",
    ".rb": "ruby", ".cpp": "cpp", ".c": "c",
}


def detect_language(file_path: str) -> str:
    for ext, lang in EXTENSION_MAP.items():
        if file_path.endswith(ext):
            return lang
    return "unknown"


def parse_diff(repo: str, pr_number: int, token: str) -> list[DiffHunk]:
    gh = Github(token)
    pull = gh.get_repo(repo).get_pull(pr_number)

    hunks = []
    for file in pull.get_files():
        if not file.patch:
            continue

        language = detect_language(file.filename)
        hunks.append(DiffHunk(
            file=file.filename,
            start_line=1,
            end_line=file.changes,
            diff=file.patch,
            language=language,
        ))

    return hunks


def chunk_hunks(hunks: list[DiffHunk], max_tokens: int = 2048) -> list[dict]:
    chunks = []
    for hunk in hunks:
        estimated_tokens = len(hunk.diff) // 4
        if estimated_tokens <= max_tokens:
            chunks.append({"file": hunk.file, "diff": hunk.diff, "language": hunk.language})
        else:
            lines = hunk.diff.split("\n")
            current_chunk: list[str] = []
            current_size = 0
            for line in lines:
                line_tokens = len(line) // 4
                if current_size + line_tokens > max_tokens and current_chunk:
                    chunks.append({
                        "file": hunk.file,
                        "diff": "\n".join(current_chunk),
                        "language": hunk.language,
                    })
                    current_chunk = []
                    current_size = 0
                current_chunk.append(line)
                current_size += line_tokens
            if current_chunk:
                chunks.append({
                    "file": hunk.file,
                    "diff": "\n".join(current_chunk),
                    "language": hunk.language,
                })

    return chunks
