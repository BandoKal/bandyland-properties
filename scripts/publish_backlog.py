"""Publish prepared tasks through authenticated gh. Checkpoints make retries safe."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "planning/github-project.json").read_text())
path = ROOT / "planning/tasks.json"
tasks = json.loads(path.read_text())
repo, owner = config["repository"], config["owner"]
number, project_id = str(config["project_number"]), config["project_id"]

def gh(*args, payload=None):
    p = subprocess.run(["gh", *args], input=json.dumps(payload) if payload is not None else None,
        text=True, capture_output=True, check=True)
    return json.loads(p.stdout) if p.stdout.strip() else None

def api(endpoint, payload=None, method=None):
    args = ["api", endpoint]
    if method:
        args += ["--method", method]
    if payload is not None:
        args += ["--input", "-"]
    result = gh(*args, payload=payload)
    if isinstance(result, dict) and result.get("errors"):
        raise RuntimeError(result["errors"])
    return result

def checkpoint():
    path.write_text(json.dumps(tasks, indent=2) + "\n")

def body(t):
    target = t["target_date"] or "Not scheduled until trigger is recorded"
    start = t["start_date"] or "Event dependent"
    deps = [next(x for x in tasks if x["key"] == key) for key in t["dependencies"]]
    dependencies = ", ".join(f'[{d["key"]}]({d["issue_url"]})' if d.get("issue_url") else d["key"] for d in deps) or "None"
    lines = [f'## {t["key"]} execution task', "", f'**Workstream:** {t["workstream"]}',
        f'**Priority:** {t["priority"]}', f'**Start date:** {start}', f'**Target date:** {target}',
        f'**Date basis:** {t["date_basis"]}', f'**Depends on:** {dependencies}', "",
        "Dates are proposed planning targets anchored to October 22, 2026. They are not contractual deadlines or proof of completion."]
    if t.get("event"):
        lines += ["", f'**Trigger:** {t["event"]}. Rebase from the actual event; do not mark overdue before the event exists.']
    lines += ["", "## Completion checklist", ""] + [f"- [ ] {s}" for s in t["checklist"]]
    lines += ["", "## Evidence and source", "", t["source"], "",
        "Attach or reference completion evidence in the approved private records location. Close only when the checklist is complete or record why the task is no longer needed.", "",
        "Source documents inform the task; they do not authorize spending, signing, contacting third parties, or making tenant decisions. Keep bank identifiers and applicant screening records out of GitHub.", "",
        f'<!-- bandyland-task:{t["key"]} -->']
    return "\n".join(lines)

assert gh("repo", "view", repo, "--json", "isPrivate")["isPrivate"]
gh("project", "edit", number, "--owner", owner, "--visibility", "PRIVATE", "--format", "json",
    "--description", "Dated execution plan for rental conversion, funding, BandyWorks Phase 0 and property equipment.",
    "--readme", "# BandyLand Properties Execution\n\nStart with the funding reconciliation and release/insurance work. Dates are proposed from October 22, 2026. The listing target is November 6, subject to prerequisites.\n\nUse Start date and Target date for scheduling, Priority for selection, and Depends on for blockers. Event-dependent tasks must be rebased from actual listing, fallback, and lease dates. No tenant or property work has been marked complete from source assumptions.\n\nThe plan and workbook disagree on reserves and startup funding; resolve F01 before committing funds. Original documents remain local.\n\nA daily 8:00 a.m. America/Chicago task will read live issues and produce a short prioritized list. Close issues with evidence; edits to dates and checklists should be made in GitHub.")
gh("project", "link", number, "--owner", owner, "--repo", repo)
fields = gh("project", "field-list", number, "--owner", owner, "--format", "json")["fields"]
field_specs = [("Start date", "DATE", None), ("Target date", "DATE", None),
    ("Workstream", "SINGLE_SELECT", "Funding,Rental,Operations,BandyWorks,Property Equipment"),
    ("Priority", "SINGLE_SELECT", "P0,P1,P2"), ("Date basis", "TEXT", None),
    ("Depends on", "TEXT", None), ("Trigger", "TEXT", None)]
for name, kind, options in field_specs:
    if not any(f["name"] == name for f in fields):
        args = ["project", "field-create", number, "--owner", owner, "--name", name,
            "--data-type", kind, "--format", "json"]
        if options:
            args += ["--single-select-options", options]
        gh(*args)
fields = {f["name"]: f for f in gh("project", "field-list", number, "--owner", owner, "--format", "json")["fields"]}
config["fields"] = fields
(ROOT / "planning/github-project.json").write_text(json.dumps(config, indent=2) + "\n")

labels = {"Funding":"0E8A16", "Rental":"1D76DB", "Operations":"5319E7", "BandyWorks":"D876E3",
    "Property Equipment":"006B75", "P0":"B60205", "P1":"FBCA04", "P2":"C2E0C6", "event-dependent":"BFD4F2"}
existing_labels = {l["name"] for l in api(f"repos/{repo}/labels?per_page=100")}
for name, color in labels.items():
    if name not in existing_labels:
        api(f"repos/{repo}/labels", dict(name=name, color=color))

existing = api(f"repos/{repo}/issues?state=all&per_page=100")
for i, t in enumerate(tasks):
    if not t.get("issue_number"):
        issue = next((x for x in existing if f'<!-- bandyland-task:{t["key"]} -->' in (x.get("body") or "")), None)
        if issue is None:
            ls = [t["workstream"], t["priority"]]
            if t.get("event"):
                ls += ["event-dependent"]
            issue = api(f"repos/{repo}/issues", dict(title=f'[{t["key"]}] {t["title"]}', body=body(t), labels=ls, assignees=[owner]))
        t.update(issue_number=issue["number"], issue_url=issue["html_url"], issue_node_id=issue["node_id"])
        checkpoint()
    print(f'Issue {i+1}/{len(tasks)}: {t["key"]} #{t["issue_number"]}', flush=True)

for i, t in enumerate(tasks):
    if not t.get("project_item_id"):
        result = api("graphql", dict(query="mutation($p:ID!,$i:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$i}){item{id}}}",
            variables=dict(p=project_id, i=t["issue_node_id"])))
        t["project_item_id"] = result["data"]["addProjectV2ItemById"]["item"]["id"]
        checkpoint()
    if not t.get("fields_published"):
        vals = {"Workstream": t["workstream"], "Priority": t["priority"], "Status": "Todo",
            "Date basis": t["date_basis"], "Depends on": ", ".join(f'#{next(x for x in tasks if x["key"]==d)["issue_number"]} ({d})' for d in t["dependencies"]) or "None",
            "Trigger": t.get("event") or "Start date and prerequisites"}
        if t["start_date"]: vals["Start date"] = t["start_date"]
        if t["target_date"]: vals["Target date"] = t["target_date"]
        mutations = []
        for j, (name, value) in enumerate(vals.items()):
            field = fields[name]
            if field.get("options"):
                option = next(o["id"] for o in field["options"] if o["name"] == value)
                literal = "{singleSelectOptionId:" + json.dumps(option) + "}"
            else:
                kind = "date" if name in ("Start date", "Target date") else "text"
                literal = "{" + kind + ":" + json.dumps(value) + "}"
            mutations.append(f'v{j}:updateProjectV2ItemFieldValue(input:{{projectId:{json.dumps(project_id)},itemId:{json.dumps(t["project_item_id"])},fieldId:{json.dumps(field["id"])},value:{literal}}}){{projectV2Item{{id}}}}')
        api("graphql", dict(query="mutation{" + " ".join(mutations) + "}"))
        api(f'repos/{repo}/issues/{t["issue_number"]}', dict(body=body(t)), method="PATCH")
        t["fields_published"] = True
        checkpoint()
    print(f'Project item {i+1}/{len(tasks)}: {t["key"]}', flush=True)
config = json.loads((ROOT / "planning/github-project.json").read_text())
config["publication_status"] = "issues_and_fields_published"
(ROOT / "planning/github-project.json").write_text(json.dumps(config, indent=2) + "\n")
print(config["project_url"], flush=True)
