#!/usr/bin/env python3
"""Create a new multi-agent task directory with UUID isolation."""

import uuid
import sys
import os
from datetime import datetime, timezone


def create_task(title: str, description: str = "") -> str:
    task_id = str(uuid.uuid4())
    task_dir = os.path.join("tasks", task_id)
    handoff_dir = os.path.join(task_dir, "handoff")
    os.makedirs(handoff_dir, exist_ok=True)

    task_md = f"""# Task

## 基本信息
- **创建时间**: {datetime.now(timezone.utc).isoformat()}
- **创建者**: user
- **优先级**: medium

## 用户原始需求
{title}
{description}

## 已知约束
- <待 Scheduler 补充>

## 验收标准（由 Product Agent 后续补充）
- [ ] <待填充>
"""

    with open(os.path.join(task_dir, "task.md"), "w", encoding="utf-8") as f:
        f.write(task_md)

    with open(os.path.join(task_dir, "status"), "w", encoding="utf-8") as f:
        f.write("pending")

    return task_id


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "未命名任务"
    desc = sys.argv[2] if len(sys.argv) > 2 else ""
    task_id = create_task(title, desc)
    print(task_id)
