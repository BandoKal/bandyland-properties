#!/usr/bin/env python3
"""Read live project + issue state with gh. Write only public dashboard fields."""
import json, subprocess, re
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def gh(*args):
    return json.loads(subprocess.check_output(['gh',*args],text=True))
def decision_alerts(items, issues, editorial):
    by_number={i['number']:i for i in issues}
    eligible={i['number']:i for i in items if i['status'] in ('In progress','On hold') and not i.get('closedAt')}
    documents={d['id']:d for d in editorial['documents'] if d.get('file')}
    alerts=[]
    for decision in editorial['decisions']:
        number=decision.get('issue')
        if decision['status']!='To decide' or number not in eligible: continue
        doc=documents.get(decision.get('document'))
        if not doc: raise ValueError(f'Pending decision #{number} needs a public decision document')
        checkpoint=decision.get('completionChecklist')
        body=by_number.get(number,{}).get('body','')
        if checkpoint and re.search(r'^\s*- \[x\] '+re.escape(checkpoint)+r'\s*$',body,re.M|re.I): continue
        alerts.append({'issue':number,'status':eligible[number]['status'],'title':decision['title'],
                       'documentTitle':doc['title'],'documentUrl':f"documents/{doc['id']}.html",
                       'issueUrl':eligible[number]['url']})
    return alerts

def snapshot(project, issues):
    by_number={i['number']:i for i in issues}
    excluded=set(json.loads((ROOT/'planning/github-project.json').read_text()).get('archived_out_of_scope_issues',[]))
    items=[]
    for row in project['items']:
        number=row['content'].get('number')
        if not number or number in excluded: continue
        issue=by_number.get(number,{})
        labels=[label['name'] for label in issue.get('labels',[])]
        if not {'rental','operations'}.intersection(label.casefold() for label in labels): continue
        items.append({'number':number,'title':re.sub(r'^\[[^]]+\]\s*','',row['title']),
                      'labels':labels,'status':row.get('status','Todo'),'closedAt':issue.get('closedAt'),
                      'target':row.get('target date'),'priority':row.get('priority',''),
                      'url':f'https://github.com/BandoKal/bandyland-properties/issues/{number}'})
    return {'updatedAt':datetime.now(timezone.utc).isoformat(), 'source':'Live GitHub Project 7 and repository issues',
            'wipLimit':3,'items':items,'decisionAlerts':decision_alerts(items,issues,json.loads((ROOT/'site/data/editorial.json').read_text()))}
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--project-file');parser.add_argument('--issues-file');args=parser.parse_args()
    project=json.loads(Path(args.project_file).read_text()) if args.project_file else gh('project','item-list','7','--owner','BandoKal','--limit','100','--format','json')
    issues=json.loads(Path(args.issues_file).read_text()) if args.issues_file else gh('issue','list','--repo','BandoKal/bandyland-properties','--state','all','--limit','100','--json','number,closedAt,labels,body')
    (ROOT/'site/data/project.json').write_text(json.dumps(snapshot(project,issues),indent=2)+'\n')
