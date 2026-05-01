# 工作流规则

## 状态机

```
pending → product → product_review → dev → dev_review → done
             ↑            ↓             ↑          ↓
             └─────(<90)─┘             └───(<90)──┘
```

| 状态 | 含义 | 活跃角色 |
|------|------|----------|
| `pending` | 刚创建，等待调度者分析 | scheduler |
| `product` | 等待/正在进行需求分析 | product |
| `product_review` | 等待/正在评审产品产出 | reviewer |
| `dev` | 等待/正在进行开发 | developer |
| `dev_review` | 等待/正在评审开发产出 | reviewer |
| `done` | 已完成，归档 | — |

## 评分规则（Reviewer 核心）

- **评分维度**：完整性(30) + 准确性(30) + 可执行性(20) + 简洁性(20) = **100 分**
- **通过阈值**：**≥ 90 分** 可进入下一阶段
- **驳回上限**：同一阶段最多驳回 **2 次**，第 3 次强制通过并由 reviewer 在 handoff 中标注风险
- **评分记录**：每次评分必须写入 `handoff/reviewer.md`，包含分数、维度拆解、通过/驳回结论

## Handoff 协议

1. **只写自己的文件**：各角色只写 `handoff/<role>.md`。
2. **状态原子更新**：角色完成产出后，将 `status` 更新为下一个阶段（product → product_review，dev → dev_review）。
3. **Reviewer 拥有状态最终决定权**：reviewer 完成评分后，根据分数更新 `status`：
   - ≥ 90：`product_review → dev` 或 `dev_review → done`
   - < 90：`product_review → product` 或 `dev_review → dev`
4. **追加而非覆盖**：handoff 文件按时间顺序追加记录，保留完整评分历史。

## Handoff 记录格式

```markdown
## [<timestamp>] <action>

### 输入
- 来源：<role>
- 内容摘要：<一句话>

### 思考
<推理过程>

### 决策/产出
- <具体产出或评分>

### 下一步
- 状态：<status>
```

## 安全约束

- 每个任务独立目录，UUID 隔离。
- 禁止跨任务读取 `tasks/<other-uuid>/`。
- 禁止在 `task.md` 中追加内容（它是只读源头）。
