import json
import sys
import os
from pathlib import Path

report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("pytest.json")
summary_path = Path(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null"))

if not report_path.exists():
    summary_path.write_text(f"❌ Report file not found at {report_path}\n", encoding="utf-8")
    sys.exit(1)

with report_path.open() as f:
    report = json.load(f)

failed_tests = [t for t in report.get("tests", []) if t.get("outcome") == "failed"]

with summary_path.open("a", encoding="utf-8") as out:
    if not failed_tests:
        out.write("✅ All tests passed!\n")
    else:
        out.write("### ❌ Failed Tests Summary\n\n")
        for test in failed_tests:
            nodeid = test.get("nodeid", "unknown")
            longrepr = test.get("longrepr", "").strip()
            captured = test.get("captured", "").strip()

            out.write(f"<details>\n<summary><code>{nodeid}</code></summary>\n\n")
            out.write("```text\n")
            out.write(f"{longrepr}\n\n{captured}\n")
            out.write("```\n</details>\n\n")
