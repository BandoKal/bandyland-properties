import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = root / "planning/github-project.json"
c = json.loads(p.read_text())

def api(endpoint, payload):
    r = subprocess.run(["gh", "api", endpoint, "-H", "X-GitHub-Api-Version: 2026-03-10", "--input", "-"], input=json.dumps(payload),
        text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    result = json.loads(r.stdout)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result

q = '{user(login:' + json.dumps(c['owner']) + '){databaseId projectV2(number:' + str(c['project_number']) + '){fields(first:50){nodes{... on ProjectV2Field{name databaseId} ... on ProjectV2SingleSelectField{name databaseId}}} views(first:30){nodes{id name number}}}}}'
u = api("graphql", {"query":q})["data"]["user"]
fields = {f["name"]: f["databaseId"] for f in u["projectV2"]["fields"]["nodes"]}
visible = [fields[n] for n in ["Title", "Status", "Assignees", "Workstream", "Priority", "Start date", "Target date", "Depends on", "Date basis", "Trigger"]]
specs = [
    dict(name="By target date", layout="table", filter="is:open", visible_fields=visible, sort_by=[[fields["Target date"], "asc"], [fields["Priority"], "asc"]]),
    dict(name="By workstream", layout="board", filter="is:open", visible_fields=visible[:7], sort_by=[[fields["Target date"], "asc"]], vertical_group_by=[fields["Workstream"]]),
    dict(name="Awaiting events", layout="table", filter='is:open label:event-dependent', visible_fields=visible, sort_by=[[fields["Target date"], "asc"]]),
]
views = {v["name"]:v for v in u["projectV2"]["views"]["nodes"]}
c["views"] = []
for spec in specs:
    if spec["name"] in views:
        n = views[spec["name"]]["number"]
        c["views"].append({"name":spec["name"], "url":f'{c["project_url"]}/views/{n}'})
        continue
    result = api(f'users/{c["owner"]}/projectsV2/{c["project_number"]}/views', spec)
    v = result.get("value", result)
    c["views"].append({"name":v["name"], "url":v["html_url"], "sort_by":v.get("sort_by")})
    print(v["name"], v["html_url"], v.get("sort_by"), flush=True)
    p.write_text(json.dumps(c, indent=2) + "\n")
p.write_text(json.dumps(c, indent=2) + "\n")
