#!/usr/bin/env python3
"""Quality Gate keamanan berbasis hasil Bandit (format JSON).

Aturan (dapat diubah lewat argumen):
  - HIGH   severity            : maksimal 0   (wajib nol)
  - MEDIUM severity            : maksimal 0   (wajib nol)
  - LOW    severity            : maksimal 5   (ditoleransi sampai batas)

Exit code 0 = lulus, 1 = gagal (workflow GitHub Actions ikut gagal).
"""
import argparse
import json
import sys


def evaluate(report, max_high=0, max_medium=0, max_low=5):
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in report.get("results", []):
        sev = issue.get("issue_severity", "").upper()
        if sev in counts:
            counts[sev] += 1
    limits = {"HIGH": max_high, "MEDIUM": max_medium, "LOW": max_low}
    violations = [
        f"{sev}: {counts[sev]} temuan (batas {limits[sev]})"
        for sev in counts
        if counts[sev] > limits[sev]
    ]
    return counts, violations


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="path ke bandit-report.json")
    parser.add_argument("--max-high", type=int, default=0)
    parser.add_argument("--max-medium", type=int, default=0)
    parser.add_argument("--max-low", type=int, default=5)
    args = parser.parse_args(argv)

    with open(args.report, encoding="utf-8") as fh:
        report = json.load(fh)

    counts, violations = evaluate(
        report, args.max_high, args.max_medium, args.max_low
    )
    print("=== SECURITY QUALITY GATE ===")
    print(f"HIGH={counts['HIGH']}  MEDIUM={counts['MEDIUM']}  LOW={counts['LOW']}")
    for issue in report.get("results", []):
        print(
            f"- [{issue['issue_severity']}] {issue['test_id']} "
            f"{issue['filename']}:{issue['line_number']} - {issue['issue_text']}"
        )
    if violations:
        print("\nQUALITY GATE: FAILED")
        for v in violations:
            print(f"  * {v}")
        return 1
    print("\nQUALITY GATE: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
