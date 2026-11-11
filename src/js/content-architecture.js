'use strict';
/* A content inventory and a navigation hierarchy have different relationships.
   Only local, authored sample HTML is inspected. Imported strings remain data. */
(() => {
  const MAX_NODES=1000, MAX_DEPTH=12, MAX_PLAN_CHARS=500000;
  const types=['region','page','section','group','text','image','link','field'];
  const statuses=['present','planned','needs-content'];
  const typeNames={region:'Shared website area',page:'Page',section:'Section',group:'Content group',text:'Text',image:'Image',link:'Link / call to action',field:'Form field / control'};
  const statusNames={present:'Available in the sample',planned:'Still to create','needs-content':'Needs content or revision'};
  const clean=(value,limit)=>typeof value==='string'?value.slice(0,limit):'';
  function normalizeNodes(value,sample) {
    if(!Array.isArray(value))return null;
    const seen=new Set(),rows=[],allowed=new Set((sample?DSStudio.process.inventory(sample):DSStudio.process.inventory('basic').concat(DSStudio.process.inventory('advanced'))).map(([,id])=>id));let total=2;
    for(const item of value.slice(0,MAX_NODES)) {
      if(!item || typeof item!=='object' || !/^content-[a-z0-9-]{1,80}$/.test(item.id || '') || seen.has(item.id) || !clean(item.label,120).trim())continue;
      seen.add(item.id);
      const node={id:item.id,parentId:clean(item.parentId,88)||null,label:clean(item.label,120).trim(),type:types.includes(item.type)?item.type:'text',
        value:clean(item.value,2400),reference:clean(item.reference,1000),notes:clean(item.notes,1200),status:statuses.includes(item.status)?item.status:'planned',sourceKey:clean(item.sourceKey,600),
        target:allowed.has(item.target)?item.target:'',
        draft:typeof item.draft==='string'?item.draft.slice(0,2400):null};
      total+=JSON.stringify(node).length+1;if(total>MAX_PLAN_CHARS)break;
      rows.push(node);
    }
    const byId=new Map(rows.map(node=>[node.id,node]));
    for(const node of rows)if(!byId.has(node.parentId))node.parentId=null;
    const valid=rows.filter(node=>{
      const ancestors=new Set([node.id]);let parent=node.parentId,depth=1;
      while(parent){if(ancestors.has(parent) || ++depth>MAX_DEPTH)return false;ancestors.add(parent);parent=byId.get(parent)?.parentId;}
      return true;
    });
    const validIds=new Set(valid.map(node=>node.id)),children=new Map();
    const repaired=valid.map(node=>({...node,parentId:node.parentId && validIds.has(node.parentId)?node.parentId:null}));
    for(const node of repaired){if(!children.has(node.parentId))children.set(node.parentId,[]);children.get(node.parentId).push(node);}
    const ordered=[];
    const visit=parentId=>{for(const node of children.get(parentId)||[]){ordered.push(node);visit(node.id);}};
    visit(null);return ordered;
  }
  const cache={basic:null,advanced:null},signatures={basic:'',advanced:''};let collecting=false;
  const mode=()=>state.sampleMode==='basic'?'basic':'advanced';
  const hash=value=>{let n=2166136261;for(const char of value){n^=char.charCodeAt(0);n=Math.imul(n,16777619);}return (n>>>0).toString(36);};
  function inventory(html,sample) {
    const doc=new DOMParser().parseFromString(html,'text/html'),nodes=[],keys=new Set();
    const names=new Map(DSStudio.process.inventory(sample).map(([name,id])=>[id,name]));
    const compact=value=>String(value??'').replace(/\s+/g,' ').trim().slice(0,2400);
    const add=(label,type,value,parent,key,target='')=>{
      if(nodes.length>=MAX_NODES)return null;
      while(keys.has(key))key+='-copy';keys.add(key);
      const node={id:'content-'+hash(key),parentId:parent?.id||null,label:label.slice(0,120),type,value:compact(value),reference:'',notes:'',status:'present',sourceKey:key,target,draft:null};
      // Hash collisions are resolved deterministically, never used to merge entries.
      while(nodes.some(old=>old.id===node.id))node.id+='-copy';
      nodes.push(node);return node;
    };
    function walk(element,parent,path,depth=1) {
      if(depth>MAX_DEPTH || !element || element.nodeType!==1 || element.matches('script,style,link,svg,template,[aria-hidden="true"]'))return;
      const tag=element.localName, text=compact(element.textContent),anchor=element.id;
      const key=anchor?'id:'+anchor:path;
      let node=null,stop=false;
      if(element.closest('nav') && (tag==='ul' || tag==='li')){[...element.children].forEach((child,index)=>walk(child,parent,key+'/'+child.localName+':'+index,depth));return;}
      if(element.matches('a.brand, a.sample-brand')) {
        add('Logo','image',compact(element.querySelector('.logo, .sample-logo')?.textContent)||'Brand mark',parent,key+'/logo');
        const parts=[...element.children].filter(child=>!child.matches('.logo, .sample-logo, svg'));
        add('Wordmark','text',compact(parts.map(child=>child.textContent).join(' '))||state.project,parent,key+'/wordmark');return;
      }
      if(anchor==='sitemap'){add('Visitor sitemap','group','Generated from selected sitemap destinations',parent,key);return;}
      if(anchor==='ia-lab'){const group=add('Information architecture','section','Content structure and visitor sitemap',parent,key,anchor);add('Planning views','group','Generated from the content plan and selected sitemap destinations',group,key+'/views');return;}
      if(tag==='header' || tag==='footer')node=add(tag==='header'?'Header':'Footer','region','Shared website region',parent,key,tag==='footer'?'footer':'');
      else if(tag==='section' || tag==='article' || tag==='aside')node=add(names.get(anchor)||element.getAttribute('aria-label')||compact(element.querySelector('h2,h3,h4')?.textContent)||({section:'Section',article:'Article',aside:'Related information'}[tag]),'section','',parent,key,names.has(anchor)?anchor:'');
      else if(tag==='nav')node=add(element.getAttribute('aria-label')||'Navigation','group','Links reference destinations elsewhere in this outline',parent,key);
      else if(tag==='figure')node=add(parent?.label==='Hero'?'Hero image':'Image and caption','group','',parent,key);
      else if(tag==='form')node=add('Form','group',element.getAttribute('aria-label')||'Labelled form controls',parent,key,names.has(anchor)?anchor:'');
      else if(tag==='fieldset')node=add('Grouped choices','group',compact(element.querySelector('legend')?.textContent),parent,key,names.has(anchor)?anchor:'');
      else if(tag==='details')node=add(element.closest('header')?'Responsive navigation':'Disclosure','group',compact(element.querySelector('summary')?.textContent),parent,key);
      else if(['ul','ol','dl','table','blockquote'].includes(tag))node=add(({ul:'List',ol:'Ordered list',dl:'Terms and definitions',table:'Table',blockquote:'Quotation'})[tag],'group','',parent,key);
      else if(tag==='img') {node=add('Image','image',element.getAttribute('src')?.startsWith('data:')?'Local generated illustration':'Website image',parent,key);add('Alternative text','text',element.getAttribute('alt')||'Decorative image',node,key+'/alt');return;}
      else if(/^h[1-6]$/.test(tag)){node=add('Heading','text',text,parent,key);stop=true;}
      else if(tag==='p' || tag==='figcaption' || tag==='summary' || tag==='legend' || tag==='caption' || tag==='small') {node=add(({p:element.matches('[class*="eyebrow"]')?'Eyebrow':'Paragraph',figcaption:'Caption',summary:'Disclosure label',legend:'Group label',caption:'Table caption',small:'Supporting text'})[tag],'text',text,parent,key);stop=true;}
      else if(tag==='a' || tag==='button') {const href=element.getAttribute('href')||'',target=href.startsWith('#') && names.has(href.slice(1))?href.slice(1):'';const label=tag==='button'?'Button':element.closest('nav')?text:element.matches('.ds-button--primary')?'Primary CTA':element.matches('.ds-button--secondary')?'Secondary CTA':'Link';const link=add(label||'Link',tag==='a'?'link':'field',text,parent,key,target);if(link)link.reference=href.slice(0,1000);return;}
      else if(['input','textarea','select','progress'].includes(tag)) {
        const label=element.id?[...doc.querySelectorAll('label')].find(label=>label.htmlFor===element.id):null;
        node=add(compact(label?.textContent || element.closest('label')?.textContent)||element.getAttribute('aria-label')||'Control','field',element.value||element.getAttribute('value')||element.getAttribute('placeholder')||'',parent,key);
        if(tag==='select')for(const [index,option] of [...element.options].entries())add('Option','text',option.textContent,node,key+'/option:'+index);
        return;
      }
      else if(['li','dt','dd','th','td'].includes(tag) && !element.querySelector('section,article,ul,ol,dl,table')) {add(({li:'List item',dt:'Term',dd:'Definition',th:'Column heading',td:'Cell'})[tag],'text',text,parent,key);for(const [i,link]of [...element.querySelectorAll('a')].entries())walk(link,parent,key+'/link:'+i,depth+1);return;}
      else if(['span','strong','cite'].includes(tag) && !element.children.length && text){add('Text','text',text,parent,key);return;}
      // An authored destination such as Card grid is a meaningful content group
      // even when its implementation uses a div. Ordinary layout wrappers stay out.
      if(names.has(anchor)){
        if(node){node.target=anchor;if(['group','text'].includes(node.type))node.label=names.get(anchor);}
        else node=add(names.get(anchor),'group','',parent,key,anchor);
      }
      if(node && node.target==='home')node=add('Hero','group','',node,key+'/hero');
      if(stop){for(const [i,link]of [...element.querySelectorAll('a')].entries())walk(link,node,key+'/link:'+i,depth+1);return;}
      [...element.children].forEach((child,index)=>walk(child,node||parent,key+'/'+child.localName+':'+index,depth+(node?1:0)));
    }
    for(const element of doc.querySelectorAll('body > header, body > main > section, body > footer'))walk(element,null,'root/'+element.localName);
    return nodes;
  }
  function prepare() {
    const sample=mode(),factory=DSStudio.samples?.[sample+'Html'];if(collecting || !factory)return;
    const {contentPlan,...planning}=state.designProcess||{};
    const signature=JSON.stringify({...state,designProcess:planning,advanced:typeof adv==='object'?adv:null});
    if(signatures[sample]===signature)return;
    collecting=true;
    try{cache[sample]=inventory(factory(),sample);signatures[sample]=signature;}finally{collecting=false;}
  }
  function nodes() {
    prepare();const sample=mode(),source=cache[sample]||[];
    const saved=state.designProcess?.contentPlan?.[sample];
    if(Array.isArray(saved)){
      const actual=new Map(source.map(node=>[node.sourceKey,node]));
      return normalizeNodes(saved,sample).map(node=>({...node,value:node.sourceKey?actual.get(node.sourceKey)?.value||'':node.value,reference:node.sourceKey?actual.get(node.sourceKey)?.reference||'':node.reference,sourceMissing:!!node.sourceKey && !actual.has(node.sourceKey)}));
    }
    const result=source.map(node=>({...node}));
    const plan=DSStudio.process.currentPlan(),legacy=DSStudio.process.entries(plan),standard=plan.pages===DSStudio.process.samplePages();
    // Custom outlines remain visible as planning entries. Existing sample paths
    // already have actual counterparts, rather than duplicate sample destinations.
    if(!standard){
      const claimed=new Set();
      for(const entry of legacy){
        const parent=result.find(node=>node.id==='content-legacy-'+entry.parentId),target=DSStudio.process.destinationId(entry.label,plan,sample);
        const actual=target && !claimed.has(target)?result.find(node=>node.target===target && node.type!=='link'):null;
        if(actual){
          const oldId=actual.id;actual.id='content-legacy-'+entry.id;actual.label=entry.label;actual.parentId=parent?.id||null;
          for(const child of result)if(child.parentId===oldId)child.parentId=actual.id;
          claimed.add(target);
        }else result.push({id:'content-legacy-'+entry.id,parentId:parent?.id||null,label:entry.label,type:target?'link':entry.type==='group'?'group':entry.type==='content'?'text':'section',value:'',reference:'',notes:'Imported from the previous outline',status:'planned',sourceKey:'',target,draft:null});
      }
    }
    return result.slice(0,MAX_NODES);
  }
  function descendants(list,id){const result=new Set([id]);let changed=true;while(changed){changed=false;for(const node of list)if(result.has(node.parentId) && !result.has(node.id)){result.add(node.id);changed=true;}}return result;}
  const path=(list,node)=>{const parts=[];let current=node;for(let i=0;current && i<MAX_DEPTH;i++){parts.unshift(current.label);current=list.find(item=>item.id===current.parentId);}return parts;};
  function markup() {
    if(collecting)return '<p>Generated content structure.</p>';
    const list=nodes(),esc=escapeHtml,byParent=new Map(),names=new Map(DSStudio.process.inventory(mode()).map(([label,id])=>[id,label]));
    for(const node of list){if(!byParent.has(node.parentId))byParent.set(node.parentId,[]);byParent.get(node.parentId).push(node);}
    const branch=(parentId=null)=>`<ul>${(byParent.get(parentId)||[]).map(node=>{const children=byParent.has(node.id),value=node.value;const label=`<strong>${esc(node.label)}</strong> <small>${esc(typeNames[node.type])}${node.status!=='present'?' · '+esc(statusNames[node.status]):''}</small>`;return `<li>${children?`<details data-content-branch="${esc(node.id)}"><summary>${label}</summary>`:label}${value?`<p>${esc(value)}</p>`:''}${node.target?`<p class="help">${node.type==='link'?'References':'Destination'}: ${esc(names.get(node.target)||node.target)}</p>`:''}${node.reference?`<p class="help">Reference: ${esc(node.reference)}</p>`:''}${node.draft!==null?`<p><strong>Planned content:</strong> ${esc(node.draft)||'(deliberately empty)'}</p><p class="help">Sample content is unchanged.</p>`:''}${node.notes?`<p class="help">${esc(node.notes)}</p>`:''}${children?branch(node.id)+'</details>':''}</li>`;}).join('')}</ul>`;
    return `<section class="ia-content-map" aria-label="Complete website content structure"><h4>Website content structure</h4><p>Regions, sections, groups and actual content. Expand a branch to inspect its text, images, controls and destination references. ${list.length} entries.</p>${list.length?branch():'<p>No content entries. Add an entry or restore the sample content inventory.</p>'}</section>`;
  }
  DSStudio.contentArchitecture={MAX_NODES,MAX_DEPTH,MAX_PLAN_CHARS,types,statuses,typeNames,statusNames,normalizeNodes,prepare,nodes,descendants,path,markup,inventory};
})();
