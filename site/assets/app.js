'use strict';
const $=id=>document.getElementById(id);
function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
function link(text,url){const n=el('a','',text);n.href=url;return n;}
function date(value){return value?new Intl.DateTimeFormat('en-US',{month:'short',day:'numeric',timeZone:'America/Chicago'}).format(new Date(value.length===10?value+'T12:00:00Z':value)):'Not scheduled';}
function card(item,type,editorial){const node=el('article','card');const top=el('div','card-top');top.append(el('span','issue-number','#'+item.number),el('span','pill '+(type==='active'?'pending':''),type==='completed'?'Complete':type==='active'?'In progress':'Proposed next'));node.append(top,el('h4','',item.title),el('p','',editorial.summaries[item.number]||'See the issue for the current checklist and context.'));const bottom=el('div','card-bottom');bottom.append(el('span','',type==='completed'?(item.closedAt?'Closed '+date(item.closedAt):'Marked Done'):(item.target?'Target '+date(item.target):'Event dependent')),link('View issue ↗',item.url));node.append(bottom);return node;}
function showTab(){const key=['overview','documents','decisions'].includes(location.hash.slice(1))?location.hash.slice(1):'overview';document.querySelectorAll('.panel').forEach(n=>n.hidden=n.id!==key);document.querySelectorAll('[data-tab]').forEach(n=>{if(n.dataset.tab===key)n.setAttribute('aria-current','page');else n.removeAttribute('aria-current');});}
window.addEventListener('hashchange',showTab);showTab();
Promise.all(['project','editorial'].map(file=>fetch('data/'+file+'.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json();}))).then(([data,editorial])=>{
 const active=data.items.filter(x=>x.status==='In progress');
 const complete=data.items.filter(x=>x.status==='Done').sort((a,b)=>(b.closedAt||'').localeCompare(a.closedAt||'')).slice(0,3);
 const todo=data.items.filter(x=>x.status==='Todo');
 const preferred=editorial.onDeck.map(n=>todo.find(x=>x.number===n)).filter(Boolean);
 const rest=todo.filter(x=>!editorial.onDeck.includes(x.number)).sort((a,b)=>(a.target||'9999').localeCompare(b.target||'9999')||a.number-b.number);
 const queued=[...preferred,...rest].slice(0,3);
 $('active-count').textContent=active.length;$('wip-warning').hidden=active.length<=data.wipLimit;
 for(const [id,items] of [['completed',complete],['active',active],['queued',queued]]){for(const item of items)$(id).append(card(item,id,editorial));if(!items.length)$(id).append(el('p','muted','No items in this stage.'));}
 $('freshness').textContent='GitHub snapshot · '+new Intl.DateTimeFormat('en-US',{dateStyle:'medium',timeStyle:'short',timeZone:'America/Chicago'}).format(new Date(data.updatedAt))+' Central';
 $('stale').hidden=Date.now()-Date.parse(data.updatedAt)<86400000;
 $('queue-note').textContent=editorial.onDeckBasis+' Recently completed is ordered by issue closure date. A Done item without a closure date appears after dated completions.';
 const holds=data.items.filter(x=>x.status==='On hold');for(const item of holds){const n=el('article','hold-item');n.append(link('#'+item.number+' · '+item.title,item.url),el('p','',editorial.holdNotes[item.number]||'Waiting on a dependency. See the issue for the reason and next follow-up.'));$('holds').append(n);}if(!holds.length)$('holds').append(el('p','muted','Nothing on hold right now.'));
 for(const doc of editorial.documents){const n=el('article','card'+(!doc.file?' private':''));n.append(el('span','eyebrow',doc.category),el('h3','',doc.title),el('p','',doc.description));const bottom=el('div','card-bottom');bottom.append(el('span','',doc.status));if(doc.file)bottom.append(link('Read document →','documents/'+doc.id+'.html'));n.append(bottom);$('document-list').append(n);}
 for(const decision of editorial.decisions){const n=el('article','card');n.append(el('span','eyebrow',decision.status),el('h3','',decision.title),el('p','',decision.body));if(decision.issue)n.append(link('Related issue #'+decision.issue+' ↗','https://github.com/BandoKal/bandyland-properties/issues/'+decision.issue));$('decision-list').append(n);}
}).catch(()=>{$('load-error').hidden=false;$('freshness').textContent='Snapshot unavailable';});
