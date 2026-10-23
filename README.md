# BandyLand Properties

Private execution workspace for the Goslin Branch rental conversion, shared funding, BandyWorks Phase 0, and property equipment.

The active project is the user-created **BandyLand project 7**, which returns all 43 issues. It replaces the original project 5, whose visibility problem is recorded in the [historical diagnostic report](planning/project-visibility.md).

- [Project board](https://github.com/users/BandoKal/projects/7/views/2)
- [Backlog](https://github.com/users/BandoKal/projects/7/views/1)
- [Roadmap](https://github.com/users/BandoKal/projects/7/views/4)
- [Workspace context](CONTEXT.md)
- [Task schedule and issue links](TASKS.md)
- [Daily to-do snapshot](DAILY_TODO.md)

The initial backlog contains 43 issues with checklists, sources, dates, priorities, and dependencies. No property work was marked complete merely because it appeared in a plan. October 22, 2026 is the proposed start, and November 6 is a conditional listing target. Update actual dates and status as work progresses.

## Start here

1. [Reconcile the rental funding and reserve policy](https://github.com/BandoKal/bandyland-properties/issues/1).
2. [Confirm actual proceeds and emergency funding](https://github.com/BandoKal/bandyland-properties/issues/2).
3. [Obtain the signed sale-listing release](https://github.com/BandoKal/bandyland-properties/issues/3).

The owner confirmed a $9,000 initial reserve, growing toward $18,000 through retained owner draw. The retention percentage and startup budget remain pending. The workbook must separate initial funding from the target and reconcile its treatment of the $2,000 preparation allowance. See the [funding decision record](planning/funding-policy.md).

## Daily routine

A Codex daily task is scheduled for 8:00 a.m. America/Chicago in the originating task. It reads live GitHub issues and project dates, selects three next actions, and highlights due work, blockers, and the next seven days. It refreshes the local `DAILY_TODO.md`; the copy in GitHub is a dated snapshot and does not automatically update through git.

The generator reads GitHub through an authenticated `gh` CLI with repository and project access. Run `scripts/daily_todo.py` with Python 3.9+ to refresh locally. If the live read fails, it does not overwrite the previous snapshot or claim stale information is current. The Codex task can alternatively use connected GitHub tools.

Update checklist progress in issue bodies and dates in project fields. Close issues when their evidence is complete. The daily list uses issue state as authoritative and flags disagreements with the project Status field. Record actual listing, fallback, and lease dates in `planning/github-project.json` and rebase the dependent project dates. Keep recurring reviews open with their next occurrence, or create a successor issue before closing the previous one.

## Source files

Unmodified copies of the supplied Word plan and Excel budget are retained locally in `sources/` and excluded from git. `CONTEXT.md` identifies sections and cell references. Its source-file links resolve in the local workspace. The two earlier shared conversations were not read and are not used as evidence.

## Maintenance

`planning/tasks.json` is the initial publication manifest, not a substitute for live status. `planning/github-project.json` stores destination IDs and actual event anchors. The publication script checkpoints created issue/item IDs to avoid duplicate creation on recovery; do not rerun it to overwrite later user edits. The source preparation script refuses to overwrite an existing manifest.
