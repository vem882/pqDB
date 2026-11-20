"""Validate and package the component's game-specific addon files."""

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from changelog import release_changelog

addon, project, version, filename, notes = sys.argv[1:]
root = Path(addon)
tracked = subprocess.check_output(["git", "ls-files", "-z", "--", addon]).decode().split("\0")
files = {name: Path(name).read_bytes() for name in tracked if name}
interfaces = {"": 50504, "_Mists": 50504, "_Vanilla": 11509, "_TBC": 20506, "_Forever": 16001, "_Camelot": 16001}
expected_tocs = {f"{addon}/{addon}{suffix}.toc" for suffix in interfaces}
assert {name for name in files if Path(name).parent == root and name.endswith(".toc")} == expected_tocs
for suffix, interface in interfaces.items():
    name = f"{addon}/{addon}{suffix}.toc"
    toc = files[name].decode()
    assert f"## Interface: {interface}" in toc.splitlines(), name
    assert f"## X-Curse-Project-ID: {project}" in toc.splitlines(), name
    expected_dependency = addon == "PandaQuestAuction"
    assert ("## Dependencies: PandaQuest" in toc.splitlines()) == expected_dependency, name
    for line in toc.splitlines():
        line = line.strip().replace("\\", "/")
        if line and not line.startswith("#"):
            assert f"{addon}/{line}" in files, f"{name} references missing {line}"
    toc, count = re.subn(r"(?mi)^## Version:.*$", f"## Version: {version}", toc)
    assert count == 1, name
    files[name] = toc.encode()
assert f"{addon}/Textures/icon.tga" in files
changelog = release_changelog(addon, version)
files[f"{addon}/CHANGELOG.md"] = changelog
Path(notes).write_bytes(changelog)
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name, content in sorted(files.items()):
        info = zipfile.ZipInfo(name)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, content, compresslevel=9)
    archive.comment = json.dumps({
        "component": commit,
        "version": version,
        "changelog_sha256": hashlib.sha256(changelog).hexdigest(),
    }, sort_keys=True).encode()
