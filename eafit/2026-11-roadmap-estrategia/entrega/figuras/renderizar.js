const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:2,viewport:{width:1100,height:900}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/fuente-figuras.html');await p.waitForTimeout(500);
const ids=await p.$$eval('.fig',a=>a.map(e=>e.id));
for(const id of ids){await (await p.$('#'+id)).screenshot({path:`${id}.png`});}

await b.close();})();
