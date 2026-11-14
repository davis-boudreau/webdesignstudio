"""Export assembly regressions using the existing isolated Chrome runner.

Run: python scripts/export_pipeline_review.py.
Use --capture only when intentionally accepting reviewed export changes; it
replaces scripts/fixtures/export_baseline.json with hashes of the current output.
"""
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path

from browser_runner import run_review


BASELINE = Path(__file__).resolve().parent / 'fixtures' / 'export_baseline.json'
HARNESS = r'''<!doctype html><meta charset="utf-8">
<title>Export pipeline review</title><iframe id="app" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,results=[],evaluate=code=>w.eval(code),expected=__EXPECTED__,capture=__CAPTURE__;
  const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}};
  try {
    const entryPoints=evaluate('[cssExport,htmlExport]');
    const outputs=[];
    for(const kind of ['defaults','custom','google','content'])for(const mode of ['basic','advanced'])for(const theme of ['light','dark']){
      const settings={sampleMode:mode,theme};
      if(kind==='custom')Object.assign(settings,{
        project:'Studio <Audit> & "Test" */',method:'mix',primary:'#123456',secondary:'#654321',accent:'#abcdef',
        font:"Georgia, 'Times New Roman', serif",base:19,ratio:1.333,leading:1.8,headingLeading:1.4,
        headingTracking:.035,bodyTracking:.012,spacing:7,radius:24,
        advanced:{weight:800,measure:78,height:60,shadow:'strong',columns:280,gap:12,align:'center',opacity:75,
          underline:false,reduce:true,motion:325,colors:{success:'#116633',warning:'#996600',danger:'#991122',focus:'#663399'}},
        buttonDesign:{variant:'outline',size:'lg',padX:25,padY:14,radius:18,weight:700,focus:'#9d5700',focusWidth:5,
          mobileFull:true,sources:{primary:'custom'},custom:{primary:'#335577'},overrides:{outline:{text:'#552244',hover:'#eeddee'}}},
        clampConfig:{minWidth:480,maxWidth:1450,mobileFactor:.73},
        responsiveDesign:{stack:820,wide:1200,maxWidth:1360,gutter:18,wideGutter:44},
        semanticOverrides:{light:{'control-border':'#556677'},dark:{'main-background':'#123456'}},
        backgroundOpacity:{light:{header:55},dark:{footer:25}},
        regionPadding:{header:{top:12},main:{right:22},footer:{bottom:8}},
        designProcess:{goal:'A useful visitor task',audience:'Students & tutors',layout:'stack',showPlanned:true,
          pages:'Home\nHome > Introduction\nResources\nResources > Lessons',prototypeTask:'Find a lesson'}
      });
      w.importConfig(settings);
      if(kind==='content'){
        const service=w.DSStudio.websiteContent,field=service.describe('id:hero-title',mode).fields.find(row=>row.field.startsWith('text:'));
        if(!field)throw Error('Missing authored hero text fixture for '+mode);
        const edits=service.merge(mode,[{...field,value:'Safe <img src=x onerror=alert(1)> & Heading'}]);
        evaluate('state.designProcess.websiteContent['+JSON.stringify(mode)+']='+JSON.stringify(edits));
      }
      // Generator-only Google cases never install font links into a live document.
      const priorFonts=evaluate('state.fontSettings');
      try {
        if(kind==='google')evaluate("state.fontSettings=DSStudio.fonts.normalize({source:'google',body:'inter',heading:'literata',weights:[400,600,700,800]})");
        const before=evaluate('projectJson()');
        const css=evaluate('cssExport()'),html=evaluate('htmlExport()'),shared=w.DSStudio.samples.foundationCss();
        test(kind+' '+mode+' '+theme+' exports do not mutate project data',()=>evaluate('projectJson()')===before);
        test(kind+' '+mode+' '+theme+' shared CSS is the exact leading prefix',()=>css.startsWith(shared));
        outputs.push({id:[kind,mode,theme].join('/'),css,html,shared});
      } finally {evaluate('state.fontSettings='+JSON.stringify(priorFonts));}
    }
    evaluate('resetStudio()');
    const hashes={};
    for(const output of outputs){
      hashes[output.id]={};
      for(const language of ['css','html','shared']){
        const bytes=new TextEncoder().encode(output[language]);
        const sha256=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(byte=>byte.toString(16).padStart(2,'0')).join('');
        hashes[output.id][language]={bytes:bytes.length,sha256};
        if(!capture)test(output.id+' '+language+' matches the reviewed export baseline',()=>{
          const baseline=expected[output.id]?.[language];
          if(!baseline || baseline.bytes!==bytes.length || baseline.sha256!==sha256)throw Error(JSON.stringify({expected:baseline,actual:{bytes:bytes.length,sha256}}));
          return true;
        });
      }
    }
    if(capture)test('EXPORT_BASELINE:'+JSON.stringify(hashes),()=>true);
    if(!capture){
      const live=w.DSStudio.exports;
      test('Live CSS stages retain the reviewed foundation-to-layout order',()=>
        live.describe().css.map(row=>row.id).join(',')==='foundation,advanced-components,buttons,state-palettes,planning,sample-layout');
      test('Public export entry points remain stable through project and sample changes',()=>
        evaluate('[cssExport,htmlExport]').every((fn,index)=>fn===entryPoints[index]));
      {
        const pipeline=live.create();let pageCalls=0;
        for(const [id,stage,order,value]of [['layout','layout',0,'L'],['button','components',20,'B'],
          ['planning','planning',0,'P'],['advanced','components',10,'A'],['states','states',0,'S'],['foundation','foundation',0,'F']]){
          pipeline.registerCss({id,stage,order,generate:()=>value});
        }
        pipeline.registerSample('basic',{css:()=>{pageCalls++;return 'BASIC';},html:()=>'<basic>'});
        pipeline.registerSample('advanced',{css:()=>{pageCalls++;return 'ADVANCED';},html:()=>'<advanced>'});
        test('Stage and component order is independent of registration order',()=>pipeline.sharedCss()==='FABSPL');
        test('Shared CSS never invokes or includes either page renderer',()=>pageCalls===0);
        test('Only the selected page follows shared CSS and supplies HTML',()=>
          pipeline.css('basic')==='FABSPLBASIC'&&pipeline.html('basic')==='<basic>'&&
          pipeline.css('advanced')==='FABSPLADVANCED'&&pipeline.html('advanced')==='<advanced>'&&pageCalls===2);
        const remove=pipeline.registerCss({id:'late-component',stage:'components',order:30,generate:()=>'X'});
        test('Later contributors reach both modes without capturing earlier generators',()=>
          pipeline.css('basic')==='FABXSPLBASIC'&&pipeline.css('advanced')==='FABXSPLADVANCED');
        remove();
        const description=pipeline.describe();description.css[0].id='changed';description.samples.length=0;
        test('Pipeline metadata is detached from registrations',()=>pipeline.describe().css[0].id==='foundation'&&pipeline.describe().samples.length===2);
      }
      {
        const pipeline=live.create();
        pipeline.registerCss({id:'zeta',stage:'components',generate:()=>'z'});
        pipeline.registerCss({id:'alpha',stage:'components',generate:()=>'a'});
        test('Equal-order contributors use deterministic id ordering',()=>pipeline.sharedCss()==='az');
        let rejected=0;
        const invalid=[{id:'alpha',stage:'components',generate:()=>''},{id:'unknown',stage:'missing',generate:()=>''},
          {id:'bad-order',stage:'components',order:NaN,generate:()=>''},{id:'bad-generator',stage:'components'}];
        for(const entry of invalid)try{pipeline.registerCss(entry);}catch{rejected++;}
        test('Invalid or duplicate CSS registrations cannot change the pipeline',()=>rejected===4&&pipeline.sharedCss()==='az');
      }
      {
        const pipeline=live.create();
        pipeline.registerSample('fallback',{css:()=>'',html:()=>'<fallback>'});
        test('Bootstrap HTML is available before sample initialization',()=>pipeline.html('basic')==='<fallback>');
        pipeline.registerSample('advanced',{css:()=>'A',html:()=>'<advanced>'});
        test('Advanced retains the historical intermediate startup fallback',()=>pipeline.html('basic')==='<advanced>'&&pipeline.css('basic')==='A');
        pipeline.registerSample('basic',{css:()=>'B',html:()=>'<basic>'});
        let rejected=0;
        for(const id of ['basic','unknown'])try{pipeline.registerSample(id,{css:()=>'',html:()=>''});}catch{rejected++;}
        for(const method of ['css','html'])try{pipeline[method]('unknown');}catch{rejected++;}
        test('Sample registration and dispatch reject duplicates and unknown modes',()=>rejected===4&&pipeline.html('basic')==='<basic>');
      }
      {
        const pipeline=live.create();let fail=true,rejected=false;
        pipeline.registerCss({id:'fallible',stage:'foundation',generate:()=>{if(fail)throw Error('Expected generator failure');return 'OK';}});
        try{pipeline.css('basic');}catch(error){rejected=error.message==='Expected generator failure';}
        fail=false;
        test('Generator failures propagate and do not leave rendering locked',()=>rejected&&pipeline.css('basic')==='OK');
        const remove=pipeline.registerCss({id:'not-text',stage:'components',generate:()=>null});
        rejected=false;try{pipeline.sharedCss();}catch(error){rejected=error.message.includes('must return a string');}remove();
        test('Non-string CSS cannot silently become a partial export',()=>rejected&&pipeline.sharedCss()==='OK');
        let valid=false;pipeline.registerSample('basic',{css:()=>'',html:()=>valid?'<valid>':null});
        rejected=false;try{pipeline.html('basic');}catch(error){rejected=error.message.includes('must return a string');}valid=true;
        test('HTML return values are checked and recover after failure',()=>rejected&&pipeline.html('basic')==='<valid>');
        const recursive=pipeline.registerCss({id:'recursive',stage:'components',generate:()=>pipeline.css('basic')});
        rejected=false;try{pipeline.css('basic');}catch(error){rejected=error.message.includes('Recursive export generation');}recursive();
        test('Recursive contributors fail clearly and recover after removal',()=>rejected&&pipeline.css('basic')==='OK');
      }
      {
        const pipeline=live.create(),remove=pipeline.registerCss({id:'replace',stage:'foundation',generate:()=>'old'});
        remove();pipeline.registerCss({id:'replace',stage:'foundation',generate:()=>'new'});remove();
        const removeSample=pipeline.registerSample('basic',{css:()=>'',html:()=>'<old>'});
        removeSample();pipeline.registerSample('basic',{css:()=>'',html:()=>'<new>'});removeSample();
        test('Stale removal handles cannot delete replacement contributors or samples',()=>
          pipeline.sharedCss()==='new'&&pipeline.html('basic')==='<new>');
      }
    }
    test('No export JavaScript errors',()=>!w.__reviewErrors.length);
  } catch(error){results.push({name:'Export harness completed',pass:false,error:String(error.stack||error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true', help='replace the reviewed baseline with current output hashes')
    args = parser.parse_args()
    expected = {} if args.capture else json.loads(BASELINE.read_text(encoding='utf-8'))['cases']
    harness = HARNESS.replace('__EXPECTED__', json.dumps(expected)).replace('__CAPTURE__', json.dumps(args.capture))
    output = io.StringIO()
    with redirect_stdout(output):
        status = run_review(harness)
    lines = output.getvalue().splitlines()
    prefix = 'PASS: EXPORT_BASELINE:'
    if args.capture and status == 0:
        cases = json.loads(next(line[len(prefix):] for line in lines if line.startswith(prefix)))
        BASELINE.parent.mkdir(exist_ok=True)
        BASELINE.write_text(json.dumps({'format': 1, 'cases': cases}, indent=2) + '\n', encoding='utf-8')
        print(f'Captured {len(cases)} reviewed export cases in {BASELINE.name}')
    print('\n'.join(line for line in lines if not line.startswith(prefix)))
    return status


if __name__ == '__main__':
    raise SystemExit(main())
