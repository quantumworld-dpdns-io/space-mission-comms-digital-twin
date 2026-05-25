#!/usr/bin/env bash
set -euo pipefail

API_URL="${1:-http://localhost:8000}"
ZAP_PORT="${2:-8080}"
REPORT_DIR="reports/owasp/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

echo "=== OWASP ZAP Baseline Scan ==="
echo "Target: $API_URL"
echo "ZAP Port: $ZAP_PORT"

# Check if ZAP is running
if ! curl -s "http://localhost:${ZAP_PORT}" > /dev/null 2>&1; then
    echo "Starting ZAP container..."
    docker run -d --name zap \
        -p ${ZAP_PORT}:8080 \
        -v "${REPORT_DIR}:/zap/wrk" \
        ghcr.io/zaproxy/zaproxy:stable \
        zap.sh -daemon -port 8080 -host 0.0.0.0
    sleep 10
    CLEANUP=true
fi

# Run baseline scan
docker run --rm \
    -v "${REPORT_DIR}:/zap/wrk" \
    ghcr.io/zaproxy/zaproxy:stable \
    zap-baseline.py \
    -t "$API_URL" \
    -r zap_report.html \
    -w zap_report.md \
    -x zap_report.xml \
    -d || true

echo "=== OWASP Scan Complete ==="
echo "Reports: $REPORT_DIR"
echo "  HTML: $REPORT_DIR/zap_report.html"
echo "  Markdown: $REPORT_DIR/zap_report.md"

# Cleanup
if [ "${CLEANUP:-false}" = true ]; then
    docker stop zap 2>/dev/null || true
    docker rm zap 2>/dev/null || true
fi
