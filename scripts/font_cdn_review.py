"""Optional network smoke check: python scripts/font_cdn_review.py.

Uses actual Google CSS2 stylesheets and font downloads in an isolated Chrome
profile. The regular browser_review suite uses deterministic local font fixtures.
"""
import browser_review as review

review.HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Live font review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[];
  const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
  const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}catch(error){results.push({name,pass:false,error:String(error)});}};
  try {
    w.dssRevealSection('previewPage',false); await wait(100);
    w.eval('importConfig({project:"Font classroom",fontSettings:{source:"google",body:"inter",heading:"literata",weights:[400,600,700]}})');
    for(let attempt=0;attempt<140 && d.getElementById('fontLoadStatus').dataset.state==='loading';attempt++)await wait(80);
    test('Live Google Fonts CSS and font files load in the studio',()=>{
      const status=d.getElementById('fontLoadStatus');
      if(status.dataset.state!=='loaded')throw Error(status.textContent);
      return [...d.fonts].some(face=>face.family.includes('Inter')&&face.status==='loaded')&&[...d.fonts].some(face=>face.family.includes('Literata')&&face.status==='loaded');
    });
    const frame=d.getElementById('previewPage'),doc=frame.contentDocument,view=frame.contentWindow;
    const faces=await Promise.race([Promise.all([doc.fonts.load('400 16px "Inter"'),doc.fonts.load('700 16px "Literata"')]),wait(2500).then(()=>[])]);
    test('Live generated preview loads real heading and body font faces',()=>faces.length===2&&faces.every(group=>group.length>0&&group.every(face=>face.status==='loaded')));
    test('Live sample uses Literata headings and Inter body text',()=>view.getComputedStyle(doc.querySelector('h1')).fontFamily.includes('Literata')&&view.getComputedStyle(doc.body).fontFamily.includes('Inter'));
    for(const mode of ['mobile','desktop']){
      d.querySelector('button[data-width="'+mode+'"]').click();await wait(50);
      test('Live web-font sample fits '+mode+' viewport',()=>doc.documentElement.scrollWidth<=view.innerWidth+1);
    }
    const html=w.eval('htmlExport()'),css=w.eval('cssExport()');
    const standalone=d.createElement('iframe');standalone.style.cssText='width:390px;height:900px;border:0';
    standalone.srcdoc=html.replace('<link rel="stylesheet" href="tokens.css">','<style>'+css+'</style>');
    await new Promise(resolve=>{standalone.onload=resolve;d.body.append(standalone);});
    const standaloneDoc=standalone.contentDocument,standaloneView=standalone.contentWindow;
    const exportedFaces=await Promise.all([standaloneDoc.fonts.load('400 16px "Inter"'),standaloneDoc.fonts.load('700 16px "Literata"')]);
    test('Standalone exported HTML loads its real Google heading and body fonts',()=>exportedFaces.every(group=>group.length>0&&group.every(face=>face.status==='loaded'))&&standaloneView.getComputedStyle(standaloneDoc.body).fontFamily.includes('Inter')&&standaloneView.getComputedStyle(standaloneDoc.querySelector('h1')).fontFamily.includes('Literata'));
    test('Standalone exported web-font page fits a phone viewport',()=>standaloneDoc.documentElement.scrollWidth<=390);
    standalone.remove();
    d.getElementById('fontFallback').click();await wait(50);
    test('Live fallback comparison changes preview families while preserving exports',()=>!view.getComputedStyle(doc.body).fontFamily.includes('Inter')&&view.getComputedStyle(doc.querySelector('h1')).fontFamily.includes('Georgia')&&w.eval('htmlExport()')===html&&w.eval('cssExport()')===css);
    for(const [id,value] of [['fontGoogleBody','source-sans-3'],['fontGoogleHeading','same']]){
      d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change',{bubbles:true}));
    }
    d.getElementById('fontFallback').click();
    for(let attempt=0;attempt<140 && d.getElementById('fontLoadStatus').dataset.state==='loading';attempt++)await wait(80);
    test('Source Sans 3 also loads from the live curated catalogue',()=>d.getElementById('fontLoadStatus').dataset.state==='loaded'&&[...d.fonts].some(face=>face.family.includes('Source Sans 3')&&face.status==='loaded'));
  }catch(error){results.push({name:'Live font integration',pass:false,error:String(error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''

if __name__ == '__main__':
    raise SystemExit(review.main())
