# 🧪 Pytest Summary GitHub Action

[![Discord](https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white)](https://discord.gg/k8DVhuYBR2)

This GitHub Action generates a detailed, collapsible summary of **failed tests** from a [`pytest-json-report`](https://github.com/pytest-dev/pytest-json-report) output file.

✅ Shows test results directly in the GitHub Actions summary
📦 Built for reuse in monorepos, shared workflows, and CI pipelines

---

## 📥 Inputs

| Name         | Description                       | Required | Default        |
|--------------|-----------------------------------|----------|----------------|
| `report-path` | Path to `pytest.json` file         | No       | `pytest.json`  |

---

## 📤 Output

- If all tests pass:
  `✅ All tests passed!`

- If there are failures:
  Outputs a collapsible `<details>` section per failed test showing:
  - Test ID
  - Failure traceback (`longrepr`)
  - Captured output (stdout/stderr)

Example:

<details>
<summary><code>tests/test_foo.py::test_bar</code></summary>

```text
Traceback (most recent call last):
  ...
AssertionError: expected 1 == 2

Captured output:
Running test...
```
<details>


🚀 Usage

```yaml
jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Pytest
        run: |
          pip install pytest pytest-json-report
          pytest --json-report --json-report-file=pytest.json

      - name: Summarize pytest failures
        uses: agent-ix/pytest-summary@v1
        with:
          report-path: pytest.json

```
