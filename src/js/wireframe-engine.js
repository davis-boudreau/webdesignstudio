'use strict';
/* Read-only mirror of the generated website. Legacy layout data is validated
   for project compatibility but never changes the mirrored HTML or CSS. */
(() => {
  const MAX_BLOCKS=1000,MAX_CHARS=80000;
  const layouts=['inherit','stack','split','grid'],emphases=['normal','primary','supporting'];
  const validId=id=>typeof id==='string' && /^content-[a-z0-9-]{1,80}$/.test(id);
  const defaults=()=>({scope:'site',content:'current',layout:'inherit',blocks:[]});
  function normalize(value) {
    const result=defaults();if(!value || typeof value!=='object' || Array.isArray(value))return result;
    if(value.scope==='site' || validId(value.scope))result.scope=value.scope;
    if(value.content==='proposed')result.content='proposed';
    if(layouts.includes(value.layout))result.layout=value.layout;
    const seen=new Set();let size=2;
    for(const item of (Array.isArray(value.blocks)?value.blocks:[]).slice(0,MAX_BLOCKS)) {
      if(!item || !validId(item.id) || seen.has(item.id))continue;
      const row={id:item.id,layout:layouts.includes(item.layout)?item.layout:'inherit',emphasis:emphases.includes(item.emphasis)?item.emphasis:'normal'};
      if(row.layout==='inherit' && row.emphasis==='normal')continue;
      size+=JSON.stringify(row).length+1;if(size>MAX_CHARS)break;
      seen.add(row.id);result.blocks.push(row);
    }
    return result;
  }
  const mode=()=>state.sampleMode==='basic'?'basic':'advanced';
  const outlineCss=()=>`/* Preserve website colours and backgrounds; annotate layout without changing boxes. */
html { --wf-ink: var(--text); --wf-frame: var(--control-border); --wf-item: var(--control-border); }
*,*::before,*::after { box-shadow: none !important; text-shadow: none !important; animation: none !important; transition: none !important; }
/* Outlines paint inside the original box; no borders, padding or positioning change. */
[data-wf-container="object"]:not(:focus-visible), [data-wf-container="item"] { outline: 1px solid var(--wf-item); outline-offset: -1px; }
[data-wf-container]::before, [data-wf-container]::after { outline: 1px solid var(--wf-item); outline-offset: -1px; }
[data-wf-container="layout"] { outline: 2px dotted var(--wf-frame); outline-offset: -2px; }
[data-wf-container="content"] { outline: 2px dashed var(--wf-frame); outline-offset: -4px; }
[data-wf-container="region"] { outline: 2px solid var(--wf-ink); outline-offset: -2px; }
`;
  const lowFidelityCss=()=>`/* Low Fidelity: neutral paint over the same responsive website boxes. */
html { --text: #222 !important; --control-border: #777 !important; --focus: #222 !important; --button-focus: #222 !important; color-scheme: light !important; }
html, body { background: #fff !important; }
*, *::before, *::after { color: #222 !important; background-color: transparent !important; background-image: none !important; border-color: #888 !important; accent-color: #666 !important; caret-color: #222 !important; }
button, .button, .ds-button, [role="button"] { background-color: #666 !important; color: #fff !important; }
button *, .button *, .ds-button *, [role="button"] *, button::before, button::after, .ds-button::before, .ds-button::after { color: #fff !important; }
img, svg, video, canvas { filter: grayscale(1) !important; }
`;
  function render() {
    return '<p class="wireframe-source-note">Compare Low Fidelity and High Fidelity views of the '+(mode()==='basic'?'Basic':'Advanced')+' website in the Studio Wireframe workspace. Both are read-only views of the same HTML and responsive layout.</p>';
  }
  function markContainers(doc,css) {
    const structural='header,main,footer,section,article,aside,figure,nav,form,fieldset,table,div,ul,ol,dl,li,dd,details';
    const rank={object:1,item:2,layout:3,content:4,region:5};
    const mark=(node,kind)=>{if((rank[node.getAttribute('data-wf-container')]||0)<rank[kind])node.setAttribute('data-wf-container',kind);};
    doc.querySelectorAll('body > header,main,body > footer,main > section').forEach(node=>mark(node,'region'));
    doc.querySelectorAll('.container').forEach(node=>mark(node,'content'));
    // Read the locally generated CSS, including nested responsive rules. Mark
    // Grid/Flex containers even when another breakpoint temporarily stacks them.
    // Selectors are authored CSS, never imported strings or content IDs.
    const sheet=new CSSStyleSheet();sheet.replaceSync(css);
    function visit(rules) {
      for(const rule of rules) {
        if(rule.selectorText && /^(inline-)?(grid|flex)$/.test(rule.style?.display||'')) {
          for(const node of doc.querySelectorAll(rule.selectorText)) {
            if(!node.matches(structural) || node.closest('[aria-hidden="true"],svg'))continue;
            mark(node,'layout');node.setAttribute('data-wf-layout',rule.style.display);
            for(const child of node.children)if(child.matches(structural))mark(child,'item');
          }
        }
        if(rule.cssRules)visit(rule.cssRules);
      }
    }
    visit(sheet.cssRules);
    // Reveal nested normal-flow groups as well as Grid/Flex wrappers.
    const nested='section,article,aside,figure,nav,form,fieldset,table,details,li,dd';
    doc.querySelectorAll(nested).forEach(node=>{if(!node.closest('[aria-hidden="true"],svg'))mark(node,'item');});
    doc.querySelectorAll('div').forEach(node=>{
      if(node.closest('[aria-hidden="true"],svg'))return;
      if([...node.children].some(child=>child.matches('h1,h2,h3,h4,h5,h6,p,div,ul,ol,dl,section,article,aside,figure,form,fieldset,details,table')))mark(node,'item');
    });
    // Every rendered HTML object gets a boundary, including inline text, controls
    // and decorative tracks. Treat each SVG illustration/icon as one object;
    // outlining its internal paths would obscure the drawing. Hidden content
    // keeps the source website's visibility and responsive/disclosure behavior.
    for(const node of doc.body.querySelectorAll('*')){
      if(node.matches('script,style,link,meta,title,base,template,source,track,br,wbr'))continue;
      if(node.namespaceURI==='http://www.w3.org/2000/svg' && (node.localName!=='svg' || node.parentElement?.closest('svg')))continue;
      mark(node,'object');
    }
    for(const node of doc.querySelectorAll('[data-wf-container]'))if(!node.hasAttribute('title')){
      const identity=node.tagName.toLowerCase()+(node.id?'#'+node.id:'')+[...node.classList].map(name=>'.'+name).join('');
      node.setAttribute('title',identity+' - '+(node.dataset.wfLayout?node.dataset.wfLayout+' layout':node.dataset.wfContainer==='object'?'page object':node.dataset.wfContainer+' container'));
    }
  }
  function createDocument({preview=false,fidelity='high'}={}) {
    const doc=new DOMParser().parseFromString(htmlExport(),'text/html');
    // Only the locally generated, escaped website is parsed. Imported settings
    // are never parsed as markup, selectors, URLs or styles.
    doc.querySelectorAll('script,iframe,object,embed,base').forEach(node=>node.remove());
    doc.querySelectorAll('link[rel="stylesheet"][href="tokens.css"]').forEach(node=>node.remove());
    if(preview)doc.querySelectorAll('link').forEach(node=>node.remove());
    const css=cssExport();markContainers(doc,css);
    doc.documentElement.dataset.wfFidelity=fidelity==='low'?'low':'high';
    const source=doc.createElement('style');source.id='wf-source-styles';source.textContent=css+DSStudio.fonts.previewCss();
    const paint=doc.createElement('style');paint.id='wf-outline-styles';paint.textContent=outlineCss();doc.head.append(source);
    if(fidelity==='low'){const neutral=doc.createElement('style');neutral.id='wf-low-fidelity-styles';neutral.textContent=lowFidelityCss();doc.head.append(neutral);}
    doc.head.append(paint);
    for(const control of doc.querySelectorAll('input,textarea,select,button'))control.inert=true;
    for(const form of doc.querySelectorAll('form')){form.removeAttribute('action');form.removeAttribute('target');}
    for(const anchor of doc.querySelectorAll('a[href]'))if(!anchor.getAttribute('href').startsWith('#'))anchor.removeAttribute('href');
    return doc;
  }
  function documentHtml({fidelity='high'}={}) {
    const doc=createDocument({fidelity});doc.title=state.project+' - '+(mode()==='basic'?'Basic':'Advanced')+' '+(fidelity==='low'?'Low Fidelity':'High Fidelity')+' wireframe';
    return '<!doctype html>\n'+doc.documentElement.outerHTML;
  }
  // Old bounded layout data remains round-trippable, but has no effect on the
  // read-only mirror. No separate wireframe content or layout model is applied.
  DSStudio.wireframeEngine={defaults,normalize,render,css:()=>'',outlineCss,lowFidelityCss,createDocument,documentHtml,MAX_BLOCKS,MAX_CHARS};
})();
