#!/usr/bin/env bash
set -euo pipefail

REPORT_DIR="reports/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

echo "=== Generating Test Reports ==="

# pytest coverage
if [ -f .coverage ]; then
    coverage html -d "$REPORT_DIR/coverage_html" 2>&1 | tail -1
    echo "Coverage report: $REPORT_DIR/coverage_html"
fi

# Robot Framework results
if [ -d robot_output ]; then
    cp -r robot_output "$REPORT_DIR/robot_output"
    echo "Robot results: $REPORT_DIR/robot_output"
fi

# Bandit scan
if [ -f bandit_report.json ]; then
    cp bandit_report.json "$REPORT_DIR/bandit_report.json"
fi

# Summary
{
    echo "Report generated: $(date)"
    echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo 'N/A')"
    echo "Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A')"
} > "$REPORT_DIR/summary.txt"

echo "=== Report saved to $REPORT_DIR ==="
