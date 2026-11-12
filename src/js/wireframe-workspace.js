"use strict";
DSStudio.register({
  id:'wireframe-workspace',title:'Read-only responsive website wireframe',
  init() {
    const engine=DSStudio.wireframeEngine,get=id=>document.getElementById(id),mode=()=>state.sampleMode==='basic'?'basic':'advanced';
    const artifact=document.querySelector('#process-wireframe [data-process-artifact="wireframe"]');
    const workspace=document.createElement('section');workspace.id='wireframe-workspace';workspace.className='wireframe-workspace';workspace.setAttribute('aria-labelledby','wireframe-workspace-title');
    workspace.innerHTML=`<header><h3 id="wireframe-workspace-title" tabindex="-1">Website wireframe</h3><p>A read-only, low-fidelity view of the same HTML and responsive layout as the live website. Saved website content changes in Architecture appear here automatically.</p></header>
      <div class="wf-view-controls"><div class="button-row" aria-label="Wireframe website sample"><button type="button" class="ghost" id="wf-basic" aria-pressed="true">Basic</button><button type="button" class="ghost" id="wf-advanced" aria-pressed="false">Advanced</button></div><div><label for="wf-width">Viewport</label><select id="wf-width"><option value="live">Match live preview</option><option value="320">320 px</option><option value="390">390 px</option><option value="768">768 px</option><option value="1280">1280 px</option><option value="fluid">Available width</option></select></div></div>
      <p class="help wf-container-key"><strong>Container outlines:</strong> solid = page regions; dashed = content-width containers; dotted = Grid/Flex groups; thin = child containers. Outlines follow the actual HTML layout.</p><p id="wf-summary" class="help" role="status"></p><div id="wf-viewport" class="wf-viewport" tabindex="0" role="region" aria-label="Scrollable read-only website wireframe"><iframe id="wf-page" title="Read-only Basic website wireframe" sandbox="allow-same-origin" srcdoc="<!doctype html><html lang='en'><head><meta charset='utf-8'></head><body></body></html>"></iframe></div>
      <div class="button-row wf-view-actions"><button type="button" class="ghost" id="wf-open-live">Compare with live website</button><button type="button" class="ghost" id="wf-download">Download wireframe HTML</button></div><p id="wf-status" class="help" role="status"></p>`;
    artifact.replaceWith(workspace);
    const pane=document.querySelector('[data-journey-pane="2"]');pane.querySelector('p.help').textContent='Review a low-fidelity version of the Basic or Advanced website. Its layout follows the same responsive HTML and CSS as the live preview.';
    const open=document.createElement('button');open.id='open-wireframe-workspace';open.type='button';open.className='ghost';open.textContent='Open Wireframe view';pane.querySelector('p.help').after(open);
    open.addEventListener('click',()=>{window.dssRevealSection('process-wireframe',false);get('wireframe-workspace-title').focus();get('wireframe-workspace-title').scrollIntoView({block:'start',behavior:'instant'});});
    const frame=get('wf-page'),wired=new WeakSet();let queued=false,previous='',previousMode='',liveWidth=0;
    function size() {
      const choice=get('wf-width').value,live=get('previewFrame').dataset.width;
      let width=choice==='fluid'?get('wf-viewport').clientWidth:Number(choice);
      if(choice==='live')width=({mobile:390,tablet:768,desktop:1280})[live]||liveWidth||get('wf-viewport').clientWidth;
      width=Math.max(240,Math.round(width||320));frame.style.width=width+'px';
      frame.title='Read-only '+(mode()==='basic'?'Basic':'Advanced')+' website wireframe';
      get('wf-basic').setAttribute('aria-pressed',String(mode()==='basic'));get('wf-advanced').setAttribute('aria-pressed',String(mode()==='advanced'));
      get('wf-summary').textContent=(mode()==='basic'?'Basic':'Advanced')+' wireframe - '+width+' px viewport. '+(choice==='live'?'Matches the live preview width. ':'')+'Scroll inside the view when needed. Forms are read only; navigation and disclosures can be inspected.';
    }
    function detailKeys(doc) {
      const seen=new Map();return [...doc.querySelectorAll('details')].map(node=>{const key=node.id||node.dataset.contentBranch||node.querySelector('summary')?.textContent||'Disclosure',count=seen.get(key)||0;seen.set(key,count+1);return [key+':'+count,node];});
    }
    function wire(doc) {
      if(wired.has(doc))return;wired.add(doc);
      doc.addEventListener('submit',event=>event.preventDefault(),true);
      doc.addEventListener('click',event=>{
        const anchor=event.target.closest('a[href]');if(!anchor)return;event.preventDefault();
        const href=anchor.getAttribute('href');if(!href.startsWith('#'))return;
        let target;try{target=doc.getElementById(decodeURIComponent(href.slice(1)));}catch{return;}if(!target)return;
        for(let node=target;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
        doc.defaultView.scrollTo({top:doc.defaultView.scrollY+target.getBoundingClientRect().top-24,behavior:'instant'});
      });
    }
    function refresh(force=false) {
      queued=false;if(!force && DSStudio.activeStage!==2)return;
      const doc=frame.contentDocument;if(!doc?.head || !doc.body)return;
      const parsed=engine.createDocument({preview:true}),signature=parsed.documentElement.outerHTML;
      if(signature!==previous || previousMode!==mode()) {
        const same=previousMode===mode(),scroll=same?{x:frame.contentWindow.scrollX,y:frame.contentWindow.scrollY}:{x:0,y:0},openDetails=new Map(same?detailKeys(doc).map(([key,node])=>[key,node.open]):[]);
        for(const name of ['documentElement','body']){for(const attr of [...doc[name].attributes])doc[name].removeAttribute(attr.name);for(const attr of parsed[name].attributes)doc[name].setAttribute(attr.name,attr.value);}
        doc.head.replaceChildren(...[...parsed.head.childNodes].map(node=>doc.importNode(node,true)));
        doc.body.replaceChildren(...[...parsed.body.childNodes].map(node=>doc.importNode(node,true)));
        for(const [key,node]of detailKeys(doc))if(openDetails.has(key))node.open=openDetails.get(key);
        previous=signature;previousMode=mode();frame.contentWindow.scrollTo(scroll.x,scroll.y);
      }
      wire(doc);DSStudio.fonts.syncPreview(doc);size();
    }
    function schedule() {if(queued || DSStudio.activeStage!==2)return;queued=true;queueMicrotask(()=>refresh());}
    for(const [id,target]of [['wf-basic','dockModeBasic'],['wf-advanced','dockModeAdvanced']])get(id).addEventListener('click',()=>get(target).click());
    get('wf-width').addEventListener('change',size);
    get('wf-open-live').addEventListener('click',()=>{window.dssRevealSection('previewShell',false);get('previewShell').focus();get('previewShell').scrollIntoView({block:'start',behavior:'instant'});});
    get('wf-download').addEventListener('click',()=>{download('wireframe.html',engine.documentHtml(),'text/html');get('wf-status').textContent='Read-only wireframe HTML download requested.';});
    frame.addEventListener('load',schedule);
    new ResizeObserver(size).observe(get('wf-viewport'));
    DSStudio.on('preview:change',({width})=>{if(width>0)liveWidth=width;if(get('wf-width').value==='live')size();});
    DSStudio.on('stage:change',({stage})=>{if(stage.index===2)schedule();});
    for(const event of ['dss:reset','dss:imported'])document.addEventListener(event,()=>{previous='';get('wf-status').textContent='';schedule();});
    const before=renderCode;renderCode=function(){before();schedule();};
    DSStudio.wireframeView={refresh:()=>refresh(true),frame};size();schedule();
  }
});
