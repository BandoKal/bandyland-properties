"""Adopt the user's working project; preserve nonempty fields and issue edits."""
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def gh(*args, payload=None):
    r=subprocess.run(['gh',*args],input=json.dumps(payload) if payload is not None else None,text=True,capture_output=True,check=True,timeout=90)
    return json.loads(r.stdout) if r.stdout.strip() else None
def graphql(q):
    r=gh('api','graphql','--input','-',payload={'query':q})
    if r.get('errors'): raise RuntimeError(r['errors'])
    return r['data']
p=ROOT/'planning/github-project.json'; c=json.loads(p.read_text())
old=dict(c)
project=gh('project','view','7','--owner','BandoKal','--format','json')
fields=gh('project','field-list','7','--owner','BandoKal','--format','json')['fields']
for name,kind,options in [('Workstream','SINGLE_SELECT','Funding,Rental,Operations,BandyWorks,Property Equipment'),('Date basis','TEXT',None),('Depends on','TEXT',None),('Trigger','TEXT',None)]:
    if not any(f['name']==name for f in fields):
        args=['project','field-create','7','--owner','BandoKal','--name',name,'--data-type',kind,'--format','json']
        if options: args+=['--single-select-options',options]
        gh(*args)
fields={f['name']:f for f in gh('project','field-list','7','--owner','BandoKal','--format','json')['fields']}
q='{user(login:"BandoKal"){projectV2(number:7){views(first:20){nodes{name number}} items(first:100){nodes{id content{... on Issue{number}} fieldValues(first:30){nodes{... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}}}}}}}}'
data=graphql(q)['user']['projectV2']
items={i['content']['number']:i for i in data['items']['nodes'] if i.get('content',{}).get('number')}
c.update(project_number=7,project_id=project['id'],project_url=project['url'],fields=fields,publication_status='user_project_active',previous_project_number=5,views=[{'name':v['name'],'url':project['url']+'/views/'+str(v['number'])} for v in data['views']['nodes']])
p.write_text(json.dumps(c,indent=2)+'\n')
tasks=json.loads((ROOT/'planning/tasks.json').read_text())
for t in tasks:
    i=items.get(t['issue_number'])
    if not i: continue
    existing={v['field']['name']:v.get('date',v.get('text',v.get('name'))) for v in i['fieldValues']['nodes'] if v.get('field')}
    # Recover original metadata from the old saved item, not stale initial definitions.
    q='query{node(id:'+json.dumps(t['project_item_id'])+'){... on ProjectV2Item{fieldValues(first:30){nodes{... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldDateValue{date field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2FieldCommon{name}}}}}}}}'
    node=graphql(q)['node']
    vals={v['field']['name']:v.get('date',v.get('text',v.get('name'))) for v in node['fieldValues']['nodes'] if v.get('field')} if node else {}
    muts=[]
    for name in ['Start date','Target date','Workstream','Priority','Date basis','Depends on','Trigger']:
        value=vals.get(name)
        if existing.get(name) or not value: continue
        f=fields[name]
        if f.get('options'):
            literal='{singleSelectOptionId:'+json.dumps(next(o['id'] for o in f['options'] if o['name']==value))+'}'
        else: literal='{'+('date' if name in ['Start date','Target date'] else 'text')+':'+json.dumps(value)+'}'
        muts.append('m'+str(len(muts))+':updateProjectV2ItemFieldValue(input:{projectId:'+json.dumps(c['project_id'])+',itemId:'+json.dumps(i['id'])+',fieldId:'+json.dumps(f['id'])+',value:'+literal+'}){projectV2Item{id}}')
    if muts: graphql('mutation{'+' '.join(muts)+'}')
    t['previous_project_item_id']=t['project_item_id']; t['project_item_id']=i['id']
    print('Adopted',t['key'],flush=True)
(ROOT/'planning/tasks.json').write_text(json.dumps(tasks,indent=2)+'\n')
f=fields['Status']; opt=next(o['id'] for o in f['options'] if o['name'].lower()=='in progress')
graphql('mutation{updateProjectV2ItemFieldValue(input:{projectId:'+json.dumps(c['project_id'])+',itemId:'+json.dumps(items[1]['id'])+',fieldId:'+json.dumps(f['id'])+',value:{singleSelectOptionId:'+json.dumps(opt)+'}}){projectV2Item{id}}}')
issue=gh('issue','view','1','--repo',c['repository'],'--json','body')
heading='## Working session breakdown'
if heading not in issue['body']:
    issue['body']+='\n\n'+heading+'\n\nWorking in [BandyLand project 7](https://github.com/users/BandoKal/projects/7/views/2). No funding choice is approved yet.\n\n1. **Reserve:** confirm whether the reduction from $18,000 to $9,000 was intentional. Keep this cash separate from startup spending.\n2. **Startup scope:** review the ten planning estimates totaling $11,310, identifying quotes, completed work, owner labor and items that can be removed.\n3. **Contingency:** decide whether to retain an additional $2,000 after funding identified work, or use a different approved allowance.\n4. **Funding total:** add the chosen reserve, agreed startup estimates and contingency; confirm the effect on remaining emergency cash.\n5. **Distribution rules:** confirm the reserve floor, funding/ramp approach and when owner payments may begin.\n6. **Implement and verify:** update a working workbook copy, preserve the original, check formulas and document approval before closing.\n\nCurrent step: reserve decision pending owner response. The $22,310 plan case equals $9,000 reserve + $11,310 startup + $2,000 contingency. It is a comparison case, not an approved expenditure.\n'
    body=ROOT/'planning/issue-1-working-body.md'; body.write_text(issue['body'])
    subprocess.run(['gh','issue','edit','1','--repo',c['repository'],'--body-file',str(body)],check=True)
for name in ['README.md','TASKS.md','DAILY_TODO.md']:
    f=ROOT/name
    f.write_text(f.read_text().replace('https://github.com/users/BandoKal/projects/5','https://github.com/users/BandoKal/projects/7'))
print('Project 7 adopted; first issue in progress.',flush=True)
