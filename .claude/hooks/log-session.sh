#!/bin/bash
# Stop hook: append to CHANGELOG.md + auto-update HANDOFF.md via claude -p

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CHANGELOG="$PROJECT_DIR/.ai-context/CHANGELOG.md"
HANDOFF="$PROJECT_DIR/.ai-context/HANDOFF.md"

[ -f "$CHANGELOG" ] || exit 0

cd "$PROJECT_DIR" || exit 0

TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"
TODAY="$(date '+%Y-%m-%d')"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'no-git')"
LAST_COMMIT="$(git log -1 --pretty=format:'%h %s' 2>/dev/null | head -c 80 || echo 'no-commit')"
COMMIT_HASH="${LAST_COMMIT%% *}"
CHANGED="$(git status --short 2>/dev/null | grep -v '\.ai-context/' | wc -l | tr -d ' ')"
CHANGED_FILES="$(git status --short 2>/dev/null | grep -v '\.ai-context/' | awk '{print $2}' | head -5 | tr '\n' ' ')"

# ── CHANGELOG dedup ──────────────────────────────────────────────────────────
# Stop hook fires on every AI response; skip if same commit+dirty state as last entry
LAST_WRITTEN_LINE="$(grep '| branch=' "$CHANGELOG" 2>/dev/null | tail -1 || true)"
if echo "$LAST_WRITTEN_LINE" | grep -qF "$COMMIT_HASH" \
   && echo "$LAST_WRITTEN_LINE" | grep -qF "dirty=${CHANGED} files"; then
    exit 0
fi

if ! grep -q "^## $TODAY" "$CHANGELOG" 2>/dev/null; then
    printf "\n## %s\n\n" "$TODAY" >> "$CHANGELOG"
fi

printf -- "- \`%s\` | branch=\`%s\` | dirty=%s files | head=\`%s\`\n" \
    "$TIMESTAMP" "$BRANCH" "$CHANGED" "$LAST_COMMIT" >> "$CHANGELOG"

if [ "$CHANGED" -gt 0 ] && [ -n "$CHANGED_FILES" ]; then
    printf "  - touched: %s\n" "$CHANGED_FILES" >> "$CHANGELOG"
fi

# ── HANDOFF.md auto-update via claude -p ────────────────────────────────────
[ -f "$HANDOFF" ] || exit 0

CLAUDE_BIN="${HOME}/.local/bin/claude"
[ -x "$CLAUDE_BIN" ] || CLAUDE_BIN="$(command -v claude 2>/dev/null || true)"
[ -n "$CLAUDE_BIN" ] || { echo "[log-session] claude not found, skipping HANDOFF update"; exit 0; }

DIFF_STAT="$(git diff --stat HEAD 2>/dev/null | tail -20)"
RECENT_LOG="$(git log -5 --oneline 2>/dev/null)"
CURRENT_HANDOFF="$(cat "$HANDOFF")"

PROMPT="你是 LLManim_Agent 專案的 session 記錄員。根據以下 git 資訊，更新 HANDOFF.md 的兩個部分。

只輸出 JSON，不要 markdown code block，不要其他文字：
{
  \"tasks\": \"<更新後的 '現在要做什麼' checklist，保留未完成的 - [ ]，把這次 commit 看起來已完成的改成 - [x]，加入新發現的 blocker，用 - [ ] 開頭，每條一行>\",
  \"last_session\": \"<更新後的 '上次 Session 改了什麼' markdown 表格，根據這次 git diff --stat 更新，保持原本的表格格式>\"
}

規則：
- tasks 最多 6 條，移除明顯已過時的
- last_session 只描述這次 session 的變動，不要堆疊舊的
- 日期用 ${TODAY}

---
Branch: ${BRANCH}
HEAD: ${LAST_COMMIT}
Dirty files (${CHANGED}): ${CHANGED_FILES}

git diff --stat:
${DIFF_STAT}

Recent commits:
${RECENT_LOG}

目前 HANDOFF.md：
${CURRENT_HANDOFF}"

RESPONSE="$("$CLAUDE_BIN" -p "$PROMPT" \
    --output-format json \
    --model claude-haiku-4-5-20251001 \
    --max-turns 1 \
    --disable-slash-commands \
    --strict-mcp-config \
    2>/dev/null)" || true

python3 - "$HANDOFF" "$TODAY" "$BRANCH" "$LAST_COMMIT" "$RESPONSE" <<'PYEOF'
import sys, re, json

handoff_path = sys.argv[1]
today = sys.argv[2]
branch = sys.argv[3]
last_commit = sys.argv[4]
raw_response = sys.argv[5]

try:
    outer = json.loads(raw_response)
    # claude --output-format json wraps in {"type":"result","result":"..."}
    llm_text = outer.get("result", outer.get("content", ""))
    if isinstance(llm_text, list):
        llm_text = llm_text[0].get("text", "")
    llm_text = llm_text.strip()
    llm_text = re.sub(r'^```json\s*', '', llm_text)
    llm_text = re.sub(r'\s*```$', '', llm_text)
    data = json.loads(llm_text)
except Exception:
    sys.exit(0)

tasks = data.get("tasks", "").strip()
last_session = data.get("last_session", "").strip()

if not tasks and not last_session:
    sys.exit(0)

with open(handoff_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update header metadata
content = re.sub(r'\*\*更新時間\*\*：.*', f'**更新時間**：{today}', content)
content = re.sub(r'\*\*Branch\*\*：.*', f'**Branch**：{branch}', content)

lines = content.split('\n')

def replace_section(lines, header_pattern, new_body):
    """Replace content between a ## header and the next ## header."""
    new_lines = []
    in_section = False
    replaced = False
    for line in lines:
        if re.match(header_pattern, line):
            in_section = True
            replaced = True
            new_lines.append(line)
            new_lines.append('')
            for bl in new_body.split('\n'):
                new_lines.append(bl)
            continue
        if in_section:
            if re.match(r'^## ', line):
                in_section = False
                new_lines.append('')
                new_lines.append(line)
            continue
        new_lines.append(line)
    return new_lines if replaced else lines

if tasks:
    lines = replace_section(lines, r'^## 現在要做什麼', tasks)

if last_session:
    lines = replace_section(lines, r'^## 上次 Session 改了什麼', last_session)

with open(handoff_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"[log-session] HANDOFF.md updated ({today})")
PYEOF

exit 0
