---
name: workflow-rules
---

# Workflow Rules and Scoring Protocol (v2)

## Status Transitions

```
pending
  → brainstorm (Scheduler decides creative work)
  → plan (Scheduler decides simple task)
  → debug (Scheduler decides bug fix)

brainstorm
  → brainstorm_review (Brainstormer writes design.md)

brainstorm_review
  → plan (Spec-Reviewer PASS)
  → brainstorm (Spec-Reviewer FAIL, <3 tries)
  → plan (force-pass, annotated risk, 3rd try)

plan
  → plan_review (Planner writes plan.md)

plan_review
  → dev (Spec-Reviewer PASS)
  → plan (Spec-Reviewer FAIL, <3 tries)
  → dev (force-pass, annotated risk, 3rd try)

dev
  → dev_review (Developer implements)

dev_review
  → done (Dual-Reviewer PROCEED)
  → debug (bug found)
  → dev (Dual-Reviewer FIX-CRITICAL/FIX-ALL, <3 tries)
  → done (force-pass, annotated risk, 3rd try)

done
  → closed (Finishing Branch executed)
```

## Spec-Reviewer Verdict Rules

| Dimension | Weight | Verdict |
|-----------|--------|---------|
| Completeness | Equal | PASS/FAIL |
| Accuracy | Equal | PASS/FAIL |
| Executability | Equal | PASS/FAIL |
| Simplicity | Equal | PASS/FAIL |

- ALL PASS → overall PASS
- ANY FAIL → overall FAIL
- 3rd rejection → force-pass, annotate risk

## Quality-Reviewer Verdict Rules

| Severity | Action | Block? |
|----------|--------|--------|
| Critical | Must fix | Yes |
| Important | Should fix | Judgment (>3 = block) |
| Minor | Note for later | No |

- No Critical + ≤3 Important → PROCEED
- Has Critical → FIX-CRITICAL
- Many Important → FIX-ALL

## Dual-Reviewer Combined Rules

```
Spec-Reviewer    Quality-Reviewer    Action
─────────────────────────────────────────────────
PASS             PROCEED            → done
PASS             FIX-CRITICAL       → dev (fix Critical)
PASS             FIX-ALL            → dev (fix Important too)
FAIL             any                → dev (fix spec gaps first)
```

## Systematic Debugging Triggers

- Dual-Reviewer finds bug during dev_review
- Tests fail during implementation
- User reports unexpected behavior mid-flow

## Finishing Branch Triggers

- Status reaches `done`
- Tests must pass before presenting options
- Exactly 4 options presented (merge/PR/keep/discard)

## Handoff File Locations

| Role | Output File |
|------|-------------|
| Scheduler | `handoff/scheduler.md` |
| Brainstormer | `handoff/brainstormer.md` + `tasks/<uuid>/design.md` |
| Spec-Reviewer (design) | `handoff/spec-reviewer.md` |
| Planner | `handoff/planner.md` + `tasks/<uuid>/plan.md` |
| Spec-Reviewer (plan) | `handoff/plan-reviewer.md` |
| Developer | `handoff/developer.md` |
| Dual-Reviewer | `handoff/dual-reviewer.md` |
| Systematic Debugger | `handoff/debug.md` |
| Finishing Branch | `handoff/finish.md` |

## Force-Pass Policy

After 3 rejections in any phase:
- Force-pass regardless of score/verdict
- Annotate risk in reviewer output
- Note: "3rd review — force-passed due to iteration limit"
- Log to `handoff/force-pass-risks.md` for post-mortem

## Do NOT

- Skip brainstorm for creative work (hard gate)
- Skip tests before finishing branch
- Bundle unrelated refactoring in any phase
- Use placeholders ("TBD", "TODO", "similar to Task N")
- Present open-ended questions at finishing branch
- Delete work without typed confirmation
