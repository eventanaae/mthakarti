const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/rest/v1/**',r=>r.fulfill({status:200,contentType:'application/json',body:'null'}));
await p.goto('http://localhost:8765/');await p.waitForTimeout(1500);
const out=await p.evaluate(()=>{const R={};for(const g of Object.keys(GR)){try{setGrade(g)}catch(e){R.err=String(e)}
  R[g]={name:GR[g].name,subj:{}};for(const k of Object.keys(SUBJ)){const s=SUBJ[k];if(!s||!s.T)continue;
   R[g].subj[k]={name:(typeof nm==='function'?nm(k):k),icon:s.icon,lang:(typeof SL==='function'?SL(s):'ar'),T:s.T.map(t=>({id:t.id,t:t.t,q:t.q||'',say:t.say||'',html:t.html||'',deep:t.deep||''})),nq:(s.Q||[]).length,
   Q:(s.Q||[])}}}return R});
require('fs').writeFileSync('/tmp/claude-0/-home-user/242672e9-88fd-5bd4-8dd6-344d4898db65/scratchpad/lessons.json',JSON.stringify(out));
for(const g in out){if(g==='err')continue;const s=out[g].subj;console.log(g,out[g].name,Object.keys(s).map(k=>k+':'+s[k].T.length).join(' '))}
console.log('err',out.err);const any=Object.values(out.g12a.subj)[0];console.log(JSON.stringify(any.Q[0]).slice(0,500));console.log(any.T[0].html.slice(0,500));console.log(String(any.T[0].deep).slice(0,300));await b.close()})();
