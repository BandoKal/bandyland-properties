import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
let marked;
try {({marked}=await import('marked'));} catch {({marked}=await import(pathToFileURL('/Users/jason/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js')));}
const output=path.join(root,'site-dist');fs.rmSync(output,{recursive:true,force:true});fs.mkdirSync(output,{recursive:true});
for(const entry of ['index.html','assets','data'])fs.cpSync(path.join(root,'site',entry),path.join(output,entry),{recursive:true});
fs.mkdirSync(path.join(output,'documents'));fs.mkdirSync(path.join(output,'downloads'));
const config=JSON.parse(fs.readFileSync(path.join(root,'site/data/editorial.json')));
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
for(const doc of config.documents.filter(d=>d.file)){
 const content=fs.readFileSync(path.join(root,'site/content',doc.file),'utf8');
 if(/<script|<iframe|javascript:/i.test(content))throw Error('Unsafe HTML in '+doc.file);
 const html=marked.parse(content,{gfm:true});
 fs.writeFileSync(path.join(output,'documents',doc.id+'.html'),`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>${escape(doc.title)} · BandyLand</title><link rel="stylesheet" href="../assets/style.css"></head><body><main class="shell reader"><div class="reader-actions"><a class="back" href="../index.html#documents">← Back to documents</a><a href="../downloads/${encodeURIComponent(doc.file)}" download>Download Markdown ↓</a></div><article>${html}</article><footer>Public review copy · Original financial documents remain private.</footer></main></body></html>`);
 fs.copyFileSync(path.join(root,'site/content',doc.file),path.join(output,'downloads',doc.file));
}
fs.writeFileSync(path.join(output,'.nojekyll'),'');
fs.writeFileSync(path.join(output,'404.html'),'<html lang="en"><meta charset="utf-8"><title>Not found · BandyLand</title><h1>This page has moved.</h1><a href="/bandyland-properties/">Return to the project dashboard</a></html>');
console.log('Built '+config.documents.filter(d=>d.file).length+' public documents and dashboard in site-dist/');
