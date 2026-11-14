"""Focused project-model regressions using the existing isolated Chrome runner.

Run: python scripts/project_model_review.py. No user profile or storage is used.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8">
<title>Project model review</title><iframe id="app" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload = () => {
  const w = app.contentWindow, results = [], evaluate = code => w.eval(code);
  const test = (name, fn) => {
    try { if (!fn()) throw Error('Assertion failed'); results.push({name,pass:true}); }
    catch(error) { results.push({name,pass:false,error:String(error.stack || error)}); }
  };
  try {
  evaluate(`
    importConfig({base:16,advanced:{measure:42},buttonDesign:{padX:10}});
    window.projectObservations=[];
    window.projectPriorRender=renderCode;
    renderCode=function(){projectObservations.push(JSON.parse(projectJson()));projectPriorRender();};
    importConfig({theme:'dark',base:21,headingTracking:.04,advanced:{measure:81},buttonDesign:{padX:33}});
  `);
  test('Every import render observes the complete foundation, advanced and button model', () =>
    w.projectObservations.length>0 && w.projectObservations.every(project =>
      project.theme==='dark' && project.base===21 && project.advanced.measure===81 &&
      project.advanced.tracking===4 && project.buttonDesign.padX===33));
  test('Rendering preserves the canonical button settings object and project values', () => evaluate(`
    (()=>{const buttons=state.buttonDesign,before=projectJson();apply();
      return state.buttonDesign===buttons && projectJson()===before;})()
  `));
  evaluate('projectObservations=[];resetStudio()');
  test('Every reset render observes complete defaults', () =>
    w.projectObservations.length>0 && w.projectObservations.every(project =>
      project.theme==='light' && project.base===16 && project.sampleMode==='basic' &&
      project.advanced.measure===65 && project.buttonDesign.padX===16));
  evaluate('renderCode=projectPriorRender');
  test('New and reset projects omit optional semantic, opacity and padding override maps', () => evaluate(`
    (()=>{
      const fresh=DSStudio.project.defaults().state;
      return ['semanticOverrides','backgroundOpacity','regionPadding'].every(key=>
        !Object.hasOwn(state,key) && !Object.hasOwn(fresh,key));
    })()
  `));
  test('Validation and serialization run without reading or writing the DOM', () => evaluate(`
    (()=>{
      const methods=['getElementById','querySelector','querySelectorAll','createElement'];
      const prior=methods.map(key=>document[key]);
      const before=projectJson(),identity=state;
      try {
        for(const key of methods)document[key]=()=>{throw Error('Codec accessed the DOM');};
        const next=DSStudio.project.normalize({base:20,advanced:{measure:73},buttonDesign:{padX:31}});
        const json=DSStudio.project.serialize(next.state,next.clampConfig);
        const fresh=DSStudio.project.defaults();
        return JSON.parse(json).advanced.measure===73 && next.state.buttonDesign.padX===31 &&
          fresh.state.sampleMode==='basic' && state===identity && projectJson()===before;
      } finally {methods.forEach((key,index)=>document[key]=prior[index]);}
    })()
  `));
  test('Legacy sample mode and hundredths tracking migrate without changing input', () => evaluate(`
    (()=>{
      const input=Object.freeze({advanced:Object.freeze({tracking:3,measure:71})});
      const next=DSStudio.project.normalize(input);
      return next.state.sampleMode==='advanced' && next.state.headingTracking===.03 &&
        next.state.advanced.tracking===3 && !Object.hasOwn(input,'sampleMode') &&
        DSStudio.project.normalize({sampleMode:'invalid'}).state.sampleMode==='basic';
    })()
  `));
  test('Advanced rules match the authored control ranges and enum choices', () => evaluate(`
    Object.entries(advMap).every(([id,key])=>{
      const el=document.getElementById(id),rule=DSStudio.project.advancedFields[key];
      if(rule.values)return JSON.stringify([...el.options].map(option=>
        typeof rule.values[0]==='number'?Number(option.value):option.value))===JSON.stringify(rule.values);
      return rule.boolean?el.type==='checkbox':Number(el.min)===rule.min && Number(el.max)===rule.max;
    })
  `));
  test('Malformed values stay bounded and unknown keys cannot become settings', () => evaluate(`
    (()=>{
      const input={base:999,headingTracking:.02,
        advanced:{measure:-99,weight:'800',underline:'false',colors:{danger:'<svg>'},['__proto__']:{polluted:true}},
        clampConfig:{mobileFactor:999},semanticOverrides:{dark:{text:'#123456',unknown:'#ffffff'}},
        buttonDesign:{variant:'__proto__',padX:'999',focus:'javascript:alert(1)'}};
      const next=DSStudio.project.normalize(JSON.parse(JSON.stringify(input)));
      return next.state.base===22 && next.state.advanced.measure===40 && next.state.advanced.weight===700 &&
        next.state.advanced.underline===true && next.state.advanced.colors.danger==='#B91C1C' &&
        next.clampConfig.mobileFactor===1 && next.state.buttonDesign.variant==='primary' &&
        next.state.buttonDesign.padX===36 && next.state.buttonDesign.focus==='#B86C20' &&
        next.state.semanticOverrides.dark.text==='#123456' &&
        !Object.hasOwn(next.state.semanticOverrides.dark,'unknown') && !({}).polluted;
    })()
  `));
  test('Snapshots and separate default projects share no mutable model objects', () => evaluate(`
    (()=>{
      const first=DSStudio.project.defaults(),second=DSStudio.project.defaults();
      first.state.advanced.colors.focus='#123456';first.state.buttonDesign.sources.primary='custom';
      first.state.designProcess.pageLinks.basic.home='home';
      const before=projectJson(),copy=projectSnapshot();
      copy.advanced.colors.focus='#abcdef';copy.buttonDesign.padX=99;copy.clampConfig.minWidth=999;
      return second.state.advanced.colors.focus==='#9D5700' &&
        second.state.buttonDesign.sources.primary==='primary' && !second.state.designProcess.pageLinks.basic.home &&
        projectJson()===before;
    })()
  `));
  test('Rejected root configurations preserve all active model references', () => evaluate(`
    [null,[],false,'invalid'].every(value=>{
      const before=projectJson(),identity=state,clampIdentity=clampConfig;
      try {importConfig(value);return false;}catch(error) {
        return projectJson()===before && state===identity && clampConfig===clampIdentity && !DSStudio.isReplacingProject();
      }
    })
  `));
  test('A failed feature normalizer cannot partially replace the project', () => evaluate(`
    (()=>{
      const before=projectJson(),identity=state,clampIdentity=clampConfig,normalize=DSStudio.responsive.normalize;
      try {
        DSStudio.responsive.normalize=()=>{throw Error('Test normalization failure');};
        try {importConfig({base:22,advanced:{measure:83}});return false;}
        catch(error){return projectJson()===before && state===identity && clampConfig===clampIdentity;}
      } finally {DSStudio.responsive.normalize=normalize;}
    })()
  `));
  test('Current project JSON round trips without losing any settings', () => evaluate(`
    (()=>{
      importConfig({theme:'dark',headingTracking:.03,advanced:{measure:78},buttonDesign:{padX:31},
        semanticOverrides:{dark:{text:'#abcdef'}},regionPadding:{header:{top:12}},
        backgroundOpacity:{light:{footer:70}}});
      const before=projectJson();importConfig(JSON.parse(before));return projectJson()===before;
    })()
  `));
  test('Replacement observers cannot autosave over the active saved project', () => evaluate(`
    (()=>{
      document.getElementById('jSaveLocal').click();
      const before=localStorage.getItem('dss-v27-projects');let guarded=false;
      const unsubscribe=DSStudio.on('project:sync',()=>{
        guarded=DSStudio.isReplacingProject();window.dssAutosave();
      });
      try {
        importConfig({project:'Replacement',advanced:{measure:80},buttonDesign:{padX:30}});
        if(!guarded || localStorage.getItem('dss-v27-projects')!==before || DSStudio.isReplacingProject())return false;
        window.dssAutosave();
        const saved=Object.values(JSON.parse(localStorage.getItem('dss-v27-projects')))[0].data;
        return saved.project==='Replacement' && saved.advanced.measure===80 && saved.buttonDesign.padX===30;
      } finally {unsubscribe();}
    })()
  `));
  test('No project-model JavaScript errors', () => !w.__reviewErrors.length);
  } catch(error) { results.push({name:'Project model harness completed',pass:false,error:String(error.stack || error)}); }
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
