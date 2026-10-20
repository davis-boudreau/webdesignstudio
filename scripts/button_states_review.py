"""Optional Chrome checks for actual reduced-motion and forced-colour modes.

Run: python scripts/button_states_review.py. Uses the existing isolated-profile
runner and local server; no additional dependencies or live network services.
"""
import browser_review as review

HARNESS = r'''<!doctype html>
<iframe id="app" src="/index.html" style="width:1280px;height:1000px"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[];
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error)});}
  };
  const wait=()=>new Promise(resolve=>setTimeout(resolve,100));
  const mode=MODE;
  try{
    w.dssRevealSection('previewPage',false);
    w.dssRevealSection('bdSingle',false);
    await wait();
    test(mode+' media preference is active',()=>w.matchMedia(mode==='reduce'?'(prefers-reduced-motion: reduce)':'(forced-colors: active)').matches);
    w.dssSelectButtonState('primary','loading');await wait();
    const lab=d.querySelector('#bdSingle .bd-button');
    const pd=d.getElementById('previewPage').contentDocument,pw=pd.defaultView;
    test(mode+' busy text and progress remain visible',()=>w.getComputedStyle(lab).opacity==='1' && w.getComputedStyle(lab,'::after').content==='""' && lab.textContent==='Processing\u2026');
    if(mode==='reduce'){
      test('Reduced motion stops the studio progress animation',()=>w.getComputedStyle(lab,'::after').animationName==='none');
      test('Reduced motion stops the generated page progress animation',()=>pw.getComputedStyle(pd.querySelector('.sample-selected-action'),'::after').animationName==='none');
    }else{
      const pressed=d.querySelector('#bdMatrix [data-sim="active"]');
      test('Forced colours replace the inset shadow with an inside outline',()=>w.getComputedStyle(pressed).outlineWidth==='2px' && w.getComputedStyle(pressed).outlineOffset==='-4px');
      w.dssSelectButtonState('primary','active');await wait();
      const action=pd.querySelector('.sample-selected-action');
      test('Forced-colour generated state simulations retain a pressed cue',()=>pw.getComputedStyle(action).outlineWidth==='2px' && pw.getComputedStyle(action).outlineOffset==='-4px');
      action.focus();
      test('Pressed styling preserves the actual keyboard focus outline',()=>action.matches(':focus-visible') && pw.getComputedStyle(action).outlineWidth==='3px' && pw.getComputedStyle(action).outlineOffset==='3px');
      w.dssSelectButtonState('primary','selected');await wait();
      test('Forced colours retain the selected checkmark',()=>pw.getComputedStyle(pd.querySelector('.sample-selected-action'),'::before').borderBottomStyle==='solid');
    }
    test(mode+' has no runtime errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Media review completes',pass:false,error:String(error.stack||error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};</script>'''


def main():
    original_run = review.subprocess.run
    original_harness = review.HARNESS
    status = 0
    try:
        for mode, flag in [('reduce', '--force-prefers-reduced-motion'),
                           ('forced', '--force-high-contrast')]:
            review.HARNESS = HARNESS.replace('MODE', repr(mode))

            def run_with_flags(command, flag=flag, **kwargs):
                return original_run([command[0], flag, *command[1:]], **kwargs)

            review.subprocess.run = run_with_flags
            status = max(status, review.main())
    finally:
        review.subprocess.run = original_run
        review.HARNESS = original_harness
    return status


if __name__ == '__main__':
    raise SystemExit(main())
