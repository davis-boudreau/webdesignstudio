'use strict';
/* Plain-text edits bind to local authored nodes, never to imported selectors/HTML. */
(() => {
  const MAX_FIELDS=2000,MAX_CHARS=2400,MAX_TOTAL=120000;
  const identity=row=>JSON.stringify([row.sourceKey,row.field,row.fingerprint]);
  const hash=value=>{let n=2166136261;for(const char of value){n^=char.charCodeAt(0);n=Math.imul(n,16777619);}return (n>>>0).toString(36);};
  function normalize(value) {
    if(!Array.isArray(value))return [];
    const result=[],seen=new Set();let total=2;
    for(const row of value.slice(0,MAX_FIELDS)) {
      if(!row || typeof row!=='object' || typeof row.sourceKey!=='string' || !row.sourceKey || row.sourceKey.length>600 ||
        typeof row.field!=='string' || !/^(text:\d{1,3}|alt|placeholder|aria-label|value)$/.test(row.field) || typeof row.fingerprint!=='string' || !/^[a-z0-9]{1,16}$/.test(row.fingerprint) || typeof row.value!=='string')continue;
      const next={sourceKey:row.sourceKey,field:row.field,fingerprint:row.fingerprint,value:row.value.slice(0,MAX_CHARS)},id=identity(next);
      if(seen.has(id))continue;
      total+=JSON.stringify(next).length+1;if(total>MAX_TOTAL)break;
      seen.add(id);result.push(next);
    }
    return result;
  }
  const caches={basic:null,advanced:null};let inspecting=false;
  function scan(html,mode) {
    if(caches[mode]?.html===html)return caches[mode];
    const doc=new DOMParser().parseFromString(html,'text/html'),entries=new Map(),fields=new Map(),textSlots=new WeakMap(),attributeSlots=new WeakMap();
    const generated=element=>element.closest('#sitemap,.sample-process-stage');
    const owned=element=>element.closest('[data-website-setting],a.brand,a.sample-brand,.footer-brand,.sample-selected-action,#sample-action-help,.sample-token-palette code');
    function slot(entry,element,field,label,target,attribute=null) {
      let existing;
      if(attribute)existing=attributeSlots.get(target)?.get(attribute);else existing=textSlots.get(target);
      if(existing){if(!entry.fields.some(field=>identity(field)===identity(existing)))entry.fields.push({...existing,label});return;}
      const original=attribute?target.getAttribute(attribute)||'':target.nodeValue;
      const descriptor={sourceKey:entry.sourceKey,field,fingerprint:hash(element.localName+'|'+field+'|'+original),label,original,
        write:value=>{if(attribute)target.setAttribute(attribute,value);else {const option=target.parentElement;if(option?.localName==='option' && !option.hasAttribute('value') && value!==original)option.setAttribute('value',option.value);target.nodeValue=value;}}};
      if(attribute){if(!attributeSlots.has(target))attributeSlots.set(target,new Map());attributeSlots.get(target).set(attribute,descriptor);}else textSlots.set(target,descriptor);
      entry.fields.push(descriptor);fields.set(identity(descriptor),descriptor);
    }
    function text(entry,element,label='Text') {
      let index=0;
      const walk=node=>{
        if(node.nodeType===3){if(node.nodeValue.trim())slot(entry,element,'text:'+index++,label,node);return;}
        if(node.nodeType!==1 || node.matches('script,style,svg,template,[aria-hidden="true"],input,select,progress') || owned(node))return;
        for(const child of node.childNodes)walk(child);
      };
      walk(element);
    }
    DSStudio.contentArchitecture.inventory(html,mode,(node,element)=>{
      const entry={sourceKey:node.sourceKey,fields:[],reason:''};entries.set(node.sourceKey,entry);
      if(generated(element)){entry.reason='Generated from the saved plan or sitemap settings. Edit its source in the relevant planning section.';return;}
      if(owned(element) || /\/(logo|wordmark)$/.test(node.sourceKey)){entry.reason='Project identity and component settings control this content. Change the project name in Brief or use the component settings.';return;}
      if(/\/text:\d+$/.test(node.sourceKey)) {
        const target=element.childNodes[Number(node.sourceKey.split('/text:').pop())];if(target?.nodeType===3)slot(entry,element,'text:0','Text',target);
      } else if(element.localName==='img')slot(entry,element,'alt','Alternative text',element,'alt');
      else if(node.sourceKey.includes('/option:')) {
        const option=element.options[Number(node.sourceKey.split('/option:').pop())];if(option)text(entry,option,'Option wording');
      } else if(['input','textarea','select','progress'].includes(element.localName)) {
        for(const label of element.labels||[])text(entry,label,'Field label');
        if(element.localName==='textarea'){
          if(!element.firstChild)element.append(doc.createTextNode(''));
          slot(entry,element,'text:0','Initial text',element.firstChild);
        }
        if(element.localName==='textarea' || (element.localName==='input' && ['text','search','email','tel','url','password','number'].includes(element.type)))slot(entry,element,'placeholder','Placeholder',element,'placeholder');
        if(element.localName==='input' && ['text','search','email','tel','url','password','number'].includes(element.type) && element.hasAttribute('value'))slot(entry,element,'value','Initial text',element,'value');
        if(element.localName==='input' && ['button','submit','reset'].includes(element.type))slot(entry,element,'value','Button wording',element,'value');
      } else if(['text','link','field'].includes(node.type))text(entry,element,node.type==='link'?'Link wording':node.type==='field'?'Button wording':node.label);
      if(element.hasAttribute('aria-label'))slot(entry,element,'aria-label',['region','section','group'].includes(node.type)?'Accessible area label':'Accessible label',element,'aria-label');
      if(!entry.fields.length)entry.reason='This item contains other content. Expand its branch and select the text, image or control you want to change.';
    },doc);
    const result={html,doc,entries,fields};caches[mode]=result;return result;
  }
  function records(mode) {return normalize(state.designProcess?.websiteContent?.[mode]);}
  function inspect(mode) {
    if(inspecting)return null;
    const factory=DSStudio.samples?.[mode+'SourceHtml'];if(!factory)return null;
    inspecting=true;try{return scan(factory(),mode);}finally{inspecting=false;}
  }
  function describe(sourceKey,mode) {
    const data=inspect(mode),saved=new Map(records(mode).map(row=>[identity(row),row])),entry=data?.entries.get(sourceKey);
    return {fields:(entry?.fields||[]).map(field=>({...field,value:saved.get(identity(field))?.value??field.original})),
      reason:entry?entry.reason:(sourceKey?'This source is unavailable. Its edits are retained but cannot be applied.':'This is a planning item. It does not create website content.'),
      missing:data?records(mode).filter(row=>!data.fields.has(identity(row))).length:0};
  }
  function merge(mode,edits) {
    const ids=new Set(edits.map(identity)),next=records(mode).filter(row=>!ids.has(identity(row)));
    for(const field of edits)if(field.value!==field.original)next.push({sourceKey:field.sourceKey,field:field.field,fingerprint:field.fingerprint,value:field.value});
    const normalized=normalize(next);
    return normalized.length===next.length && next.every(row=>row.value.length<=MAX_CHARS)?normalized:null;
  }
  function applyText(html,mode) {
    const edits=records(mode);if(inspecting || !edits.length)return html;
    const data=scan(html,mode);
    let applied=false;
    for(const row of edits){const field=data.fields.get(identity(row));if(field){field.write(row.value);applied=true;}}
    if(!applied)return html;
    const result='<!doctype html>\n'+data.doc.documentElement.outerHTML;
    // A parsed document is mutable; never reuse it after applying overrides.
    caches[mode]=null;return result;
  }
  DSStudio.websiteContent={normalize,describe,merge,apply:applyText,MAX_FIELDS,MAX_CHARS,MAX_TOTAL};
})();
