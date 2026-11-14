"""Focused view lifecycle/scheduling checks using an isolated Chrome profile.

Run: python scripts/view_updates_review.py.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8">
<title>View updates review</title><iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload = async () => {
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const wait=()=>new Promise(resolve=>setTimeout(resolve,100));
  const test=(name,fn)=>{
    try {if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
  };
  try {
    evaluate('resetStudio()');await wait();
    w.dssShowWizardStep(5,false);w.DSStudio.typographyWorkspace.show('context',false);
    d.getElementById('type-context-choice').value='button';
    d.getElementById('type-context-choice').dispatchEvent(new w.Event('change',{bubbles:true}));
    d.getElementById('type-context-choice').focus();
    await wait();
    const weight=d.getElementById('bdWeight');weight.value='700';
    weight.dispatchEvent(new w.Event('input',{bubbles:true}));await wait();
    test('Typography component context refreshes after the live preview changes',()=>{
      const frame=d.getElementById('previewPage'),button=frame.contentDocument.querySelector('.ds-button');
      const actual=frame.contentWindow.getComputedStyle(button).fontWeight;
      const specimen=w.getComputedStyle(d.getElementById('type-specimen-text')).fontWeight;
      if(actual!=='700'||specimen!==actual)throw Error(JSON.stringify({actual,specimen}));
      return true;
    });
    test('Background component refresh preserves the active Typography lesson and focus',()=>
      w.DSStudio.activeStage===5 && d.activeElement===d.getElementById('type-context-choice'));
    const views=w.DSStudio.views,emit=event=>w.DSStudio.emit(event);
    views.flush();
    {
      let runs=0;
      const task=views.subscribe({id:'test-coalesce',events:['test:a','test:b'],run:()=>runs++});
      for(let index=0;index<20;index++){emit('test:a');emit('test:b');task.schedule();}
      test('Background scheduling leaves synchronous callers uninterrupted',()=>runs===0);
      await Promise.resolve();
      test('Repeated dependent events coalesce to one update per turn',()=>runs===1);
      task.dispose();
    }
    {
      const order=[];
      const lesson=views.subscribe({id:'test-lesson',phase:'lesson',events:['test:order'],run:()=>order.push('lesson')});
      const preview=views.subscribe({id:'test-preview',phase:'preview',events:['test:order'],run:()=>order.push('preview')});
      emit('test:order');await Promise.resolve();
      test('Preview phase precedes lessons regardless of registration order',()=>order.join(',')==='preview,lesson');
      lesson.dispose();preview.dispose();
    }
    {
      const order=[];
      const lesson=views.subscribe({id:'test-dependent-lesson',phase:'lesson',events:['test:ready'],run:()=>order.push('lesson')});
      const preview=views.subscribe({id:'test-dependent-preview',phase:'preview',run:()=>{order.push('preview');emit('test:ready');}});
      preview.schedule();await Promise.resolve();
      test('A preview can invalidate its dependent lesson within the same flush',()=>order.join(',')==='preview,lesson');
      lesson.dispose();preview.dispose();
    }
    {
      const order=[];
      const preview=views.subscribe({id:'test-next-preview',phase:'preview',run:()=>order.push('preview')});
      const lesson=views.subscribe({id:'test-next-lesson',phase:'lesson',run:()=>{order.push('lesson');preview.schedule();}});
      lesson.schedule();await Promise.resolve();
      test('An earlier phase invalidated by a lesson waits until the next flush',()=>order.join(',')==='lesson');
      await Promise.resolve();
      test('Deferred earlier-phase invalidation is retained',()=>order.join(',')==='lesson,preview');
      lesson.dispose();preview.dispose();
    }
    {
      let oldRuns=0,newRuns=0;
      const old=views.subscribe({id:'test-dispose',events:['test:dispose'],run:()=>oldRuns++});
      old.schedule();old.dispose();
      const current=views.subscribe({id:'test-dispose',events:['test:dispose'],run:()=>newRuns++});
      old.dispose();old.schedule();emit('test:dispose');await Promise.resolve();
      test('Disposal cancels pending work and stale handles cannot remove a reused id',()=>oldRuns===0&&newRuns===1);
      current.dispose();
    }
    {
      const prior=w.console.error,logged=[];let completed=false;
      const broken=views.subscribe({id:'test-error',phase:'preview',run:()=>{throw Error('Expected scheduler test failure');}});
      const healthy=views.subscribe({id:'test-after-error',phase:'lesson',run:()=>{completed=true;}});
      try {
        w.console.error=(...args)=>{
          if(args[0]==='DSStudio view "test-error" failed')logged.push(args[0]);else prior.apply(w.console,args);
        };
        broken.schedule();healthy.schedule();await Promise.resolve();
        test('One failed view is reported without blocking other views',()=>logged.length===1&&completed);
      } finally {w.console.error=prior;broken.dispose();healthy.dispose();}
    }
    {
      const first=views.subscribe({id:'test-unique',run:()=>{}});let rejected=0;
      try {
        for(const config of [{id:'test-unique',run:()=>{}},{id:'bad-phase',phase:'unknown',run:()=>{}},{id:'missing-run'}]){
          try{views.subscribe(config);}catch{rejected++;}
        }
        test('Invalid and duplicate view registrations are rejected',()=>rejected===3);
      } finally {first.dispose();}
    }
    {
      const references=evaluate('[apply,renderCode,renderType]');let runs=0,base=0;
      const task=views.subscribe({id:'test-project-view',events:['foundation:updated','type:updated','output:updated'],run:()=>{
        runs++;base=JSON.parse(evaluate('projectJson()')).base;
      }});
      for(const value of [18,19,20]){
        const input=d.getElementById('jBase');input.value=value;input.dispatchEvent(new w.Event('input',{bubbles:true}));
      }
      test('Model changes and exports stay synchronous while views are pending',()=>runs===0&&JSON.parse(evaluate('projectJson()')).base===20&&evaluate('cssExport()').includes('--font-size-base: 20px'));
      await Promise.resolve();
      test('Foundation, typography and output notifications produce one latest-value update',()=>runs===1&&base===20);
      test('View updates leave the shared lifecycle functions intact',()=>evaluate('[apply,renderCode,renderType]').every((fn,index)=>fn===references[index]));
      runs=0;
      evaluate('state.base=22;apply();resetStudio()');await Promise.resolve();
      test('Pending work reads the replacement project rather than stale captured state',()=>runs===1&&base===16&&d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent.includes('--font-size-base: 16px'));
      task.dispose();
    }
    await wait();
    test('No view-update JavaScript errors',()=>!w.__reviewErrors.length);
  } catch(error){results.push({name:'View update harness completed',pass:false,error:String(error.stack||error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
