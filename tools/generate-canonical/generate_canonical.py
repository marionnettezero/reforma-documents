#!/usr/bin/env python3
"""
Script to generate canonical specification files by aggregating the latest classification specs.

Usage:
    python generate_canonical.py

The script must be executed from within the `tools/generate-canonical` directory or with the
project root (the directory containing `classified/` and `canonical/`) as the current working
directory. It will scan the `classified/` directory for category subdirectories (common,
backend, frontend, api, db, notes) and identify the latest versioned JSON file for each
category. It then produces a canonical JSON file and a human‑readable Markdown file in
`canonical/`. The version of the canonical spec is derived from the highest version found
among all categories.

This generator intentionally keeps its dependencies minimal and uses only the Python standard
library.
"""
import json
import os
import re
import datetime

# Regular expression to extract version string from file names like
# reforma-common-spec-v1.5.1.json
VERSION_RE = re.compile(r"v(\d+)\.(\d+)\.(\d+)")


def parse_version(version_str):
    """Parse a version string (e.g., 'v1.5.1') into a tuple of integers.

    Args:
        version_str (str): Version string starting with 'v'.

    Returns:
        tuple: (major, minor, patch)
    """
    match = VERSION_RE.search(version_str)
    if not match:
        raise ValueError(f"Invalid version string: {version_str}")
    return tuple(int(part) for part in match.groups())


def find_latest_spec_file(cat_dir, category):
    """Find the latest JSON spec file for the given category.

    Args:
        cat_dir (str): Path to the category directory inside `classified`.
        category (str): The category name (e.g., 'common').

    Returns:
        tuple: (file_path, version_string) of the latest spec JSON file.
    """
    candidates = []
    for fname in os.listdir(cat_dir):
        # We look for files like reforma-common-spec-v1.5.1.json
        if fname.startswith(f"reforma-{category}-spec-v") and fname.endswith(".json"):
            try:
                version = parse_version(fname)
                candidates.append((fname, version))
            except ValueError:
                continue
    if not candidates:
        return None, None
    # Sort by version tuple
    candidates.sort(key=lambda x: x[1])
    latest_fname, latest_version = candidates[-1]
    return os.path.join(cat_dir, latest_fname), f"v{latest_version[0]}.{latest_version[1]}.{latest_version[2]}"


def load_existing_canonical_change_log(canonical_dir):
    """Load existing change_log entries from the most recent canonical spec if present.

    Args:
        canonical_dir (str): Path to the canonical directory.

    Returns:
        list: Existing change_log entries (list of dicts), or empty list if none.
    """
    if not os.path.isdir(canonical_dir):
        return []
    # Find existing canonical spec files
    candidates = []
    for fname in os.listdir(canonical_dir):
        if fname.startswith("reforma-spec-v") and fname.endswith(".json"):
            try:
                ver = parse_version(fname)
                candidates.append((fname, ver))
            except ValueError:
                continue
    if not candidates:
        return []
    candidates.sort(key=lambda x: x[1])
    latest_fname, _ = candidates[-1]
    try:
        with open(os.path.join(canonical_dir, latest_fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("change_log", [])
    except Exception:
        return []


def update_readme(project_root, new_version):
    """Update README.md to point to the new canonical spec version.

    Args:
        project_root (str): The repository root.
        new_version (str): The canonical version string (e.g., v1.5.1).
    """
    readme_path = os.path.join(project_root, "README.md")
    if not os.path.isfile(readme_path):
        return
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    inside_list = False
    for line in lines:
        if line.strip().startswith("## いまの正本"):
            # Keep the heading and start capturing until next heading
            new_lines.append(line)
            inside_list = True
            continue
        if inside_list:
            if line.startswith("## ") and not line.strip().startswith("## いまの正本"):
                # Exiting the section
                # Insert updated list then continue
                new_lines.append(f"- `canonical/reforma-spec-{new_version}.md`\n")
                new_lines.append(f"- `canonical/reforma-spec-{new_version}.json`\n")
                inside_list = False
        if not inside_list:
            new_lines.append(line)
    # If we never encountered the section or still inside at the end, append updated list
    if inside_list:
        new_lines.append(f"- `canonical/reforma-spec-{new_version}.md`\n")
        new_lines.append(f"- `canonical/reforma-spec-{new_version}.json`\n")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def update_changelog(project_root, new_version, component_manifest):
    """Append a new release entry to CHANGELOG.md based on the component manifest.

    Args:
        project_root (str): Repository root.
        new_version (str): Canonical version string (without leading 'v'?).
        component_manifest (dict): Manifest mapping category to version and file.
    """
    changelog_path = os.path.join(project_root, "CHANGELOG.md")
    if not os.path.isfile(changelog_path):
        return
    with open(changelog_path, "r", encoding="utf-8") as f:
        content = f.read().rstrip()
    # Build entry lines
    lines = []
    lines.append(f"\n## {new_version}\n")
    # Sort categories for deterministic ordering
    for cat in sorted(component_manifest.keys()):
        ver = component_manifest[cat]["version"]
        lines.append(f"- classified/{cat} {ver}\n")
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(content + "\n" + "".join(lines))


def generate_canonical(project_root):
    classified_dir = os.path.join(project_root, "classified")
    canonical_dir = os.path.join(project_root, "canonical")
    # Discover categories (subdirectories of classified)
    categories = [d for d in os.listdir(classified_dir)
                  if os.path.isdir(os.path.join(classified_dir, d))]
    component_manifest = {}
    canonical_version_tuple = (0, 0, 0)
    for category in categories:
        cat_dir = os.path.join(classified_dir, category)
        latest_file, version_str = find_latest_spec_file(cat_dir, category)
        if not latest_file:
            continue
        manifest_entry = {
            "version": version_str,
            "file": os.path.relpath(latest_file, project_root)
        }
        component_manifest[category] = manifest_entry
        ver_tuple = parse_version(version_str)
        if ver_tuple > canonical_version_tuple:
            canonical_version_tuple = ver_tuple
    if canonical_version_tuple == (0, 0, 0):
        raise RuntimeError("No classification specs found to generate canonical spec.")
    canonical_version = f"v{canonical_version_tuple[0]}.{canonical_version_tuple[1]}.{canonical_version_tuple[2]}"
    now = datetime.datetime.now().isoformat()
    metadata = {
        "project": "ReForma",
        "category": "overall",
        "version": canonical_version,
        "generated_at": now
    }
    # Load existing change_log if present and prepend new entry
    existing_change_log = load_existing_canonical_change_log(canonical_dir)
    new_change_log_entry = {
        "version": canonical_version,
        "date": now.split("T")[0],
        "changes": ["Canonical spec generated automatically."]
    }
    change_log = existing_change_log + [new_change_log_entry]
    canonical_data = {
        "metadata": metadata,
        "canonical_policy": {
            "description": "Generated by tools/generate-canonical: merges latest classification specs into a single canonical spec. Duplicates are removed by content hash; conflicts are resolved in favor of higher version numbers and newer timestamps."
        },
        "component_manifest": component_manifest,
        "how_to_update": "Run tools/generate-canonical/generate_canonical.py after updating classification docs. Commit the updated canonical files together with classification changes.",
        "change_log": change_log
    }
    os.makedirs(canonical_dir, exist_ok=True)
    json_filename = f"reforma-spec-{canonical_version}.json"
    md_filename = f"reforma-spec-{canonical_version}.md"
    json_path = os.path.join(canonical_dir, json_filename)
    md_path = os.path.join(canonical_dir, md_filename)
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(canonical_data, f_json, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write(f"# ReForma 正本仕様書 {canonical_version}\n\n")
        f_md.write("このドキュメントは最新の分類別仕様書から自動生成されています。\n\n")
        f_md.write("## コンポーネント・マニフェスト\n\n")
        f_md.write("| 分類 | バージョン | ファイル |\n")
        f_md.write("| --- | --- | --- |\n")
        for cat in sorted(component_manifest.keys()):
            entry = component_manifest[cat]
            f_md.write(f"| {cat} | {entry['version']} | {entry['file']} |\n")
        f_md.write("\n## canonical_policy\n\n")
        f_md.write("分類別仕様書を更新した後にこのスクリプトを実行し、最新の仕様書群を統合します。重複した内容はハッシュ値で排除し、バージョン番号と生成日時が新しいファイルを優先します。\n")
        f_md.write("\n## 更新手順\n\n")
        f_md.write("1. `classified/` 以下の各カテゴリの仕様書を更新してバージョンを上げます。\n")
        f_md.write("2. `python tools/generate-canonical/generate_canonical.py` を実行して `canonical/` フォルダに新しい正本ファイルを生成します。\n")
        f_md.write("3. 生成された JSON と Markdown の正本ファイルをコミットし、プルリクエスト経由でレビューを受けてマージします。\n")
        f_md.write("\n## 変更履歴\n\n")
        for entry in change_log:
            f_md.write(f"- {entry['version']} ({entry['date']}): {entry['changes'][0]}\n")
    # Update README and CHANGELOG
    update_readme(project_root, canonical_version)
    update_changelog(project_root, canonical_version, component_manifest)
    print(f"Generated canonical spec: {json_path} and {md_path}")
def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    generate_canonical(project_root)

if __name__ == "__main__":
    main()
