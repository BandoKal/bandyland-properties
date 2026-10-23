"""Render the published issue index without changing task definitions."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
tasks=json.loads((root/"planning/tasks.json").read_text())
c=json.loads((root/"planning/github-project.json").read_text())
rows=["# BandyLand Properties Task Schedule", "", "Prepared October 22, 2026 from the supplied business plan and budget. Dates are proposed; source completion status was not supplied. Use the live project for subsequent status and schedule changes.", "", f'[Active GitHub project]({c["project_url"]}/views/2)', "", "## Dated work", "", "| Target | Start | Task | Workstream | Priority | Depends on |", "| --- | --- | --- | --- | --- | --- |"]
bykey={t["key"]:t for t in tasks}
for t in tasks:
    if not t["target_date"]: continue
    deps=", ".join(f'[{k}]({bykey[k]["issue_url"]})' for k in t["dependencies"]) or "None"
    rows.append(f'| {t["target_date"]} | {t["start_date"]} | [{t["key"]}: {t["title"]}]({t["issue_url"]}) | {t["workstream"]} | {t["priority"]} | {deps} |')
rows += ["", "## Event-dependent and recurring work", "", "Listing review dates in the table are placeholders until the actual publication date is recorded. The following tasks have no artificial due date:", ""]
for t in tasks:
    if not t["target_date"]:
        rows += [f'- [{t["key"]}: {t["title"]}]({t["issue_url"]}) — {t["event"]}.']
rows += ["", "## Source and scheduling rules", "", "The plan contains a 30-day conversion sequence, but actual prerequisites govern launch and possession. The proposed November 6 listing yields November 13 and November 20 demand reviews. A fallback review occurs at least seven days after an actual price change. Neither a signed lease nor occupancy is assumed by day 30.", "", "BandyWorks and property-equipment dates are proposed sequencing of the workbook's purchase dependencies. No document supplies firm vendor delivery dates. Keep work blocked until required approvals, quotes, installation checks and funding exist.", "", "P0 means a funding, legal, insurance, safety or execution prerequisite; P1 means planned execution work; P2 means a purchase that can follow the critical prerequisites. Priority alone does not make a blocked task executable.", ""]
(root/"TASKS.md").write_text("\n".join(rows))
print(f'Rendered {len(tasks)} linked tasks')
