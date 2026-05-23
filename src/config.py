"""Configuration loader for .codereview.yml."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


SEVERITY_MAP = {"low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass
class ReviewConfig:
    severity_threshold: int = 2
    focus_areas: list[str] = field(default_factory=lambda: ["security", "bugs", "performance"])
    ignore_patterns: list[str] = field(default_factory=list)
    max_comments: int = 15


def load_config(path: str = ".codereview.yml") -> ReviewConfig:
    config_file = Path(path)
    if not config_file.exists():
        return ReviewConfig()

    with open(config_file) as f:
        raw = yaml.safe_load(f) or {}

    threshold_str = raw.get("severity_threshold", "medium")
    return ReviewConfig(
        severity_threshold=SEVERITY_MAP.get(threshold_str, 2),
        focus_areas=raw.get("focus_areas", ReviewConfig.focus_areas),
        ignore_patterns=raw.get("ignore_patterns", []),
        max_comments=raw.get("max_comments", 15),
    )
