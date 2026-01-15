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
`canonical/`.

正本のバージョンは、既存の正本の最大バージョンを基に patch を +1 して決定します。
分類別仕様書の内容を実際に統合し、1冊の正本として出力します。
"""
import json
import os
import re
import datetime

# Regular expression to extract version string from file names like
# reforma-common-spec-v1.5.1.json
VERSION_RE = re.compile(r"v(\d+)\.(\d+)\.(\d+)")


def parse_version(version_str):
    """Parse a version string (e.g., 'v1.5.1') into a tuple of integers."""
    match = VERSION_RE.search(version_str)
    if not match:
        raise ValueError(f"Invalid version string: {version_str}")
    return tuple(int(part) for part in match.groups())


def version_to_str(ver_tuple):
    """Convert version tuple to string."""
    return f"v{ver_tuple[0]}.{ver_tuple[1]}.{ver_tuple[2]}"


def find_latest_spec_files(cat_dir, category):
    """Find the latest JSON and MD spec files for the given category.

    Returns:
        tuple: (json_path, md_path, version_string)
    """
    candidates = []
    for fname in os.listdir(cat_dir):
        if fname.startswith(f"reforma-{category}-spec-v") and fname.endswith(".json"):
            try:
                version = parse_version(fname)
                candidates.append((fname, version))
            except ValueError:
                continue
    if not candidates:
        return None, None, None
    candidates.sort(key=lambda x: x[1])
    latest_fname, latest_version = candidates[-1]
    json_path = os.path.join(cat_dir, latest_fname)
    md_fname = latest_fname.replace(".json", ".md")
    md_path = os.path.join(cat_dir, md_fname)
    if not os.path.isfile(md_path):
        md_path = None
    return json_path, md_path, version_to_str(latest_version)


def find_latest_canonical_version(canonical_dir):
    """Find the latest canonical spec version."""
    if not os.path.isdir(canonical_dir):
        return (1, 5, 0)  # Default starting version
    candidates = []
    for fname in os.listdir(canonical_dir):
        if fname.startswith("reforma-spec-v") and fname.endswith(".json"):
            try:
                ver = parse_version(fname)
                candidates.append(ver)
            except ValueError:
                continue
    if not candidates:
        return (1, 5, 0)
    candidates.sort()
    return candidates[-1]


def increment_patch(ver_tuple):
    """Increment the patch version."""
    return (ver_tuple[0], ver_tuple[1], ver_tuple[2] + 1)


def load_json_file(path):
    """Load JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_md_file(path):
    """Load Markdown file."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_canonical(project_root):
    classified_dir = os.path.join(project_root, "classified")
    canonical_dir = os.path.join(project_root, "canonical")

    # Discover categories (subdirectories of classified)
    categories = [d for d in os.listdir(classified_dir)
                  if os.path.isdir(os.path.join(classified_dir, d))]

    # Collect latest specs for each category
    component_manifest = {}
    category_contents = {}

    for category in categories:
        cat_dir = os.path.join(classified_dir, category)
        json_path, md_path, version_str = find_latest_spec_files(cat_dir, category)
        if not json_path:
            continue

        manifest_entry = {
            "version": version_str,
            "json_file": os.path.relpath(json_path, project_root),
            "md_file": os.path.relpath(md_path, project_root) if md_path else None
        }
        component_manifest[category] = manifest_entry

        # Load actual content
        category_contents[category] = {
            "version": version_str,
            "json": load_json_file(json_path),
            "md": load_md_file(md_path)
        }

    if not component_manifest:
        raise RuntimeError("No classification specs found to generate canonical spec.")

    # Determine new canonical version (increment patch from latest existing)
    latest_canonical = find_latest_canonical_version(canonical_dir)
    new_version_tuple = increment_patch(latest_canonical)
    canonical_version = version_to_str(new_version_tuple)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Build canonical JSON with full content
    canonical_data = {
        "metadata": {
            "project": "ReForma",
            "category": "overall",
            "version": canonical_version,
            "generated_at": now,
            "description": "分類別仕様書を統合した正本仕様書"
        },
        "component_manifest": component_manifest,
        "specifications": {}
    }

    # Include actual spec content
    for category in sorted(category_contents.keys()):
        content = category_contents[category]
        canonical_data["specifications"][category] = {
            "version": content["version"],
            "content": content["json"]
        }

    os.makedirs(canonical_dir, exist_ok=True)
    json_filename = f"reforma-spec-{canonical_version}.json"
    md_filename = f"reforma-spec-{canonical_version}.md"
    json_path = os.path.join(canonical_dir, json_filename)
    md_path = os.path.join(canonical_dir, md_filename)

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(canonical_data, f_json, ensure_ascii=False, indent=2)

    # Write Markdown (full content)
    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write(f"# ReForma 正本仕様書 {canonical_version}\n\n")
        f_md.write(f"**生成日時**: {now}\n\n")
        f_md.write("このドキュメントは最新の分類別仕様書から自動生成された統合版です。\n\n")
        f_md.write("---\n\n")

        f_md.write("## コンポーネント・マニフェスト\n\n")
        f_md.write("| 分類 | バージョン | JSON | Markdown |\n")
        f_md.write("| --- | --- | --- | --- |\n")
        for cat in sorted(component_manifest.keys()):
            entry = component_manifest[cat]
            md_file = entry['md_file'] or '-'
            json_file = entry['json_file'].replace('\\', '/')
            md_file_display = entry['md_file'].replace('\\', '/') if entry['md_file'] else '-'
            f_md.write(f"| {cat} | {entry['version']} | {json_file} | {md_file_display} |\n")

        f_md.write("\n---\n\n")

        # Include full Markdown content from each category
        category_order = ["common", "api", "backend", "frontend", "db", "notes"]
        for cat in category_order:
            if cat not in category_contents:
                continue
            content = category_contents[cat]
            f_md.write(f"# {cat.upper()} 仕様 ({content['version']})\n\n")
            if content["md"]:
                # Remove the first heading from embedded MD to avoid duplicate titles
                md_content = content["md"]
                lines = md_content.split('\n')
                # Skip first line if it's a heading
                if lines and lines[0].startswith('# '):
                    md_content = '\n'.join(lines[1:])
                f_md.write(md_content)
            else:
                f_md.write("（Markdown 版なし。JSON を参照してください。）\n")
            f_md.write("\n\n---\n\n")

    # Update README
    update_readme(project_root, canonical_version)

    print(f"Generated canonical spec: {json_path} and {md_path}")


def update_readme(project_root, new_version):
    """Update README.md to point to the new canonical spec version."""
    readme_path = os.path.join(project_root, "README.md")
    if not os.path.isfile(readme_path):
        return
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the canonical spec version references
    # Pattern: reforma-spec-vX.Y.Z
    old_pattern = r"reforma-spec-v\d+\.\d+\.\d+"
    new_ref = f"reforma-spec-{new_version}"
    content = re.sub(old_pattern, new_ref, content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    generate_canonical(project_root)


if __name__ == "__main__":
    main()
