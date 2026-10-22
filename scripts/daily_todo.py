"""Read live project issues and write a dependency-aware daily Markdown list."""
import argparse
import calendar
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
QUERY = """query($owner:String!,$number:Int!,$cursor:String){user(login:$owner){projectV2(number:$number){
items(first:100,after:$cursor){pageInfo{hasNextPage endCursor} nodes{id isArchived
fieldValues(first:30){nodes{
... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}
... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}
}}
content{... on Issue{number title body url state repository{nameWithOwner}}}
}}}}}"""

def fetch(config):
    cursor, items = None, []
    while True:
        payload = dict(query=QUERY, variables=dict(owner=config["owner"], number=config["project_number"], cursor=cursor))
        r = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=json.dumps(payload),
            text=True, capture_output=True)
        if r.returncode:
            raise RuntimeError("Live GitHub read failed; existing daily file was not refreshed. " + r.stderr.strip())
        data = json.loads(r.stdout)
        if data.get("errors"):
            raise RuntimeError(data["errors"])
        page = data["data"]["user"]["projectV2"]["items"]
        items += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    # Project indexing can lag new memberships. Verify via repository issues too.
    fragment = """id isArchived project{id} fieldValues(first:30){nodes{
    ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}}
    ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}
    ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}
    }}"""
    query = "query($owner:String!,$repo:String!,$cursor:String){repository(owner:$owner,name:$repo){issues(first:100,after:$cursor){pageInfo{hasNextPage endCursor} nodes{number title body url state repository{nameWithOwner} projectItems(first:100){nodes{" + fragment + "}}}}}}"
    cursor = None
    merged = {i["id"]:i for i in items}
    repo_owner, repo_name = config["repository"].split("/")
    while True:
        r = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=json.dumps(dict(query=query, variables=dict(owner=repo_owner, repo=repo_name, cursor=cursor))), text=True, capture_output=True)
        if r.returncode:
            raise RuntimeError("Live issue-membership verification failed; daily file not refreshed. " + r.stderr)
        result = json.loads(r.stdout)
        if result.get("errors"):
            raise RuntimeError(result["errors"])
        page = result["data"]["repository"]["issues"]
        for issue in page["nodes"]:
            memberships = issue.pop("projectItems")["nodes"]
            for item in memberships:
                if item["project"]["id"] == config["project_id"]:
                    item["content"] = issue
                    merged[item["id"]] = item
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return list(merged.values())

def plus_months(date, n):
    m = date.month - 1 + n
    y, m = date.year + m // 12, m % 12 + 1
    return date.replace(year=y, month=m, day=min(date.day, calendar.monthrange(y,m)[1]))

def normalize(items, config):
    records = []
    for item in items:
        issue = item.get("content") or {}
        if not issue.get("number") or issue.get("repository", {}).get("nameWithOwner") != config["repository"]:
            continue
        fields = {}
        for value in item["fieldValues"]["nodes"]:
            if value.get("field"):
                fields[value["field"]["name"]] = value.get("date", value.get("text", value.get("name")))
        match = re.search(r"bandyland-task:([A-Z]\d+)", issue.get("body") or "")
        key = match.group(1) if match else str(issue["number"])
        deps = [int(n) for n in re.findall(r"#(\d+)", fields.get("Depends on", ""))]
        if not deps:
            dep_line = re.search(r"\*\*Depends on:\*\* (.*)", issue.get("body") or "")
            if dep_line:
                deps = [int(n) for n in re.findall(r"/issues/(\d+)", dep_line.group(1))]
        unchecked = re.findall(r"^- \[ \] (.+)$", issue.get("body") or "", re.M)
        records.append(dict(**issue, key=key, fields=fields, dependencies=deps,
            archived=item["isArchived"], next_action=unchecked[0] if unchecked else "Review completion evidence and update the issue.",
            start=fields.get("Start date"), due=fields.get("Target date"), event_wait=None))
    by_number = {r["number"]:r for r in records}
    for r in records:
        r["blockers"] = [n for n in r["dependencies"] if n not in by_number or by_number[n]["state"] != "CLOSED"]
        key = r["key"]
        listing = config.get("actual_listing_date")
        fallback = config.get("actual_fallback_date")
        lease = config.get("actual_lease_start")
        if key in ("R19", "R20", "R21", "R23") and not listing:
            r["event_wait"] = "Record actual listing date after publication"
        elif key in ("R20", "R21"):
            r["due"] = (dt.date.fromisoformat(listing) + dt.timedelta(days=7 if key == "R20" else 14)).isoformat()
            r["start"] = r["due"]
        if key == "R22":
            if not fallback:
                r["event_wait"] = "Only if rent changes to fallback; record actual change date"
            else:
                r["start"] = r["due"] = (dt.date.fromisoformat(fallback) + dt.timedelta(days=7)).isoformat()
        if key in ("O01", "O02", "O03", "O04"):
            if not lease:
                r["event_wait"] = "Record actual lease start and configure the next occurrence"
            elif not r["due"]:
                months = {"O01":1,"O02":3,"O03":6,"O04":12}[key]
                r["due"] = plus_months(dt.date.fromisoformat(lease), months).isoformat()
                r["start"] = r["due"]
        if key in ("R24", "R25") and not r["blockers"] and not r["due"]:
            r["event_wait"] = "Set the agreed lease/move-in date and verify readiness"
    return records

def render(records, config, today, now):
    opened = [r for r in records if r["state"] == "OPEN" and not r["archived"]]
    order = lambda r: (r["due"] or "9999", r["fields"].get("Priority", "P2"), r["number"])
    ready = sorted([r for r in opened if not r["blockers"] and not r["event_wait"] and (not r["start"] or r["start"] <= today)], key=order)
    due = sorted([r for r in opened if r["due"] and r["due"] <= today and not r["event_wait"]], key=order)
    waiting = sorted([r for r in opened if (r["blockers"] or r["event_wait"]) and (not r["start"] or r["start"] <= today)], key=order)
    week = (dt.date.fromisoformat(today)+dt.timedelta(days=7)).isoformat()
    upcoming = sorted([r for r in opened if r["due"] and today < r["due"] <= week and not r["event_wait"]], key=order)
    lines = [f"# Daily To Do for {today}", "", f'Live GitHub snapshot: {now}. Time zone: {config["timezone"]}.', "",
        f'[Project]({config["project_url"]}) · [All issues]({config["repository_url"]}/issues)', "",
        f'{len(opened)} open project issues. Dates are proposed unless confirmed in the issue; blocked tasks are not treated as executable.', "", "## Focus today", ""]
    for r in ready[:3]:
        lines += [f'- [ ] [{r["title"]}]({r["url"]}) — target {r["due"] or "unscheduled"}.', f'  Next step: {r["next_action"]}']
    if not ready:
        lines += ["No unblocked scheduled work is ready. Review the blockers and event triggers below."]
    if len(ready)>3:
        lines += ["", f"{len(ready)-3} additional unblocked tasks are available in the project; keep today's focus manageable."]
    lines += ["", "## Due or overdue", ""]
    for r in due:
        suffix = f'Blocked by {", ".join("#"+str(n) for n in r["blockers"])}' if r["blockers"] else "Ready"
        lines += [f'- [{r["title"]}]({r["url"]}) — {r["due"]}; {suffix}.']
    if not due: lines += ["None as of this live read."]
    lines += ["", "## Blockers and event dates", ""]
    for r in waiting[:8]:
        reason = r["event_wait"] or "Waiting for " + ", ".join(f'[{"#"+str(n)}]({config["repository_url"]}/issues/{n})' for n in r["blockers"])
        lines += [f'- [{r["title"]}]({r["url"]}): {reason}.']
    if not waiting: lines += ["No blockers affect work scheduled to start by today."]
    lines += ["", "## Coming in the next seven days", ""]
    for r in upcoming[:12]:
        lines += [f'- {r["due"]}: [{r["title"]}]({r["url"]})' + (" — prerequisites open." if r["blockers"] else ".")]
    if not upcoming: lines += ["No dated issues in this window."]
    mismatch = [r for r in records if (r["fields"].get("Status") == "Done") != (r["state"] == "CLOSED")]
    if mismatch:
        lines += ["", "## Status discrepancies", ""] + [f'- [{r["title"]}]({r["url"]}): issue state and project status disagree; issue state governs this list.' for r in mismatch]
    lines += ["", "## Updating the plan", "", "Update checkboxes, target dates and completion evidence in GitHub. Close completed issues. Record actual listing, fallback and lease dates in planning/github-project.json and rebase dependent project dates. Recurring operations need their next occurrence recorded after each review; a closed recurring issue is not proof that later periods are complete.", ""]
    return "\n".join(lines)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date", help="Optional review date YYYY-MM-DD")
    args=parser.parse_args()
    config=json.loads((ROOT/"planning/github-project.json").read_text())
    now=dt.datetime.now(ZoneInfo(config["timezone"]))
    today=args.date or now.date().isoformat()
    records=normalize(fetch(config), config)
    text=render(records,config,today,now.isoformat(timespec="seconds"))
    (ROOT/"DAILY_TODO.md").write_text(text)
    print(text)

if __name__ == "__main__": main()
