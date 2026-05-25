#!/usr/bin/env bash
# auto_commit.sh — Automated commit processor for TODOS.md
#
# Processes the next pending todo item from TODOS.md, stages changes,
# creates a conventional commit, and pushes.
#
# Usage:
#   ./scripts/auto_commit.sh [--dry-run] [--batch N] [--lang LANG] [--from N]
#
# Flags:
#   --dry-run   Show what would be committed without committing
#   --batch N   Process N items in sequence (default: 1)
#   --lang LANG Filter todos by language/phase label
#   --from N    Start from a specific todo number

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TODOS_FILE="$ROOT_DIR/TODOS.md"
LOG_FILE="$ROOT_DIR/auto_commit.log"

DRY_RUN=false
BATCH=1
LANG_FILTER=""
FROM_FILTER=""

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --batch) BATCH="$2"; shift 2 ;;
        --lang) LANG_FILTER="$2"; shift 2 ;;
        --from) FROM_FILTER="$2"; shift 2 ;;
        *) echo "Unknown flag: $1"; exit 1 ;;
    esac
done

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Find next pending todo
find_next_pending() {
    local line_num=0
    local skip_line="${FROM_FILTER:-0}"

    while IFS= read -r line; do
        line_num=$((line_num + 1))
        if [[ "$line_num" -le "$skip_line" ]]; then
            continue
        fi
        # Match: | 1234 | Phase Name | Description
        if [[ "$line" =~ ^\|[[:space:]]*[0-9]+[[:space:]]*\| ]]; then
            local todo_num
            todo_num=$(echo "$line" | sed -E 's/^\|[[:space:]]*([0-9]+).*/\1/')
            local phase_name
            phase_name=$(echo "$line" | awk -F'|' '{print $3}' | xargs)

            # Apply language filter if set
            if [[ -n "$LANG_FILTER" ]]; then
                if ! echo "$phase_name" | grep -qi "$LANG_FILTER"; then
                    continue
                fi
            fi

            echo "$todo_num|$phase_name|$line"
            return 0
        fi
    done < "$TODOS_FILE"

    return 1
}

commit_item() {
    local todo_num="$1"
    local phase_name="$2"
    local description="$3"

    log "Processing todo #$todo_num: [$phase_name] $description"

    # Generate conventional commit type and message
    local type="feat"
    if echo "$description" | grep -qi "fix\|bug\|correct\|error"; then
        type="fix"
    elif echo "$description" | grep -qi "test\|robot\|owasp"; then
        type="test"
    elif echo "$description" | grep -qi "doc\|readme\|comment"; then
        type="docs"
    elif echo "$description" | grep -qi "ci\|cd\|action\|workflow\|release"; then
        type="ci"
    elif echo "$description" | grep -qi "refactor\|clean\|restructure"; then
        type="refactor"
    elif echo "$description" | grep -qi "config\|setup\|init\|install"; then
        type="chore"
    elif echo "$description" | grep -qi "perf\|benchmark\|optimize\|speed"; then
        type="perf"
    fi

    local commit_msg="${type}: #${todo_num} - ${description}"

    # Stage all changes
    if [[ -z "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
        log "No changes to stage for todo #$todo_num"
        return 0
    fi

    git -C "$ROOT_DIR" add -A

    if $DRY_RUN; then
        log "[DRY-RUN] Would commit: $commit_msg"
        log "[DRY-RUN] Changes:"
        git -C "$ROOT_DIR" diff --cached --stat
        return 0
    fi

    # Commit
    if git -C "$ROOT_DIR" commit -m "$commit_msg"; then
        log "Committed: $commit_msg"
        if git -C "$ROOT_DIR" push; then
            log "Pushed successfully"
        else
            log "WARNING: Push failed (will retry on next run)"
        fi
    else
        log "ERROR: Commit failed"
        return 1
    fi
}

# Main loop
processed=0
for ((i=0; i<BATCH; i++)); do
    next=$(find_next_pending)
    if [[ -z "$next" ]]; then
        log "No more pending todos found"
        break
    fi

    IFS='|' read -r num phase desc <<< "$next"

    if $DRY_RUN; then
        commit_item "$num" "$phase" "$desc"
    else
        commit_item "$num" "$phase" "$desc" || {
            log "Failed to process todo #$num, skipping"
            continue
        }
    fi

    processed=$((processed + 1))
done

log "Processed $processed todos"
echo "Done: $processed commits processed"
