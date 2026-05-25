#!/bin/bash
# SessionStart hook: 檢查 HANDOFF.md Section 1 是否落後 git，落後就提醒跑 /handoff
# 邏輯：讀 Section 1 的 <!-- SECTION_1_UPDATED_AT: YYYY-MM-DD --> 註解，
#       比對自該日起的 commit 數，>= 3 就提醒。
# 絕不改文件，只輸出提醒到 stderr。

PROJECT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -z "$PROJECT_DIR" ] && exit 0

HANDOFF="$PROJECT_DIR/.ai-context/HANDOFF.md"
[ -f "$HANDOFF" ] || exit 0

# 抓出 SECTION_1_UPDATED_AT 日期
LAST_DATE=$(grep -oE 'SECTION_1_UPDATED_AT: [0-9]{4}-[0-9]{2}-[0-9]{2}' "$HANDOFF" | head -1 | awk '{print $2}')
[ -z "$LAST_DATE" ] && exit 0

# 數該日期後的 commit 數（不含當天，用 --since 是 inclusive 到當天 00:00）
COMMIT_COUNT=$(cd "$PROJECT_DIR" && git log --since="$LAST_DATE 00:00:00" --oneline 2>/dev/null | wc -l | tr -d ' ')

THRESHOLD=3
if [ "$COMMIT_COUNT" -ge "$THRESHOLD" ]; then
    cat >&2 <<EOF
[handoff-reminder] HANDOFF Section 1 自 $LAST_DATE 起已落後 $COMMIT_COUNT 個 commit。
                   建議跑 /handoff 更新「當前焦點」。
EOF
fi

exit 0