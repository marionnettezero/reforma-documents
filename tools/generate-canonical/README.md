# generate-canonical

This directory contains a simple Python script to generate the ReForma canonical specification from the latest classification documents.

## Usage

1. Ensure that Python 3 is installed on your system.
2. From the root of the repository (the directory containing `classified/` and `canonical/`), run:

```bash
python tools/generate-canonical/generate_canonical.py
```

The script scans the `classified/` directory for JSON specification files (e.g., `reforma-common-spec-v1.5.0.json`) and identifies the highest semantic version for each category. It then creates a canonical JSON file and a Markdown summary in the `canonical/` directory. The canonical version number is derived from the highest version among the classifications.

The generator does not currently merge the actual content of the specs; instead, it builds a manifest pointing to the latest versions. You can extend the script to perform deeper content merging if needed.

## Automating with GitHub Actions

To automatically regenerate and commit the canonical spec whenever classification docs change, create a workflow file (e.g., `.github/workflows/generate_canonical.yml`) with the following steps:

```yaml
name: Generate canonical spec
on:
  push:
    paths:
      - 'classified/**'
      - 'tools/generate-canonical/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Generate canonical spec
        run: python tools/generate-canonical/generate_canonical.py

      - name: Commit and push changes
        uses: EndBug/add-and-commit@v9
        with:
          add: 'canonical/*'
          message: 'chore: regenerate canonical spec'
          default_author: github_actions
          push: true
```

This workflow triggers on any change under `classified/` or `tools/generate-canonical/`. It checks out the repository, runs the generator script, and commits any updates to the `canonical/` folder back to the repository using the [Add & Commit GitHub Action]【417625223897387†L192-L214】.

## Notes

- Ensure the action has sufficient permissions to push to your repository's default branch.
- Adjust the Python version or additional dependencies in the workflow as needed.
