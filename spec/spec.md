---
type: master-requirements
name: pytest-summary
org: agent-ix
component_type: github-actions
implementation_language: python
depends_on: []
---

# Master Requirements Specification

## Purpose

Pytest Summary is a composite GitHub Action that renders a human-readable summary
of failed tests into the GitHub Actions job summary. It consumes a
[`pytest-json-report`](https://github.com/pytest-dev/pytest-json-report) output
file and writes a collapsible Markdown report to `$GITHUB_STEP_SUMMARY`, so that
test failures are visible directly in the CI run page without digging through raw
logs. The action exists to give monorepos, shared workflows, and reusable CI
pipelines a consistent, low-effort way to surface failing tests and collection
errors to developers reviewing a run.

## Scope

This specification covers the composite action contract (`action.yml`) and the
Python summarizer (`main.py`) that backs it. In scope:

- The single `report-path` input (default `pytest.json`) and its resolution.
- Parsing the JSON report and selecting failed `tests` and failed `collectors`.
- Emitting a collapsible `<details>` block per failure with node id, `longrepr`
  traceback, and captured output, or an "All tests passed" message when none fail.
- Writing output to the file referenced by `GITHUB_STEP_SUMMARY`.
- Exit-code semantics (non-zero when the report file is missing).

Out of scope: running pytest itself, generating the JSON report, modifying check
status or PR comments, and any non-pytest test runners.

## System Overview

The action runs as a composite GitHub Action. `action.yml` declares one optional
input, `report-path`, and a single composite step that invokes
`python "${{ github.action_path }}/main.py" "${{ inputs.report-path }}"` under
`bash`.

`main.py` resolves the report path from `argv[1]` (falling back to `pytest.json`)
and the summary destination from the `GITHUB_STEP_SUMMARY` environment variable
(falling back to `/dev/null` for local runs). If the report file is absent it
writes an error line and exits `1`. Otherwise it loads the JSON, partitions
`report["tests"]` and `report["collectors"]` by `outcome == "failed"`, and
appends Markdown to the summary file: a single success line when there are no
failures, or a `### Failed Tests Summary` section and/or
`### Import or Collection Failures` section, each containing one collapsible
`<details>` block per failing item with the node id, `longrepr`, and captured
output rendered inside a fenced `text` block.

## Requirements Architecture

Requirements for this component are organized into the following classes:

- **Functional Requirements (FR)** — input resolution, JSON report parsing,
  failure selection, Markdown rendering of `<details>` blocks, success-path
  output, and exit-code behavior on a missing report.
- **Non-Functional Requirements (NFR)** — robustness against malformed or
  partial reports, deterministic output ordering, and portability across the
  Ubuntu GitHub-hosted runners that provide Python and bash.
- **Interface Requirements** — the `action.yml` input contract (`report-path`)
  and the `GITHUB_STEP_SUMMARY` output contract that callers consume.

Individual requirement artifacts are maintained alongside this master spec under
`spec/` as the component evolves.

## References

- README: `README.md` — usage, inputs, and example output for the action.
- Action definition: `action.yml` — composite action and `report-path` input.
- Summarizer source: `main.py` — report parsing and Markdown rendering logic.
- [`pytest-json-report`](https://github.com/pytest-dev/pytest-json-report) — the
  upstream plugin that produces the consumed JSON report format.
- [GitHub Actions job summaries](https://docs.github.com/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary)
  — the `GITHUB_STEP_SUMMARY` mechanism written to by this action.
