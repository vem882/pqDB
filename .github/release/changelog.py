"""Describe the differences from the last released version of this addon."""

from __future__ import annotations

import html
import re
import subprocess
from pathlib import PurePosixPath

GAMES = {
    "Anniversary": "TBC Anniversary",
    "Era": "Classic Era",
    "Forever": "WoW Forever",
}
DATA_FILES = {"Items.lua", "Npcs.lua", "Objects.lua", "Quests.lua"}
DATA_ROW = re.compile(r"^\[(\d+)\]\s*=\s*(.+)$", re.MULTILINE)
VERSION_TAG = re.compile(r"v(\d+(?:\.\d+)+)")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8")


def previous_tag(version: str) -> str:
    current = tuple(map(int, version.split(".")))
    for tag in git("tag", "--merged", "HEAD", "--sort=-version:refname").splitlines():
        if (match := VERSION_TAG.fullmatch(tag)) and tuple(map(int, match[1].split("."))) < current:
            return tag
    raise ValueError(f"No earlier release tag found for {version}")


def changes(base: str, addon: str) -> dict[str, list[str]]:
    grouped = {"Added": [], "Changed": [], "Removed": []}
    diff = git("diff", "--name-status", "--no-renames", "-z", base, "HEAD")
    fields = diff[:-1].split("\0") if diff else []
    for status, path in zip(fields[::2], fields[1::2], strict=True):
        folder = "Addon" if path.startswith(f"{addon}/") else "Repository"
        name = path.removeprefix(f"{addon}/")
        category = {"A": "Added", "D": "Removed"}.get(status, "Changed")
        grouped[category].append(f"- {folder} <code>{html.escape(name)}</code>")
    return grouped


def data_changes(base: str, addon: str) -> list[str]:
    paths = git("diff", "--name-only", "--no-renames", "-z", base, "HEAD", "--", addon).split("\0")
    lines = []
    for path in paths:
        parts = PurePosixPath(path).parts
        if not parts or parts[-1] not in DATA_FILES or parts[-2] != "Data":
            continue
        delta = git("diff", "--no-ext-diff", "--unified=0", base, "HEAD", "--", path)
        before, after = {}, {}
        for line in delta.splitlines():
            if not line.startswith(("+[", "-[")):
                continue
            if match := DATA_ROW.fullmatch(line[1:]):
                (after if line[0] == "+" else before)[match[1]] = match[2]
        added = len(after.keys() - before.keys())
        removed = len(before.keys() - after.keys())
        changed = sum(before[key] != after[key] for key in before.keys() & after.keys())
        if added or removed or changed:
            game = GAMES.get(parts[-3], "MoP Classic")
            kind = parts[-1].removesuffix(".lua")
            lines.append(f"- {game} {kind.lower()} — {added:,} added, {changed:,} changed, {removed:,} removed")
    return lines


def release_changelog(addon: str, version: str) -> bytes:
    base = previous_tag(version)
    title = [f"# {addon} {version}", "", f"Changes since {base}.", ""]
    commits = git("log", "--no-merges", "--format=%s", f"{base}..HEAD").splitlines()
    if commits:
        title.extend(["## Summary", "", *(f"- {html.escape(commit)}" for commit in commits), ""])
    if addon == "PandaQuestDB" and (rows := data_changes(base, addon)):
        title.extend(["## Game data", "", *rows, ""])
    for section, entries in changes(base, addon).items():
        title.extend([f"## {section}", "", *(entries or ["No entries."]), ""])
    return "\n".join(title).encode("utf-8")
