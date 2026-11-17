'use strict';
/* Independent teaching markup, the website's actual CSS, and no iframe scripts. */
(() => {
  function guideColours(doc){const root=doc?.documentElement;if(!root)return;const colours=getComputedStyle(document.documentElement);for(const name of ['text','surface','control-border','focus'])root.style.setProperty('--learning-ui-'+name,colours.getPropertyValue('--studio-'+name));}
  function mount({id,title,element,parent,layout='',ready=()=>{}}){
    const frame=document.createElement('iframe');frame.id=id;frame.title=title;frame.className='learning-preview-frame';frame.setAttribute('sandbox','allow-same-origin');
    frame.srcdoc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style id="learning-website-css"></style><style id="learning-layout-css"></style></head><body></body></html>';
    parent.append(frame);
    let pending=null,options={},key='',observer,sizing=0;
    function interfaceColours(){guideColours(frame.contentDocument);}
    const interfaceObserver=new MutationObserver(interfaceColours);interfaceObserver.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
    function size(){
      if(sizing)return;
      sizing=requestAnimationFrame(()=>{sizing=0;const doc=frame.contentDocument;if(!doc?.body)return;const style=frame.contentWindow.getComputedStyle(doc.body),height=Math.min(2000,Math.max(96,Math.ceil(doc.body.getBoundingClientRect().height+(parseFloat(style.marginTop)||0)+(parseFloat(style.marginBottom)||0))))+'px';if(frame.style.height!==height)frame.style.height=height;});
    }
    function render(snapshot,fontOptions={}){
      pending=snapshot;options=fontOptions;const doc=frame.contentDocument;if(!doc?.getElementById('learning-website-css'))return;
      if(element.ownerDocument!==doc){if(element.tagName==='BODY')doc.body.replaceWith(doc.adoptNode(element));else doc.body.append(doc.adoptNode(element));}
      const next=JSON.stringify(snapshot);
      if(next!==key){key=next;doc.getElementById('learning-website-css').textContent=DSStudio.exports.css(snapshot.state.sampleMode,snapshot);}
      const fallback=fontOptions.fallback??DSStudio.fonts.showFallback,fonts=DSStudio.fonts.resolve(true,snapshot.state);
      doc.getElementById('learning-layout-css').textContent=layout+'\n[data-learning-selected] { outline: 3px solid var(--learning-ui-focus); outline-offset: -3px; }'+(fallback?'\n/* Optional fallback comparison; website CSS above remains unchanged. */\n:root { --font-body: '+fonts.body+'; --font-heading: '+fonts.heading+'; }':'');
      doc.documentElement.dataset.theme=snapshot.state.theme;doc.body.classList.toggle('sample-home',snapshot.state.sampleMode==='advanced');
      interfaceColours();
      DSStudio.fonts.syncLearning(doc,snapshot.state,kind=>{size();fontOptions.report?.(kind);},fallback,true);size();
    }
    frame.addEventListener('load',()=>{if(!frame.contentDocument?.getElementById('learning-website-css'))return;key='';if(pending)render(pending,options);observer?.disconnect();observer=new ResizeObserver(size);observer.observe(frame.contentDocument.body);ready();});
    function clearFonts(){if(frame.contentDocument)DSStudio.fonts.clearLearning(frame.contentDocument);key='';}
    DSStudio.on('project:install',()=>{clearFonts();pending=null;});
    document.getElementById('fontRetry')?.addEventListener('click',()=>{clearFonts();if(pending)render(pending,options);});
    return {frame,render,size,get document(){return frame.contentDocument;}};
  }
  function bindTheme(select,updated=()=>{}){
    function updateTheme(){const control=document.getElementById('jTheme');if(state.theme===select.value)return;control.value=select.value;control.dispatchEvent(new Event('input',{bubbles:true}));updated();}
    select.addEventListener('input',updateTheme);select.addEventListener('change',updateTheme);return select;
  }
  function theme(id,parent){
    const field=document.createElement('div'),label=document.createElement('label'),select=document.createElement('select'),help=document.createElement('p');field.className='field';select.id=id;label.htmlFor=id;label.textContent='Website theme';select.add(new Option('Light','light'));select.add(new Option('Dark','dark'));help.id=id+'-help';help.className='help';help.textContent='Changes the shared website theme. Proposed edits stay in place; Studio appearance is separate.';select.setAttribute('aria-describedby',help.id);field.append(label,select,help);parent.append(field);
    // Commit before a workspace's bubbling input listener refreshes the selector.
    return bindTheme(select);
  }
  DSStudio.learningPreviews=Object.freeze({mount,theme,bindTheme,guideColours});
})();
