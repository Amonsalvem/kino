import fs from 'node:fs';
const P=JSON.parse(fs.readFileSync('patrones-nuevos.json','utf8')).map(p=>({...p,re:new RegExp(p.regex,(p.flags||'')+'gu')}));
const run=(f)=>{const L=fs.readFileSync(f,'utf8').split('\n');let n=0;for(const l of L)for(const p of P)for(const m of l.matchAll(p.re)){n++;console.log(f.split('/').pop(),p.gravedad,p.id,'«'+m[0]+'»','::',l.slice(0,80));}return n;};
for(const f of process.argv.slice(2)) console.log(f,'→',run(f));
