'use strict';
/* Shared property actions. Feature-owned forms retain their validation and saves. */
(() => {
  function preview(source) {
    const stage=DSStudio.stages.find(item=>item.lesson===source.closest('#main > .studio-section')?.id) || DSStudio.stages[DSStudio.activeStage];
    if(stage)window.dssShowWizardStep(stage.index,false);
    const result=document.getElementById('studio-section-4'),keep=new Set([result]);
    if(stage)keep.add(document.getElementById(stage.lesson));
    for(let node=source;node;node=node.parentElement)if(node.tagName==='DETAILS')keep.add(node);
    for(const section of document.querySelectorAll('#main > .studio-section, #palette-workspace details, #typography-workspace details, #button-workspace details, #spacing-workspace details'))section.open=keep.has(section);
    result.open=true;DSStudio.views.flush();
    document.getElementById('previewShell').focus({preventScroll:true});
    const height=document.querySelector('.topbar').getBoundingClientRect().height;
    window.scrollTo({top:window.scrollY+result.getBoundingClientRect().top-height-8,behavior:'instant'});
  }
  function create({parent,id,save,discard,saveButton,discardButton,previewOnly=false}) {
    const reuse=saveButton?.parentElement===parent && discardButton?.parentElement===parent;
    const bar=reuse?parent:document.createElement('div');bar.classList.add('button-row','property-actions');
    const extras=reuse?[...bar.children].filter(node=>node!==saveButton && node!==discardButton):[];
    if(id)bar.dataset.propertyActions=id;
    function action(label,handler,existing) {
      const button=existing||document.createElement('button');
      if(!existing)button.type='button';
      button.textContent=label;
      if(handler)button.addEventListener('click',handler);
      bar.append(button);return button;
    }
    const commit=previewOnly?null:action('Save',save,saveButton),cancel=previewOnly?null:action('Discard',discard,discardButton);
    const show=action('Responsive page preview',()=>preview(show));show.className='ghost';show.dataset.propertyPreview='';
    bar.append(...extras);
    if(cancel)cancel.classList.add('ghost');if(!reuse)parent.append(bar);
    return {bar,save:commit,discard:cancel,preview:show};
  }
  DSStudio.propertyActions=Object.freeze({create,preview});
})();
