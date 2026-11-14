"""Independent standalone exports checks using the local Chrome runner.

Run: python scripts/standalone_exports_review.py. Owns its app, profile and fixtures.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Standalone Exports review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w = app.contentWindow, d = w.document, results = [];
  window.addEventListener('unhandledrejection', event => {
    results.push({name:'Browser harness completed without an unhandled exception',pass:false,error:String(event.reason?.stack || event.reason)});
    document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  });
  const evaluate = code => w.eval(code);
  const test = (name, fn) => {
    try { if (!fn()) throw Error('Assertion failed'); results.push({name, pass:true}); }
    catch (e) { results.push({name, pass:false, error:String(e)}); }
    document.title='Browser review: '+results.length+' checks; last: '+name;
  };
  const revealArchitecture=()=>d.querySelectorAll('#architecture-sitemap,#architecture-saved-review,#architecture-sitemap-advanced,#architecture-advanced,#sitemap-choices details,#section-sitemap-choices details,#sitemap-editor details').forEach(el=>el.open=true);
  // Destination-editor fixtures explicitly reveal its secondary controls.
  const revealDestinationPlan=()=>{revealArchitecture();const source=d.getElementById('sitemap-source');if(source && source.value!=='custom'){source.value='custom';source.dispatchEvent(new w.Event('change',{bubbles:true}));}d.querySelectorAll('#sitemap-destination-editor, #sitemap-outline-editor, #process-ia .ia-destination-map, #sitemap-choices details, #sitemap-editor details').forEach(el=>el.open=true);};
  const input = (id, value, type='input') => {
    if(id.startsWith('sitemap-') || id==='plan-pages')revealDestinationPlan();
    const el=d.getElementById(id);
    w.DSStudio.paletteWorkspace?.revealControl(el);
    w.DSStudio.typographyWorkspace?.revealControl(el);
    if(id.startsWith('ia-')){const disclosure=el.closest('.ia-editor-disclosure');if(disclosure)disclosure.open=true;}
    el.value=value;
    el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  // Most historical feature fixtures exercise the complete Advanced sample.
  // Default/reset behavior is checked separately through resetStudio directly.
  const reset = () => {evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc = () => d.getElementById('previewPage').contentDocument;
  const previewWindow = () => d.getElementById('previewPage').contentWindow;
  const saved = () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data;
  const wait = (ms=100) => new Promise(resolve => setTimeout(resolve,ms));
  const originalDownload=w.download,originalClipboard=w.navigator.clipboard;
  const prepare=async()=>{
    app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();
    reset();w.DSStudio.inspector.show({language:'css',section:'all'});d.querySelector('[data-width="desktop"]').click();w.dssShowWizardStep(0,false);await wait();
  };
  try {
  test('Independent standalone exports startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  await prepare();
  input('bdSize','lg');d.getElementById('bdMobileFull').checked=true;d.getElementById('bdMobileFull').dispatchEvent(new w.Event('input',{bubbles:true}));await wait();
  const sampleDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Sample home page has header, main, footer, hero and a single headline', () => !!sampleDoc.querySelector('body > header nav') && !!sampleDoc.querySelector('body > main') && !!sampleDoc.querySelector('body > footer nav') && !!sampleDoc.querySelector('#home .sample-lead') && sampleDoc.querySelectorAll('h1').length===1);
  test('Every sample navigation and action anchor reaches an existing section', () => [...sampleDoc.querySelectorAll('a[href^="#"]')].every(link=>sampleDoc.getElementById(link.hash.slice(1))));
  test('Every main section offers primary and secondary actions matching the wizard variants', () => [...sampleDoc.querySelectorAll('main > section')].length===9 && [...sampleDoc.querySelectorAll('main > section')].every(section=>{
    const rows=section.querySelectorAll('.sample-section-actions');
    return rows.length===1 && rows[0].children.length===2 && rows[0].firstElementChild.matches('.ds-button--primary') && rows[0].lastElementChild.matches('a.ds-button--secondary[href]') && (section.id==='contact'?rows[0].firstElementChild.matches('form button[type="submit"]'):rows[0].firstElementChild.matches('a[href]'));
  }));
  test('Section actions follow selected button size and mobile full-width settings', () => [...sampleDoc.querySelectorAll('.sample-section-actions .ds-button')].every(action=>action.classList.contains('ds-button--lg') && action.classList.contains('ds-button--mobile-full')));
  test('Header navigation and section actions make every main section reachable', () => {
    const targets=new Set([...sampleDoc.querySelectorAll('header nav a, .sample-section-actions a')].map(link=>link.getAttribute('href').slice(1)));
    return [...sampleDoc.querySelectorAll('main > section')].every(section=>targets.has(section.id));
  });
  test('Sample images are embedded, labelled and follow the selected palette', () => {
    const images=[...sampleDoc.querySelectorAll('img')];
    return images.length>=2 && images.every(img=>img.alt && img.getAttribute('width') && img.src.startsWith('data:image/svg+xml')) && decodeURIComponent(images[0].src).includes(evaluate('palette().roles.primary')) && !sampleDoc.querySelector('script');
  });
  test('Sample home page showcases actions, cards, forms, table, FAQ and progress', () => ['.card','.ds-button--primary','.ds-button--secondary','.ds-button--accent','.ds-button--outline','.ds-button--text','form input[type="email"]','select','textarea','input[type="radio"]','input[type="checkbox"]','input[type="range"]','input[readonly]','input[disabled]','table caption','details summary','progress','blockquote'].every(selector=>sampleDoc.querySelector(selector)));
  test('Field guide offers ten lesson cards with real practice destinations', () => {
    const cards=[...sampleDoc.querySelectorAll('#services .sample-lesson-card')];
    return sampleDoc.title.includes('Web Design Field Guide') && cards.length===10 && cards.every(card=>sampleDoc.getElementById(card.querySelector('a').hash.slice(1))) && sampleDoc.querySelector('header a[href="#services"]').textContent==='Lessons';
  });
  test('Grid workshop includes twelve tracks, seven layout regions and an inspectable CSS recipe', () => sampleDoc.querySelectorAll('.sample-grid-tracks > span').length===12 && sampleDoc.querySelectorAll('.sample-grid-demo > div').length===7 && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('repeat(12, minmax(0, 1fr))') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('grid-column: 1 / -1;') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('.sample-demo-card { grid-column: span 4; }') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('@media (max-width: 48rem)'));
  test('Type and colour examples describe the actual selected design settings', () => {
    const values=[...sampleDoc.querySelectorAll('.sample-type-settings dd')].map(item=>item.textContent);
    const colours=[...sampleDoc.querySelectorAll('.sample-token-palette code')].map(item=>item.textContent);
    return JSON.stringify(values)===JSON.stringify(evaluate('[state.base+"px",String(state.ratio),String(state.leading)]')) && JSON.stringify(colours)===JSON.stringify(evaluate('[palette().roles.primary,palette().roles.secondary,palette().roles.accent]'));
  });
  test('Flexbox workshop exports working examples, a shared CSS recipe and a layout comparison', () => {
    const recipe=sampleDoc.querySelector('#flex-lab code').textContent;
    return sampleDoc.querySelectorAll('.sample-flex-tags [role="listitem"]').length===3
      && sampleDoc.querySelectorAll('.sample-layout-comparison tbody tr').length===3
      && sampleDoc.querySelectorAll('.sample-lesson-card.sample-flex-stack').length===10
      && recipe.includes('flex: 1 1 12rem') && recipe.includes('margin-top: auto') && evaluate('cssExport()').includes(recipe);
  });
  test('Sample IDs and labelled controls are valid', () => {
    const ids=[...sampleDoc.querySelectorAll('[id]')].map(el=>el.id);
    return ids.length===new Set(ids).size && [...sampleDoc.querySelectorAll('label[for]')].every(label=>sampleDoc.getElementById(label.htmlFor));
  });
  input('bdState','loading'); input('advState','invalid','change');
  const selectedDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Sample markup reflects selected loading and invalid field states', () => !!selectedDoc.querySelector('.sample-selected-action[disabled][aria-busy="true"]') && selectedDoc.getElementById('contact-email').getAttribute('aria-invalid')==='true');
  test('Loading demonstrations leave section navigation and the contact action usable', () => [...selectedDoc.querySelectorAll('.sample-section-actions a')].every(link=>link.getAttribute('href')?.startsWith('#') && !link.hasAttribute('aria-disabled') && !link.hasAttribute('disabled')) && !selectedDoc.querySelector('.sample-form button[type="submit"]').disabled);
  reset(); input('jProject','Cedar Studio'); input('jRadius',24); input('advHeight',52); input('advWeight',800,'change');
  for (const theme of ['light','dark']) {
    input('jTheme',theme);
    const page=d.createElement('iframe'); page.style.cssText='width:1440px;height:1400px;border:0';
    page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{page.onload=resolve;d.body.append(page);});
    const pd=page.contentDocument, pw=page.contentWindow;
    test('Rendered '+theme+' sample applies theme, typography, radius and control height', () => {
      const heading=pw.getComputedStyle(pd.querySelector('h1')), image=pw.getComputedStyle(pd.querySelector('img')), field=pw.getComputedStyle(pd.querySelector('.input'));
      const body=pw.getComputedStyle(pd.body), expected=evaluate(`palette('${theme}').roles.background`);
      return heading.fontWeight==='800' && image.borderRadius==='24px' && parseFloat(field.minHeight)===52 && body.backgroundColor===evaluate(`'rgb('+hexRgb('${expected}').join(', ')+')'`);
    });
    test('Rendered '+theme+' hero image loads without external assets', () => pd.querySelector('#home img').complete && pd.querySelector('#home img').naturalWidth===960);
    test('Rendered '+theme+' button foreground uses the selected component token', () => pw.getComputedStyle(pd.querySelector('.ds-button--primary')).color===evaluate("'rgb('+hexRgb(dssGetButtonContrastData().themes['"+theme+"'].primary.fg).join(', ')+')'"));
    for (const width of [320,768,1440]) {
      page.style.width=width+'px'; await wait();
      test('Rendered '+theme+' home page fits '+width+'px', () => pd.documentElement.scrollWidth<=pw.innerWidth+1);
      test(theme+' section action pairs fit and keep their spacing at '+width+'px', () => [...pd.querySelectorAll('.sample-section-actions')].every(row=>{
        const bounds=row.getBoundingClientRect(), buttons=[...row.children].map(button=>button.getBoundingClientRect());
        const [first,second]=buttons;
        return buttons.every(box=>box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44) && (Math.abs(second.top-first.top)<1?second.left-first.right>=7.5:second.top-first.bottom>=7.5);
      }));
      test(theme+' header logo and project title scale at '+width+'px', () => {
        const logo=pd.querySelector('header .sample-logo'), title=pd.querySelector('header .sample-brand-title');
        const box=logo.getBoundingClientRect(), expected=evaluate(`fluidTypePx(3,${width})`);
        return logo.textContent==='Logo' && logo.getAttribute('aria-hidden')==='true' && box.width>=44 && Math.abs(box.width-box.height)<1 && logo.scrollWidth<=logo.clientWidth+1 && title.textContent==='Cedar Studio' && Math.abs(parseFloat(pw.getComputedStyle(title).fontSize)-expected)<.11;
      });
      const menu=pd.getElementById('sample-menu'), toggle=menu.querySelector('summary');
      const desktop=pd.querySelector('.sample-desktop-navigation'), mobile=pd.getElementById('sample-mobile-navigation');
      if (width<=768) {
        test(theme+' header uses a closed hamburger at '+width+'px', () => pw.getComputedStyle(desktop).display==='none' && toggle.getBoundingClientRect().width>=44 && toggle.getBoundingClientRect().height>=44 && !menu.open && mobile.getClientRects().length===0 && toggle.getAttribute('aria-controls')===mobile.id);
        toggle.focus(); toggle.click();
        test(theme+' hamburger opens and closes the navigation at '+width+'px', () => {
          const opened=menu.open && mobile.getBoundingClientRect().height>0 && mobile.querySelectorAll('a').length===6 && pw.getComputedStyle(toggle.querySelector('.sample-menu-bars')).display==='none' && pd.activeElement===toggle;
          toggle.click();
          return opened && !menu.open && mobile.getClientRects().length===0;
        });
        test(theme+' menu is borderless with default text and an accent-only icon', () => {
          const accent=evaluate(`palette('${theme}').roles.accent`), text=evaluate(`palette('${theme}').roles.text`);
          const colour=hex=>evaluate(`'rgb('+hexRgb('${hex}').join(', ')+')'`);
          const style=pw.getComputedStyle(toggle);
          return pw.getComputedStyle(toggle.querySelector('svg')).stroke===colour(accent) && style.color===colour(text) && style.backgroundColor==='rgba(0, 0, 0, 0)' && parseFloat(style.borderTopWidth)===0 && toggle.querySelector('span').textContent==='Menu';
        });
      } else {
        test(theme+' desktop navigation stays visible with its mobile menu closed', () => !menu.open && pw.getComputedStyle(menu).display==='none' && desktop.getBoundingClientRect().height>0 && desktop.querySelectorAll('a').length===6);
      }
    }
    page.remove();
  }
  reset(); await wait();
  const gridPage=d.createElement('iframe'); gridPage.style.cssText='width:1440px;height:1000px;border:0';
  const loadGridPage = async () => {
    gridPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{gridPage.onload=resolve;if(!gridPage.isConnected)d.body.append(gridPage);});
  };
  await loadGridPage();
  const gridDoc=()=>gridPage.contentDocument, gridWindow=()=>gridPage.contentWindow;
  const gridStyle=selector=>gridWindow().getComputedStyle(gridDoc().querySelector(selector));
  for (const underline of [true,false]) {
    evaluate(`adv.underline=${underline}; applyAdvanced(); renderCode();`);
    await loadGridPage(); await wait();
    test('Header navigation overrides the general underline setting '+underline+' in export and preview', () => [gridDoc(),previewDoc()].every(doc=>{
      const win=doc.defaultView;
      return [...doc.querySelectorAll('.sample-header .sample-nav a')].every(link=>win.getComputedStyle(link).textDecorationLine==='none') && win.getComputedStyle(doc.querySelector('.sample-footer .footer-links a')).textDecorationLine===(underline?'underline':'none');
    }));
    test('All resource table links start plain with general underlines '+underline+' in export and preview', () => [gridDoc(),previewDoc()].every(doc=>{
      const links=[...doc.querySelectorAll('.sample-table-wrap a')];
      return links.length===3 && links.every(link=>doc.defaultView.getComputedStyle(link).textDecorationLine==='none');
    }));
  }
  reset(); await wait(); await loadGridPage();
  for (const theme of ['light','dark']) {
    gridDoc().documentElement.dataset.theme=theme;
    for (const width of [320,1440]) {
      gridPage.style.width=width+'px'; await wait();
      gridDoc().getElementById('sample-menu').open=width<=768;
      const link=gridDoc().querySelector(width<=768?'.sample-mobile-navigation a':'.sample-desktop-navigation a');
      const style=gridDoc().querySelector('style'), original=style.textContent;
      // Equal-specificity class substitutions exercise the exported pointer-state cascade.
      style.textContent=original.replaceAll(':hover','.review-hover').replaceAll(':active','.review-active');
      try {
        test(theme+' header navigation underlines on hover without resizing at '+width+'px', () => {
          const before=link.getBoundingClientRect(); link.classList.add('review-hover');
          const hovered=gridWindow().getComputedStyle(link), after=link.getBoundingClientRect();
          const passes=hovered.textDecorationLine==='underline' && Math.abs(before.width-after.width)<1 && Math.abs(before.height-after.height)<1;
          link.classList.remove('review-hover'); return passes;
        });
        test(theme+' header navigation adds a non-colour pressed cue at '+width+'px', () => {
          const normal=parseFloat(gridWindow().getComputedStyle(link).textDecorationThickness);
          link.classList.add('review-active'); const pressed=gridWindow().getComputedStyle(link);
          const passes=pressed.textDecorationLine==='underline' && parseFloat(pressed.textDecorationThickness)>normal;
          link.classList.remove('review-active'); return passes;
        });
        test(theme+' header navigation uses the button keyboard focus ring at '+width+'px', () => {
          link.focus(); const focus=gridWindow().getComputedStyle(link), root=gridWindow().getComputedStyle(gridDoc().documentElement);
          const expected=evaluate(`'rgb('+hexRgb('${root.getPropertyValue('--button-focus').trim()}').join(', ')+')'`);
          const passes=gridDoc().activeElement===link && link.matches(':focus-visible') && focus.outlineStyle==='solid' && focus.outlineWidth===root.getPropertyValue('--button-focus-width').trim() && focus.outlineColor===expected && focus.outlineOffset==='3px';
          link.blur(); return passes;
        });
        const resources=[...gridDoc().querySelectorAll('.sample-table-wrap a')];
        test(theme+' resource links underline on hover without resizing at '+width+'px', () => resources.every(resource=>{
          const before=resource.getBoundingClientRect(); resource.classList.add('review-hover');
          const computed=gridWindow().getComputedStyle(resource), after=resource.getBoundingClientRect();
          const passes=computed.textDecorationLine==='underline' && Math.abs(before.width-after.width)<1 && Math.abs(before.height-after.height)<1;
          resource.classList.remove('review-hover'); return passes;
        }));
        test(theme+' resource links have a stronger pressed underline at '+width+'px', () => resources.every(resource=>{
          const normal=parseFloat(gridWindow().getComputedStyle(resource).textDecorationThickness);
          resource.classList.add('review-active'); const computed=gridWindow().getComputedStyle(resource);
          const passes=computed.textDecorationLine==='underline' && parseFloat(computed.textDecorationThickness)>normal;
          resource.classList.remove('review-active'); return passes;
        }));
        test(theme+' resource links retain the shared keyboard focus ring at '+width+'px', () => resources.every(resource=>{
          resource.focus(); const computed=gridWindow().getComputedStyle(resource), root=gridWindow().getComputedStyle(gridDoc().documentElement);
          const expected=evaluate(`'rgb('+hexRgb('${root.getPropertyValue('--button-focus').trim()}').join(', ')+')'`);
          const passes=gridDoc().activeElement===resource && resource.matches(':focus-visible') && computed.outlineStyle==='solid' && computed.outlineWidth===root.getPropertyValue('--button-focus-width').trim() && computed.outlineColor===expected && computed.outlineOffset==='3px';
          resource.blur(); return passes;
        }));
      } finally { style.textContent=original; }
    }
  }
  gridPage.style.width='1440px'; await loadGridPage();
  test('Wide page uses twelve tracks with six-column halves and four-column cards', () => {
    const width=selector=>gridDoc().querySelector(selector).getBoundingClientRect().width;
    return ['.sample-hero','.sample-split','.card-grid'].every(selector=>gridStyle(selector).gridTemplateColumns.split(' ').length===12) && Math.abs(width('.sample-hero > div')*2+24-width('.sample-hero'))<1 && Math.abs(width('.card-grid > .card')*3+48-width('.card-grid'))<1;
  });
  test('Default layout padding, margins and gutters follow the 8px spacing scale', () => {
    const checks=[['main','paddingLeft',32],['.sample-hero','paddingTop',80],['.sample-section','paddingTop',64],['.card','paddingTop',24],['.sample-home h1','marginBottom',16],['.sample-lead','marginBottom',24],['.card-grid','columnGap',24],['.sample-home .input','paddingLeft',16],['.sample-home .input','paddingTop',8],['.sample-footer .footer-inner','paddingTop',32]];
    return checks.every(([selector,prop,size])=>parseFloat(gridStyle(selector)[prop])===size);
  });
  test('Footer spacing is applied once and ordinary selects retain the surface colour', () => gridStyle('.sample-footer').paddingTop==='0px' && gridStyle('.sample-footer').marginTop==='0px' && gridStyle('select.input').backgroundColor===gridStyle('.card').backgroundColor && gridStyle('input[readonly]').backgroundColor!==gridStyle('select.input').backgroundColor);
  test('Link and button state colours survive the simplified cascade in both themes', () => {
    // Substitute classes of equal specificity to resolve pointer-state CSS in headless Chrome.
    const style=gridDoc().querySelector('style'), original=style.textContent;
    style.textContent=original.replaceAll(':hover','.review-hover').replaceAll(':active','.review-active')+'\n.ds-button { transition: none !important; }';
    try {
      return ['light','dark'].every(theme=>{
        gridDoc().documentElement.dataset.theme=theme;
        return ['primary','secondary','accent','outline','text'].every(variant=>['hover','active'].every(stateName=>[...gridDoc().querySelectorAll('.ds-button--'+variant)].every(button=>{
        button.classList.add('review-'+stateName);
        const computed=gridWindow().getComputedStyle(button), root=gridWindow().getComputedStyle(gridDoc().documentElement);
        const rgb=value=>evaluate(`'rgb('+hexRgb('${value.trim()}').join(', ')+')'`);
        const matches=computed.color===rgb(root.getPropertyValue('--button-'+variant+'-'+stateName+'-text')) && computed.backgroundColor===rgb(root.getPropertyValue('--button-'+variant+'-'+stateName));
        button.classList.remove('review-'+stateName);
        return matches;
        })));
      });
    } finally { style.textContent=original; gridDoc().documentElement.dataset.theme='light'; }
  });
  for (const width of [320,390,600,768,900,1024,1280,1440]) {
    gridPage.style.width=width+'px'; await wait();
    test('Grid and spacing fit the generated page at '+width+'px', () => {
      const doc=gridDoc(), cards=[...doc.querySelectorAll('#services .card')], row=doc.querySelector('#services .card-grid').getBoundingClientRect();
      const expected=width<476?1:width<710?2:3;
      const firstRow=cards.filter(card=>Math.abs(card.getBoundingClientRect().top-cards[0].getBoundingClientRect().top)<1);
      return doc.documentElement.scrollWidth<=width+1 && firstRow.length===expected && cards.every(card=>card.getBoundingClientRect().left>=row.left-1 && card.getBoundingClientRect().right<=row.right+1) && (width>768 || gridStyle('.sample-hero').gridTemplateColumns.split(' ').length===1);
    });
    test('Tutorial grid adapts spans and keeps every region in bounds at '+width+'px', () => {
      const doc=gridDoc(), demo=doc.querySelector('.sample-grid-demo'), bounds=demo.getBoundingClientRect(), figure=doc.querySelector('.sample-grid-figure').getBoundingClientRect(), notes=doc.querySelector('.sample-lab-notes').getBoundingClientRect();
      const columns=gridStyle('.sample-grid-demo').gridTemplateColumns.split(' ').length;
      const gap=parseFloat(gridStyle('.sample-grid-demo').columnGap), main=doc.querySelector('.sample-demo-main').getBoundingClientRect(), aside=doc.querySelector('.sample-demo-aside').getBoundingClientRect(), cards=[...doc.querySelectorAll('.sample-demo-card')];
      const spans=width<=768?[...demo.children].every(region=>Math.abs(region.getBoundingClientRect().width-bounds.width)<1):Math.abs(main.width-aside.width*2-gap)<1 && Math.abs(cards.reduce((total,card)=>total+card.getBoundingClientRect().width,0)+gap*2-bounds.width)<1;
      return columns===(width<=768?1:12) && spans && (width<=1024?notes.top>figure.bottom:notes.left>figure.right) && [...demo.children].every(region=>{const box=region.getBoundingClientRect();return box.left>=bounds.left-1 && box.right<=bounds.right+1 && region.scrollWidth<=region.clientWidth+1;});
    });
  }
  gridPage.style.width='768px'; input('advColumns',320); input('advGap',32); await loadGridPage();
  test('Card minimum width and gutter controls still change responsive column counts', () => gridStyle('.card-grid').gridTemplateColumns.split(' ').length===2 && gridStyle('.card-grid').columnGap==='32px');
  test('Tutorial grid uses the configured grid gap', () => gridStyle('.sample-grid-demo').gap==='32px');
  test('Flexbox rows share the configured grid gap', () => gridStyle('.sample-flex-row').gap==='32px' && gridStyle('.sample-flex-media').gap==='32px');
  for (const theme of ['light','dark']) {
    evaluate(`state.theme='${theme}'; apply();`); await loadGridPage();
    for (const width of [320,390,768,1280,1440]) {
      gridPage.style.width=width+'px'; await wait();
      test(theme+' Flexbox examples align, wrap and fit at '+width+'px', () => {
        const doc=gridDoc(), row=doc.querySelector('.sample-flex-row'), tags=doc.querySelector('.sample-flex-tags'), media=doc.querySelector('.sample-flex-media');
        const marker=doc.querySelector('.sample-flex-marker').getBoundingClientRect(), copy=doc.querySelector('.sample-flex-copy').getBoundingClientRect();
        const rowStyle=gridStyle('.sample-flex-row');
        return rowStyle.display==='flex' && rowStyle.flexWrap==='wrap' && rowStyle.alignItems==='center' && rowStyle.justifyContent==='space-between'
          && gridStyle('.sample-flex-copy').flexGrow==='1' && gridStyle('.sample-flex-copy').flexShrink==='1'
          && gridStyle('.sample-flex-stack').flexDirection==='column'
          && (width>390 || (tags.getBoundingClientRect().top>row.firstElementChild.getBoundingClientRect().bottom && copy.top>=marker.bottom))
          && [row,tags,media,...row.children,...media.children].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && el.scrollWidth<=el.clientWidth+1;})
          && doc.documentElement.scrollWidth<=width+1;
      });
    }
  }
  gridPage.style.width='320px'; await wait();
  test('Large custom gutters and card minimums collapse without mobile overflow', () => gridStyle('.card-grid').gridTemplateColumns.split(' ').length===1 && gridDoc().documentElement.scrollWidth<=320);
  evaluate('importConfig({spacing:3,advanced:{gap:12,height:42},buttonDesign:{padX:18,padY:12,minHeight:44}})');
  await loadGridPage();
  test('Imported spacing and component dimensions are preserved without snapping', () => evaluate('state.spacing===3 && adv.gap===12 && adv.height===42 && state.buttonDesign.padX===18 && state.buttonDesign.padY===12 && state.buttonDesign.minHeight===44') && gridStyle('.card').paddingTop==='18px' && gridStyle('.ds-button').paddingLeft==='18px' && gridStyle('.input').minHeight==='42px');
  gridPage.remove();
  reset(); await wait();
  await prepare();
  const standalone=d.createElement('iframe'); standalone.style.cssText='width:1440px;height:1000px;border:0';
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('jProject','Standalone homepage'); input('jBase',18); await wait();
    const files={}; w.download=(name,content,type)=>{files[name]={content,type};};
    d.getElementById('jExportHtml').click(); d.getElementById('jExportCss').click(); w.download=originalDownload;
    const parsed=new w.DOMParser().parseFromString(files['index.html'].content,'text/html');
    test(theme+' standalone pair has a relative CSS link, embedded images and no studio scripts or inline styles', () => parsed.querySelector('link[rel="stylesheet"][href="tokens.css"]') && !parsed.querySelector('script,style') && [...parsed.querySelectorAll('img')].every(img=>img.src.startsWith('data:image/svg+xml')) && parsed.documentElement.dataset.theme===theme);
    const cssUrl=w.URL.createObjectURL(new w.Blob([files['tokens.css'].content],{type:'text/css'}));
    standalone.srcdoc=files['index.html'].content.replace('href="tokens.css"','href="'+cssUrl+'"');
    await new Promise(resolve=>{standalone.onload=resolve;if(!standalone.isConnected)d.body.append(standalone);});
    const pd=standalone.contentDocument, pw=standalone.contentWindow;
    test(theme+' HTML loads its separate complete stylesheet and basic website components', () => pd.querySelector('link[rel="stylesheet"]').sheet && !pd.querySelector('style,script') && pw.getComputedStyle(pd.body).fontSize==='18px' && pd.querySelector('.sample-brand').textContent.includes('Standalone homepage') && ['header nav','main','#home .sample-lead','img','.card','form input[type="email"]','table','details summary','.sample-notice','progress','footer nav'].every(selector=>pd.querySelector(selector)));
    for (const width of [320,768,1440]) {
      standalone.style.width=width+'px'; await wait();
      test(theme+' separately linked website reflows at '+width+'px', () => pd.documentElement.scrollWidth<=width+1 && pw.getComputedStyle(pd.querySelector('.sample-hero')).gridTemplateColumns.split(' ').length===(width<=768?1:12));
    }
    standalone.style.width='320px'; await wait();
    const menu=pd.getElementById('sample-menu'); menu.querySelector('summary').click();
    test(theme+' standalone mobile menu and FAQ work with native HTML', () => {
      const faq=pd.getElementById('getting-started'), wasOpen=faq.open; faq.querySelector('summary').click();
      return menu.open && pd.querySelector('.sample-mobile-navigation').getBoundingClientRect().height>0 && faq.open!==wasOpen && !pd.querySelector('.sample-form').checkValidity();
    });
    w.URL.revokeObjectURL(cssUrl);
  }
  standalone.remove(); reset(); await wait();
  const advancedHtml=evaluate('htmlExport()'), advancedCss=evaluate('cssExport()');
  evaluate('resetStudio()');await wait();
  test('Sample mode resets to Basic with a labelled independent tab group', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')==='dockModeBasic' && d.querySelector('[aria-label="Website sample complexity"]'));
  d.getElementById('dockTabHtml').click(); d.getElementById('dockModeBasic').click(); await wait();
  test('Basic selection synchronizes inspector, preview and central exports while retaining the language tab', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('codeView').textContent===evaluate('codeContent()') && previewDoc().querySelector('.skill-cards') && !previewDoc().querySelector('#design-process'));
  test('Basic exports shared system foundations without the Advanced gallery styles', () => evaluate('cssExport()').length<advancedCss.length && evaluate('cssExport()').includes('--space-unit:') && evaluate('cssExport()').includes('--button-pad-x:') && evaluate('cssExport()').includes('repeat(auto-fit, minmax(') && !evaluate('cssExport()').includes('.sample-grid-demo'));
  const basicDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Basic hero embeds the same accessible offline illustration as Advanced and the live inspector', () => {
    const image=basicDoc.querySelector('#home img'), advanced=new w.DOMParser().parseFromString(advancedHtml,'text/html').querySelector('#home img');
    const live=previewDoc().querySelector('#home img');
    return image && image.getAttribute('src')===advanced.getAttribute('src') && image.getAttribute('src').startsWith('data:image/svg+xml;') && image.alt.length>0 && image.width===960 && image.height===720 && live.complete && live.naturalWidth===960 && live.getAttribute('src')===image.getAttribute('src') && d.getElementById('dockCss').textContent===evaluate('htmlExport()');
  });
  test('Basic HTML has exactly four main sections, one heading, logo/nav, hero, three cards, signup and footer', () => basicDoc.querySelectorAll('main > section').length===4 && basicDoc.querySelectorAll('h1').length===1 && basicDoc.querySelector('header .logo[aria-hidden="true"]') && basicDoc.querySelector('header nav[aria-label]') && basicDoc.querySelector('#home .button') && basicDoc.querySelectorAll('.skill-cards article').length===3 && basicDoc.querySelector('#signup form') && basicDoc.querySelector('footer nav[aria-label], footer nav[aria-labelledby]') && basicDoc.querySelector('footer a[href="#top"]'));
  test('Basic is a compact component showcase without long code recipes or exercises', () => basicDoc.querySelector('h1').textContent==='Start with the essentials.' && !basicDoc.querySelector('main pre, main .practice') && !/Try it:|workshop sign-up|HTML \/ Meaning/.test(basicDoc.querySelector('main').textContent) && basicDoc.querySelectorAll('main > section h2').length===3);
  test('Basic showcase keeps one native form, component FAQ and footer disclosure', () => basicDoc.querySelectorAll('details').length===3 && basicDoc.querySelectorAll('main form').length===1 && basicDoc.getElementById('contact-form') && basicDoc.getElementById('basic-faq').closest('#basic-usability') && basicDoc.getElementById('footer-sitemap'));
  test('Basic semantic structure distinguishes sections, independent articles and related aside content', () => basicDoc.querySelectorAll('main').length===1 && basicDoc.querySelectorAll('h1').length===1 && [...basicDoc.querySelectorAll('main section')].every(section=>section.getAttribute('aria-labelledby') && section.contains(basicDoc.getElementById(section.getAttribute('aria-labelledby')))) && basicDoc.querySelector('.layout-example .content-sidebar > article[aria-labelledby="main-content-example-title"] + aside[aria-labelledby="related-links-title"]') && basicDoc.querySelectorAll('.skill-cards > article').length===3 && !basicDoc.querySelector('asside') && basicDoc.querySelector('header nav[aria-label]') && basicDoc.querySelector('footer nav[aria-labelledby="sitemap-title"]') && basicDoc.querySelector('.skip-link').hash==='#main-content');
  test('Basic names header destinations and hero actions after the components they reach', () => [...basicDoc.querySelectorAll('.desktop-navigation a')].map(a=>a.textContent).join(',')==='Home,Components,Layouts,Forms' && [...basicDoc.querySelectorAll('#home .section-actions a')].map(a=>a.hash).join(',')==='#features,#lists');
  test('Basic form groups native radio choices with a legend and one initial choice', () => basicDoc.querySelector('#form-options > legend').textContent==='Learning preference' && basicDoc.querySelectorAll('#form-options input[type="radio"][name="learning"]').length===2 && basicDoc.querySelectorAll('#form-options input:checked').length===1 && [...basicDoc.querySelectorAll('#form-options input')].every(input=>input.closest('label')) && basicDoc.querySelector('#basic-signup-note[role="status"]'));
  test('Basic optional select and textarea start empty with matching labels', () => ['signup-topic','signup-question'].every(id=>basicDoc.getElementById(id).value==='' && !basicDoc.getElementById(id).required && basicDoc.querySelector('label[for="'+id+'"]')) && basicDoc.getElementById('signup-question').defaultValue==='');
  test('Basic footer has main navigation and a four-section eyebrow sitemap', () => basicDoc.querySelectorAll('footer nav').length===2 && basicDoc.querySelector('footer .footer-links') && basicDoc.getElementById('footer-sitemap').tagName==='DETAILS' && !basicDoc.getElementById('footer-sitemap').open && [...basicDoc.querySelectorAll('footer .footer-links a')].map(a=>a.hash).join(',')==='#home,#features,#lists,#signup' && [...basicDoc.querySelectorAll('#sitemap .sitemap-list > li > a')].map(a=>a.textContent).join(',')==='HTML & CSS essentials,Components / Flexbox,Layouts / CSS Grid,Forms / Labels & controls' && basicDoc.querySelectorAll('#sitemap a').length===12 && basicDoc.querySelector('#sitemap a[href="#home"]') && !basicDoc.querySelector('#sitemap a[href="#footer"]'));
  test('Basic gives every main section one primary CTA and one secondary route', () => [...basicDoc.querySelectorAll('main > section')].every(section => {
    const pair=section.querySelector('.section-actions');
    return pair && pair.children.length===2 && pair.children[0].classList.contains('ds-button--primary') && pair.children[1].classList.contains('ds-button--secondary') && !pair.querySelector('[disabled], [aria-busy], [data-preview-state]');
  }));
  test('Basic feature cards offer distinct paths into the practical toolkit', () => [...basicDoc.querySelectorAll('.skill-cards article > a')].map(a=>a.hash).join(',')==='#list-collection,#list-workflow,#list-terms');
  d.querySelector('[data-width="mobile"]').click(); await wait();
  const basicMenuAccent=evaluate('state.accent');
  previewDoc().querySelector('#basic-menu summary').click(); input('jAccent','#3769a8'); await wait();
  test('Basic preview preserves an open hamburger through live palette edits', () => previewDoc().getElementById('basic-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.menu-icon')).color==='rgb(55, 105, 168)');
  previewDoc().querySelector('#basic-menu a[href="#lists"]').click(); await wait();
  test('Basic mobile navigation reaches the toolkit inside the preview', () => previewDoc().activeElement===previewDoc().getElementById('lists'));
  previewDoc().getElementById('basic-menu').open=false; input('jAccent',basicMenuAccent);
  d.querySelector('[data-width="fluid"]').click(); await wait();
  const basicActionProject=evaluate('projectJson()');
  for (const link of [...previewDoc().querySelectorAll('.section-actions a, .skill-cards article > a')]) {
    const page=previewDoc(), target=page.getElementById(link.hash.slice(1));
    link.click(); await wait();
    test('Basic action to '+link.getAttribute('href')+' navigates within the preview and focuses its destination', () => previewDoc()===page && page.activeElement===target && evaluate('projectJson()')===basicActionProject);
  }
  const basicActionSettings=evaluate('projectJson()');
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('bdVariant','secondary'); input('bdDefaultBg','#602d54'); input('bdText','#ffffff'); input('bdSize','lg');
    d.getElementById('bdMobileFull').checked=true; d.getElementById('bdMobileFull').dispatchEvent(new w.Event('input',{bubbles:true})); await wait();
    test(theme+' Basic CTAs follow wizard variant colours, size and width settings in the preview and HTML inspector', () => {
      const page=previewDoc(), links=[...page.querySelectorAll('.section-actions .ds-button--secondary')];
      return links.length===4 && links.every(a=>previewWindow().getComputedStyle(a).backgroundColor==='rgb(96, 45, 84)' && a.classList.contains('ds-button--lg') && a.classList.contains('ds-button--mobile-full')) && previewWindow().getComputedStyle(page.querySelector('.section-actions .ds-button--primary')).backgroundColor!=='rgb(96, 45, 84)' && d.getElementById('dockCss').textContent===evaluate('htmlExport()');
    });
    d.querySelector('button[data-width="mobile"]').click(); await wait();
    test(theme+' Basic mobile CTAs use the selected full width and retain visible keyboard focus', () => {
      const page=previewDoc(), pairs=[...page.querySelectorAll('.section-actions')], link=page.querySelector('#features .ds-button--secondary');
      link.focus();
      return pairs.every(pair=>[...pair.children].every(a=>Math.abs(a.getBoundingClientRect().width-pair.getBoundingClientRect().width)<2)) && link.matches(':focus-visible') && previewWindow().getComputedStyle(link).outlineStyle==='solid' && page.documentElement.scrollWidth<=390;
    });
    d.querySelector('button[data-width="fluid"]').click(); await wait();
    d.getElementById('dockTabCss').click();
    test(theme+' Basic CSS inspector and preview share the wizard-generated CTA stylesheet', () => d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('#602d54'));
    d.getElementById('dockTabHtml').click();
  }
  evaluate('importConfig('+basicActionSettings+')'); await wait();
  test('Basic HTML IDs, fragment destinations and form labels resolve without scripts or inline styles', () => {
    const ids=[...basicDoc.querySelectorAll('[id]')].map(el=>el.id);
    return ids.length===new Set(ids).size && !basicDoc.querySelector('script,style') && basicDoc.querySelector('link[href="tokens.css"]') && [...basicDoc.querySelectorAll('a[href^="#"]')].every(link=>basicDoc.getElementById(link.hash.slice(1))) && [...basicDoc.querySelectorAll('label[for]')].every(label=>basicDoc.getElementById(label.htmlFor));
  });
  for (const [key,id] of [['End','dockModeAdvanced'],['Home','dockModeBasic'],['ArrowRight','dockModeAdvanced'],['ArrowLeft','dockModeBasic']]) {
    const selected=d.querySelector('.studio-dock-modes [aria-selected="true"]');
    selected.dispatchEvent(new w.KeyboardEvent('keydown',{key,bubbles:true})); await wait();
    test('Mode tabs support '+key+' navigation and one tab stop', () => d.activeElement===d.getElementById(id) && d.getElementById(id).getAttribute('aria-selected')==='true' && [...d.querySelectorAll('.studio-dock-modes button')].filter(button=>button.tabIndex===0).length===1 && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')===id);
  }
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Returning to Advanced preserves its exact generated page and CSS', () => evaluate('htmlExport()')===advancedHtml && evaluate('cssExport()')===advancedCss);
  d.getElementById('dockModeBasic').click(); await wait(); d.getElementById('jSaveLocal').click();
  const basicProjectId=d.getElementById('jProjects').value, basicProject=evaluate('projectJson()');
  test('Basic selection is saved with the active local project and JSON', () => JSON.parse(basicProject).sampleMode==='basic' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[basicProjectId].data.sampleMode==='basic');
  reset(); evaluate('importConfig('+basicProject+')'); await wait();
  test('Import restores Basic tab selection, preview and export generation', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && previewDoc().querySelector('.signup-form'));
  const basicFiles=[]; w.download=(name,content,type)=>basicFiles.push({name,content,type});
  for (const [index,button] of [...d.querySelectorAll('[data-website-download]')].entries()) {
    button.click(); const html=button.dataset.websiteDownload==='html';
    test('Basic website download '+index+' uses the selected sample and matching file name', () => basicFiles.at(-1).name===(html?'index.html':'tokens.css') && basicFiles.at(-1).content===evaluate(html?'htmlExport()':'cssExport()'));
  }
  let basicCopied=''; Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{basicCopied=text;}}});
  for (const language of ['html','css']) {
    d.getElementById(language==='html'?'dockTabHtml':'dockTabCss').click(); d.getElementById('dockCopy').click(); await wait(); d.getElementById('dockDownload').click();
    test('Basic '+language+' copy and inspector download match the visible code', () => basicCopied===d.getElementById('dockCss').textContent && basicFiles.at(-1).content===basicCopied && basicFiles.at(-1).name===(language==='html'?'index.html':'tokens.css'));
  }
  test('Basic keeps section inspection without a separate exercise guide', () => !d.getElementById('dockLearning').hidden && !d.querySelector('.dock-start') && w.DSStudio.stages[8].task.includes('spacing unit'));
  for (const section of ['basics','header','hero','skills','toolkit','form','footer']) {
    input('dockSection',section,'change');
    for (const language of ['html','css']) {
      d.getElementById(language==='html'?'dockTabHtml':'dockTabCss').click();
      const shown=d.getElementById('dockCss').textContent;
      test('Basic '+section+' '+language+' excerpt isolates its authored section', () => shown.includes('SECTION: '+section) && shown!==evaluate(language==='html'?'htmlExport()':'cssExport()') && (section!=='hero' || !shown.includes('SECTION: toolkit')));
      d.getElementById('dockCopy').click(); await wait(); d.getElementById('dockDownload').click();
      test('Basic '+section+' '+language+' copies excerpt but downloads complete file', () => basicCopied===shown && basicFiles.at(-1).content===evaluate(language==='html'?'htmlExport()':'cssExport()') && basicFiles.at(-1).name===(language==='html'?'index.html':'tokens.css'));
    }
  }
  input('dockSection','hero','change');
  const beforeExercisePadding=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.hero')).paddingTop), beforeExerciseUnit=evaluate('state.spacing');
  input('jSpacing',6); await wait();
  test('Focused CSS follows live spacing changes without changing complete preview styles', () => previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.hero')).paddingTop)===beforeExercisePadding*6/beforeExerciseUnit && d.getElementById('dockCss').textContent.includes('grid-template-columns'));
  input('dockSection','basics','change');
  test('Page basics shows current spacing token definitions for the live exercise', () => d.getElementById('dockCss').textContent.includes('--space-unit: 6px;') && d.getElementById('dockCss').textContent.includes('--space-4: calc(var(--space-unit) * 4);'));
  input('dockSection','hero','change');
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Advanced hides learning controls and always shows complete code', () => d.getElementById('dockLearning').hidden && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  d.getElementById('dockModeBasic').click(); await wait();
  test('Returning to Basic restores its section filter without saving it in project state', () => d.getElementById('dockSection').value==='hero' && !d.getElementById('dockLearning').hidden && !JSON.parse(evaluate('projectJson()')).dockSection);
  let finishExcerptCopy;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>new Promise(resolve=>{finishExcerptCopy=resolve;})}});
  d.getElementById('dockCopy').click(); input('dockSection','header','change'); finishExcerptCopy(); await wait();
  test('A delayed clipboard result cannot label another section as copied', () => d.getElementById('dockCopy').textContent==='Copy CSS excerpt');
  w.DSStudio.inspector.show();
  for (const theme of ['light','dark']) {
    input('dockTheme',theme,'change');
    for (const width of [320,1440]) {
      app.style.width=width+'px'; await wait();
      test(theme+' Basic learning controls fit at '+width+'px with expanded guide', () => {
        const learning=d.getElementById('dockLearning'), select=d.getElementById('dockSection');
        return learning.scrollWidth<=learning.clientWidth+1 && select.getBoundingClientRect().width<=learning.clientWidth && learning.clientHeight>0 && select.getBoundingClientRect().bottom<=learning.getBoundingClientRect().bottom+1 && select.labels[0].textContent==='Study a section' && select.tabIndex===0;
      });
    }
  }
  input('dockTheme','light','change');
  input('dockSection','all','change'); input('jSpacing',4); await wait();
  test('Complete file restores export parity and formatted labelled markup', () => d.getElementById('dockCss').textContent===evaluate('cssExport()') && /<article[^>]+>\n\s+<p/.test(evaluate('htmlExport()')) && /\.hero-layout \{\n\s+display: grid;/.test(evaluate('cssExport()')));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard}); w.download=originalDownload;
  const initialBasicImage=previewDoc().querySelector('#home img').getAttribute('src');
  input('jProject','Harbour learning club'); input('jBase',18); input('jPrimary','#196b63'); input('advGap',32); await wait();
  test('Basic hero illustration follows live palette edits and HTML exports', () => {
    const live=previewDoc().querySelector('#home img'), exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#home img');
    return live.complete && live.naturalWidth===960 && live.getAttribute('src')!==initialBasicImage && live.getAttribute('src')===exported.getAttribute('src') && decodeURIComponent(live.getAttribute('src')).includes(evaluate('palette().roles.primary'));
  });
  test('Basic design settings update its HTML, CSS, preview and source descriptions', () => previewDoc().querySelector('.brand').textContent.includes('Harbour learning club') && previewWindow().getComputedStyle(previewDoc().body).fontSize==='18px' && previewWindow().getComputedStyle(previewDoc().querySelector('.skill-cards')).gap==='32px' && d.getElementById('dockNote').textContent.startsWith('Basic CSS'));
  const basicForm=previewDoc().querySelector('form');
  test('Basic signup has required name/email/consent and native invalid-input checks', () => !basicForm.checkValidity() && ['signup-name','signup-email'].every(id=>previewDoc().getElementById(id).required) && basicForm.querySelector('input[type="checkbox"]').required);
  previewDoc().getElementById('signup-name').value='Taylor'; previewDoc().getElementById('signup-email').value='taylor@example.com'; basicForm.querySelector('input[type="checkbox"]').checked=true;
  previewDoc().getElementById('signup-topic').value='grid'; previewDoc().getElementById('signup-question').value='How do columns adapt?';
  previewDoc().querySelector('input[name="learning"][value="group"]').checked=true;
  previewDoc().getElementById('basic-faq').open=true;
  const basicBrowsingDoc=previewDoc(); basicForm.requestSubmit(); await wait();
  test('Basic live signup validates and remains a static demonstration without navigating', () => previewDoc()===basicBrowsingDoc && basicForm.checkValidity() && previewDoc().getElementById('basic-signup-note').textContent.includes('No message has been sent'));
  input('jRadius',20); await wait();
  test('Basic optional controls and native FAQ retain state across live edits', () => previewDoc().getElementById('signup-topic').value==='grid' && previewDoc().getElementById('signup-question').value==='How do columns adapt?' && previewDoc().getElementById('basic-faq').open && previewDoc().querySelector('input[name="learning"][value="group"]').checked);
  test('Basic form values survive live design edits', () => previewDoc().getElementById('signup-name').value==='Taylor' && previewDoc().querySelector('input[type="checkbox"]').checked);
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Switching sample modes resets browsing without leaking Basic form values into Advanced', () => previewDoc().getElementById('contact-name').value==='' && Math.abs(previewWindow().scrollY)<1);
  d.getElementById('dockModeBasic').click(); await wait();
  test('Switching back to Basic begins a fresh browsing session', () => previewDoc().getElementById('signup-name').value==='' && !previewDoc().querySelector('input[type="checkbox"]').checked);
  const basicPage=d.createElement('iframe'); basicPage.style.cssText='width:1440px;height:1000px;border:0';
  for (const theme of ['light','dark']) {
    input('jTheme',theme); await wait();
    const cssUrl=w.URL.createObjectURL(new w.Blob([evaluate('cssExport()')],{type:'text/css'}));
    const htmlUrl=w.URL.createObjectURL(new w.Blob([evaluate('htmlExport()').replace('href="tokens.css"','href="'+cssUrl+'"')],{type:'text/html'}));
    basicPage.src=htmlUrl;
    await new Promise(resolve=>{basicPage.onload=resolve;if(!basicPage.isConnected)d.body.append(basicPage);});
    const pd=basicPage.contentDocument, pw=basicPage.contentWindow;
    const footerDisclosure=pd.getElementById('footer-sitemap'),footerSummary=pd.getElementById('sitemap-toggle');
    test(theme+' Basic sitemap starts collapsed with a native disclosure and visible heading',()=>!footerDisclosure.open && footerSummary.tagName==='SUMMARY' && pw.getComputedStyle(footerSummary).display==='list-item' && footerSummary.getBoundingClientRect().height>=44 && pd.querySelector('#sitemap a').getBoundingClientRect().height===0);
    footerSummary.click();

    test(theme+' Basic standalone hero loads its current theme illustration without external assets', () => {
      const image=pd.querySelector('#home img');
      return image.complete && image.naturalWidth===960 && image.naturalHeight===720 && image.alt.length>0 && image.getAttribute('src')===evaluate('DSStudio.samples.illustration(palette().roles)');
    });
    for (const width of [320,390,768,1440]) {
      basicPage.style.width=width+'px'; await wait();
      test(theme+' Basic hamburger switches navigation at '+width+'px', () => {
        const menu=pd.getElementById('basic-menu'), desktop=pd.querySelector('.desktop-navigation');
        const links=nav=>[...nav.querySelectorAll('a')].map(link=>link.getAttribute('href')).join(',');
        const mobile=pd.querySelector('.mobile-navigation');
        menu.open=false;
        const narrow=width<=768;
        if (links(desktop)!==links(mobile) || pw.getComputedStyle(menu).display!==(narrow?'block':'none') || pw.getComputedStyle(desktop).display!==(narrow?'none':'block') || mobile.getClientRects().length) return false;
        if (!narrow) return true;
        const summary=menu.querySelector('summary'); summary.focus(); summary.click();
        const opened=menu.open && mobile.getClientRects().length>0 && pw.getComputedStyle(pd.querySelector('.menu-bars')).display==='none' && pw.getComputedStyle(pd.querySelector('.menu-close')).display!=='none' && summary.getBoundingClientRect().height>=44 && pw.getComputedStyle(summary).outlineStyle==='solid' && [...mobile.querySelectorAll('a')].every(link=>link.getBoundingClientRect().height>=44 && link.getBoundingClientRect().right<=width+1);
        summary.click();
        return opened && !menu.open && !mobile.getClientRects().length;
      });
      test(theme+' Basic toolkit is a conventional equal-width CSS Grid at '+width+'px', () => {
        const grid=pd.querySelector('.list-grid'), cards=[...grid.children], sizes=cards.map(card=>card.getBoundingClientRect());
        return pw.getComputedStyle(grid).display==='grid' && sizes.every(box=>Math.abs(box.width-sizes[0].width)<1 && box.right<=width+1) && cards.every(card=>pw.getComputedStyle(card).gridRowEnd==='auto') && (width===1440?sizes.every(box=>Math.abs(box.top-sizes[0].top)<1):true);
      });
      test(theme+' Basic hero image and text reflow at '+width+'px', () => {
        const layout=pd.querySelector('.hero-layout'), text=layout.firstElementChild.getBoundingClientRect(), image=pd.querySelector('#home img').getBoundingClientRect();
        return pw.getComputedStyle(layout).gridTemplateColumns.split(' ').length===(width<=768?1:2) && image.width>0 && Math.abs(image.width/image.height-4/3)<.01 && image.right<=width+1 && (width<=768 ? image.top>=text.bottom : image.left>=text.right);
      });
      test(theme+' Basic sitemap columns have vertically stacked child links at '+width+'px', () => {
        const groups=[...pd.querySelectorAll('#sitemap .sitemap-list > li')], children=[...pd.querySelectorAll('#sitemap .sitemap-list > li > ul')];
        const map=pd.querySelector('#sitemap'), grid=map.querySelector('.sitemap-list'), mapBox=map.getBoundingClientRect(), gridBox=grid.getBoundingClientRect();
        if (pw.getComputedStyle(pd.getElementById('sitemap-title')).textAlign!=='left' || pw.getComputedStyle(grid).justifyItems!=='center' || Math.abs((gridBox.left+gridBox.right)/2-(mapBox.left+mapBox.right)/2)>1) return false;
        return groups.length===4 && children.length===3 && children.every((list,index)=>{
          const style=pw.getComputedStyle(list), bounds=list.getBoundingClientRect(), links=[...list.querySelectorAll('a')], boxes=links.map(link=>link.getBoundingClientRect());
          return style.display==='flex' && style.flexDirection==='column' && pw.getComputedStyle(list.parentElement).textAlign==='center' && links.length===[3,4,1][index] && boxes.every((box,i)=>box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44 && Math.abs((box.left+box.right)/2-(bounds.left+bounds.right)/2)<1 && (!i||box.top>=boxes[i-1].bottom-1));
        }) && (width!==1440||groups.every(group=>Math.abs(group.getBoundingClientRect().top-groups[0].getBoundingClientRect().top)<1)) && pd.documentElement.scrollWidth<=width+1;
      });
      test(theme+' Basic content/sidebar layout and UI components fit at '+width+'px', () => {
        const layout=pd.querySelector('.content-sidebar'), children=[...layout.children], boxes=children.map(el=>el.getBoundingClientRect());
        return pw.getComputedStyle(layout).gridTemplateColumns.split(' ').length===(width<=768?1:2) && (width<=768?boxes[1].top>=boxes[0].bottom:boxes[1].left>=boxes[0].right && boxes[0].width>boxes[1].width) && [...pd.querySelectorAll('.component-demo, .content-sidebar > *, #signup select, #signup textarea, #signup fieldset')].every(el=>el.getBoundingClientRect().right<=width+1 && el.getBoundingClientRect().width>0) && pw.getComputedStyle(pd.querySelector('.media-object')).display==='flex' && pd.querySelector('.avatar[aria-hidden="true"]') && pd.querySelector('.badge').textContent==='Available';
      });
      test(theme+' Basic section actions wrap inside their containers at '+width+'px', () => [...pd.querySelectorAll('.section-actions')].every(pair=>{
        const bounds=pair.getBoundingClientRect();
        return parseFloat(pw.getComputedStyle(pair).gap)>0 && [...pair.children].every(action=>{const box=action.getBoundingClientRect();return box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44;});
      }));
      test(theme+' Basic sections have distinct responsive compositions at '+width+'px', () => {
        const columns=selector=>pw.getComputedStyle(pd.querySelector(selector)).gridTemplateColumns.split(' ').length;
        const skills=pd.querySelector('.skills-intro').getBoundingClientRect(), lessons=pd.querySelector('.skill-cards').getBoundingClientRect();
        const form=pd.querySelector('.signup-form').getBoundingClientRect(), area=pd.querySelector('.signup-layout').getBoundingClientRect();
        return pw.getComputedStyle(pd.querySelector('.skills-layout')).display==='flex' && pw.getComputedStyle(pd.querySelector('.skills-layout')).flexDirection===(width<=768?'column':'row') && pw.getComputedStyle(pd.querySelector('.skill-cards')).display==='flex' && [...pd.querySelectorAll('#features *')].every(el=>!['grid','inline-grid'].includes(pw.getComputedStyle(el).display)) && columns('.signup-layout')===1 && (width<=768?lessons.top>=skills.bottom:lessons.left>=skills.right) && Math.abs((form.left+form.right)/2-(area.left+area.right)/2)<2 && pw.getComputedStyle(pd.querySelector('.signup-form')).maxWidth!=='none' && pd.querySelector('.hero-image figcaption');
      });
      test(theme+' Basic classic footer keeps its layout inside the open sitemap disclosure at '+width+'px', () => {
        const footer=pd.querySelector('.site-footer'), layout=footer.querySelector('.footer-inner');
        const identity=layout.querySelector('.footer-identity').getBoundingClientRect(), nav=layout.querySelector('nav').getBoundingClientRect(), links=[...layout.querySelectorAll('nav a')];
        return layout.children.length===2 && pw.getComputedStyle(layout).display==='grid' && footer.querySelector('.footer-brand') && !footer.querySelector('.footer-lesson') && footer.querySelectorAll('nav').length===2 && footer.querySelector('#sitemap').tagName==='NAV' && pw.getComputedStyle(footer.querySelector('.sitemap-list')).display==='grid' && (width<=768?nav.top>=identity.bottom:nav.left>=identity.right && Math.abs(nav.top-identity.top)<1) && (width!==1440||links.every(link=>Math.abs(link.getBoundingClientRect().top-links[0].getBoundingClientRect().top)<1)) && footer.querySelector('details').open && [...footer.querySelectorAll('a')].every(link=>link.getBoundingClientRect().height>=44);
      });
      test(theme+' Basic standalone page reflows with its separate stylesheet at '+width+'px', () => {
        const grid=pd.querySelector('.skill-cards'), cards=[...grid.children], first=cards[0].getBoundingClientRect();
        const columns=cards.filter(card=>Math.abs(card.getBoundingClientRect().top-first.top)<1).length;
        return pd.querySelector('link').sheet && !pd.querySelector('style,script') && pd.documentElement.scrollWidth<=width+1 && !pd.querySelector('.lesson-code') && columns===1 && pw.getComputedStyle(grid).display==='flex' && pw.getComputedStyle(pd.querySelector('.signup-layout')).gridTemplateColumns.split(' ').length===1 && [...pd.querySelectorAll('header nav a, footer nav[aria-label="Footer navigation"] a, .button')].filter(el=>el.getClientRects().length).every(el=>el.getBoundingClientRect().height>=44);
      });
    }
    pd.querySelector('#basic-faq summary').focus(); pd.querySelector('#basic-faq summary').click();
    test(theme+' Basic native FAQ opens with a visible focus outline and no scripts', () => pd.getElementById('basic-faq').open && pw.getComputedStyle(pd.querySelector('#basic-faq summary')).outlineStyle==='solid' && !pd.querySelector('script'));
    pd.querySelector('#basic-faq summary').click();
    pd.querySelector('.site-footer .sitemap-list > li > a[href="#features"]').click(); await wait();
    test(theme+' Basic footer Services link reaches its real section', () => pw.location.hash==='#features' && pd.getElementById('features').getBoundingClientRect().top>=-1);
    test(theme+' Basic standalone sitemap expands without scripts and has real destinations', () => pd.getElementById('sitemap').tagName==='NAV' && footerDisclosure.open && [...pd.querySelectorAll('#sitemap a')].every(link=>link.getBoundingClientRect().height>=44 && pd.getElementById(link.hash.slice(1))));
    pd.querySelector('.skip-link').focus();
    test(theme+' Basic skip link and focus outline are visible with keyboard focus', () => pd.activeElement===pd.querySelector('.skip-link') && pd.activeElement.getBoundingClientRect().top>=0 && pw.getComputedStyle(pd.activeElement).outlineStyle==='solid');
    pd.querySelector('.back-to-top').click(); await wait();
    test(theme+' Basic standalone Back to top uses a real native fragment destination', () => pw.location.hash==='#top' && pd.getElementById('top').getBoundingClientRect().top>=-1 && pd.getElementById('top').getBoundingClientRect().top<10);
    w.URL.revokeObjectURL(cssUrl); w.URL.revokeObjectURL(htmlUrl);
  }
  basicPage.remove();
  evaluate('importConfig({sampleMode:"<script>",project:"<img src=x onerror=alert(1)>"})');
  test('Invalid sample mode falls back to Basic', () => evaluate('state.sampleMode')==='basic');
  evaluate('importConfig({sampleMode:"basic",project:"<img src=x onerror=alert(1)>"})');
  test('Basic escapes imported project text in its title and brand', () => {
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return page.querySelectorAll('img').length===1 && page.querySelector('#home img').getAttribute('src').startsWith('data:image/svg+xml;') && !page.querySelector('script,[onerror]') && page.querySelector('.brand').textContent.includes('<img src=x onerror=alert(1)>');
  });
  evaluate('importConfig({})'); await wait();
  test('Legacy projects without a sample mode retain Advanced', () => evaluate('state.sampleMode')==='advanced' && d.getElementById('dockModeAdvanced').getAttribute('aria-selected')==='true');
  d.getElementById('dockModeAdvanced').click(); evaluate('resetStudio()'); await wait();
  test('Reset restores Basic mode and its matching preview and exports', () => evaluate('state.sampleMode')==='basic' && previewDoc().querySelector('.skill-cards') && !previewDoc().querySelector('#design-process') && evaluate('htmlExport()').includes('skill-cards') && d.getElementById('sampleModeHelp').textContent.startsWith('Basic'));
  d.getElementById('dockModeAdvanced').click();await wait();
  await prepare();
  // The following standalone list layout uses a complete Basic custom outline.
  app.style.width='1440px';reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1,false);input('plan-pages',w.DSStudio.process.samplePages('basic'));await wait();
  const listsPage=d.createElement('iframe'); listsPage.style.cssText='width:1440px;height:1000px;border:0';
  listsPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
  await new Promise(resolve=>{listsPage.onload=resolve;d.body.append(listsPage);});
  for (const width of [320,390,1440]) {
    listsPage.style.width=width+'px'; await wait();
    test('Basic list cards and sitemap fit at '+width+'px', () => {
      const pd=listsPage.contentDocument, cards=[...pd.querySelectorAll('#lists .list-grid > article')], boxes=cards.map(card=>card.getBoundingClientRect());
      return pd.documentElement.scrollWidth<=width+1 && boxes.every(box=>box.left>=0 && box.right<=width+1) && (width===1440?(Math.abs(boxes[1].top-boxes[0].top)<1 && boxes[1].left>=boxes[0].right && Math.abs(boxes[2].top-boxes[0].top)<1 && boxes[2].left>=boxes[1].right):(boxes[1].top>=boxes[0].bottom && boxes[2].top>=boxes[1].bottom));
    });
  }
  listsPage.remove();
  for (const mode of ['basic','advanced']) {
    evaluate('importConfig('+JSON.stringify({sampleMode:mode,designProcess:{pages:'Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact'}})+')'); await wait();
    test(mode+' old starter upgrades to the complete map without planned placeholders', () => d.getElementById('plan-pages').value===w.DSStudio.process.samplePages(mode) && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  }
  reset(); await wait();
  const systemPage=d.createElement('iframe'); systemPage.style.cssText='width:1440px;height:1000px;border:0';
  for (const edited of [false,true]) {
    if (edited) {
      for (const [id,value,type] of [['jSpacing',6],['jBase',20],['jRatio',1.25],['advMeasure',52],['advBorder',2],['advHeight',56],['advShadow','strong','change'],['advOpacity',72],['advAlign','center','change'],['advFocus',5],['bdPaddingX',28],['bdPaddingY',14],['bdRadius',18],['bdMinHeight',60],['bdWeight',600],['bdSize','lg'],['bdVariant','primary'],['bdDefaultBg','#602d54'],['bdText','#ffffff']]) input(id,value,type||'input');
      const editedProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+editedProject+')'); await wait();
    }
    for (const theme of ['light','dark']) {
      input('jTheme',theme); await wait();
      const signatures=[];
      for (const mode of ['advanced','basic']) {
        d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
        const css=evaluate('cssExport()');
        systemPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+css+'</style>');
        await new Promise(resolve=>{systemPage.onload=resolve;if(!systemPage.isConnected)d.body.append(systemPage);});
        const pd=systemPage.contentDocument,pw=systemPage.contentWindow;
        const style=selector=>pw.getComputedStyle(pd.querySelector(selector));
        const signature={body:style('body').font,h1:style('h1').font,h2:style('main h2').font,h3:style('main h3').font,padding:style('.card').padding,border:style('.card').border,shadow:style('.card').boxShadow,opacity:style('.card').opacity,measure:style('.card p:last-of-type').maxWidth,input:style('.input').minHeight,inputPadding:style('.input').padding,button:style('#home .ds-button').padding,buttonHeight:style('#home .ds-button').minHeight,buttonRadius:style('#home .ds-button').borderRadius,buttonWeight:style('#home .ds-button').fontWeight,buttonBackground:style('#home .ds-button').backgroundColor,buttonText:style('#home .ds-button').color,align:style(mode==='basic'?'.skill-cards':'.card-grid').alignItems,footerPadding:style('.footer-inner').padding,footerLinkWeight:style(mode==='basic'?'.sitemap-list > li > a':'.footer-links a').fontWeight,navFont:style('header nav a').font,navDecoration:style('header nav a').textDecorationLine,background:style('body').backgroundColor};
        signatures.push(signature);
        test(mode+' '+theme+' '+(edited?'edited/imported':'default')+' follows system dimensions in standalone CSS',()=> css.startsWith(w.DSStudio.samples.foundationCss()) && signature.padding===(edited?'36px':'24px') && signature.input===(edited?'56px':'48px') && signature.opacity===(edited?'0.72':'1') && signature.align===(edited?'center':'stretch') && Math.abs(parseFloat(style('h1').fontSize)-evaluate('fluidTypePx(5,1440)'))<.2 && (!edited || (Math.abs(parseFloat(signature.button)-17.08)<.02 && signature.buttonRadius==='18px' && signature.buttonBackground==='rgb(96, 45, 84)' && signature.buttonText==='rgb(255, 255, 255)' && signature.shadow!=='none')));
        if (mode==='basic') test(theme+' Basic sign-up width follows the '+(edited?'edited/imported':'default')+' reading measure',()=>style('.signup-form').maxWidth!=='none' && style('.signup-form').maxWidth===signature.measure);
        const previewStyle=previewWindow().getComputedStyle(previewDoc().querySelector('.card'));
        test(mode+' preview and inspector use the same edited system as downloads',()=>previewStyle.padding===signature.padding && previewStyle.opacity===signature.opacity && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()'));
        const map=pd.getElementById('sitemap');
        const footerDisclosure=pd.getElementById('footer-sitemap'),footerSummary=pd.getElementById('sitemap-toggle');
        test(mode+' '+theme+' sitemap starts collapsed in standalone export',()=>!footerDisclosure.open && footerSummary.tagName==='SUMMARY' && pw.getComputedStyle(footerSummary).display==='list-item' && footerSummary.getBoundingClientRect().height>=44 && map.getBoundingClientRect().height===0);
        footerSummary.click();

        test(mode+' footer presents its sitemap and working return destination',()=> map.tagName==='NAV' && map.closest('details').open && pw.getComputedStyle(pd.getElementById('sitemap-title')).textAlign==='left' && pd.querySelector('.footer-bottom a[href="#top"]') && pd.getElementById('top'));
        test(mode+' footer sitemap works without JavaScript and keeps all destinations valid',()=> map.tagName==='NAV' && [...map.querySelectorAll('a')].every(a=>a.getBoundingClientRect().height>=44 && pd.getElementById(a.hash.slice(1))));
        footerSummary.focus();
        test(mode+' '+theme+' sitemap summary retains the shared visible focus ring',()=>pd.activeElement===footerSummary && pw.getComputedStyle(footerSummary).outlineStyle==='solid' && pw.getComputedStyle(footerSummary).outlineWidth===style(':root').getPropertyValue('--button-focus-width').trim());
        footerSummary.click();
        test(mode+' '+theme+' sitemap heading collapses its content while remaining available',()=>!footerDisclosure.open && map.getBoundingClientRect().height===0 && footerSummary.getBoundingClientRect().height>=44);
        footerSummary.click();

        for (const width of [320,390,1440]) {
          systemPage.style.width=width+'px'; await wait();
          const menu=pd.querySelector('.basic-menu, .sample-menu'); if(menu)menu.open=width<=768;
          const navLink=pd.querySelector(mode==='basic'?(width<=768?'.mobile-navigation a':'.desktop-navigation a'):width<=768?'.sample-mobile-navigation a':'.sample-desktop-navigation a');
          test(mode+' '+theme+' navigation matches Advanced text at '+width+'px '+(edited?'edited':'default'),()=>{
            const ns=pw.getComputedStyle(navLink), live=previewWindow().getComputedStyle(previewDoc().querySelector('header nav a'));
            return ns.fontWeight==='600' && ns.fontFamily===style('body').fontFamily && ns.fontSize===style('body').fontSize && ns.textDecorationLine==='none' && live.fontWeight==='600' && live.textDecorationLine==='none' && navLink.getBoundingClientRect().height>0;
          });
          navLink.focus();
          test(mode+' navigation retains the Advanced focus ring at '+width+'px',()=>pd.activeElement===navLink && pw.getComputedStyle(navLink).outlineStyle==='solid' && pw.getComputedStyle(navLink).outlineWidth===style(':root').getPropertyValue('--button-focus-width').trim());
          test(mode+' '+theme+' footer fits '+width+'px '+(edited?'edited':'default'),()=>pd.documentElement.scrollWidth<=width+1 && [...pd.querySelectorAll('.website-footer a')].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && box.height>=44;}) && [...map.querySelectorAll('.sitemap-list > li')].every(group=>pw.getComputedStyle(group).textAlign==='center') && [...map.querySelectorAll('.sitemap-list ul')].every(list=>{const bounds=list.getBoundingClientRect();return pw.getComputedStyle(list).flexDirection==='column' && [...list.querySelectorAll('a')].every(link=>{const box=link.getBoundingClientRect();return Math.abs((box.left+box.right)/2-(bounds.left+bounds.right)/2)<1;});}));
        }
        systemPage.style.width='1440px'; await wait();
      }
      test(theme+' '+(edited?'edited/imported':'default')+' Basic and Advanced share typography, spacing, components and footer styles',()=>JSON.stringify(signatures[0])===JSON.stringify(signatures[1]));
    }
  }
  systemPage.remove(); reset(); await wait();
  reset(); await wait();
  await prepare();
  // Sitemap disclosure retains its existing grid/navigation and browsing state.
  for (const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();await wait();
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    const footerDocument=previewDoc();
    test(mode+' live sitemap starts collapsed without changing its saved plan',()=>!previewDoc().getElementById('footer-sitemap').open && previewDoc().getElementById('sitemap').tagName==='NAV' && previewDoc().getElementById('sitemap').getAttribute('aria-labelledby')==='sitemap-title');
    previewDoc().getElementById('sitemap-toggle').click();previewDoc().getElementById('sitemap-toggle').focus();
    input('jAccent','#246a68');await wait();
    test(mode+' open sitemap and summary focus survive live palette rendering',()=>previewDoc()===footerDocument && previewDoc().getElementById('footer-sitemap').open && previewDoc().activeElement.id==='sitemap-toggle');
    input('jTheme','dark');await wait();
    test(mode+' sitemap stays open across theme updates',()=>previewDoc().getElementById('footer-sitemap').open);
    previewDoc().getElementById('sitemap-toggle').click();input('jRadius',18);await wait();
    test(mode+' collapsed sitemap stays collapsed after CSS edits',()=>!previewDoc().getElementById('footer-sitemap').open && !evaluate('projectJson()').includes('footer-sitemap'));
    const footerFragment=previewDoc().createElement('a');footerFragment.href='#sitemap';footerFragment.textContent='Review sitemap';previewDoc().body.append(footerFragment);footerFragment.click();await wait();
    test(mode+' preview fragment navigation reveals the collapsed sitemap destination',()=>previewDoc().getElementById('footer-sitemap').open && previewDoc().activeElement===previewDoc().getElementById('sitemap'));
    footerFragment.remove();
    const accordionPage=d.createElement('iframe'),accordionUrl=w.URL.createObjectURL(new w.Blob([evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>')],{type:'text/html'}));
    accordionPage.src=accordionUrl;await new Promise(resolve=>{accordionPage.onload=resolve;d.body.append(accordionPage);});
    const fd=accordionPage.contentDocument,fw=accordionPage.contentWindow,disclosure=fd.getElementById('footer-sitemap');
    fw.location.hash='sitemap';await wait();
    test(mode+' standalone native fragment reveals the map without a script',()=>disclosure.open && !fd.querySelector('script') && fw.location.hash==='#sitemap');
    fd.getElementById('sitemap-toggle').click();
    test(mode+' standalone summary can collapse the fragment-revealed map',()=>!disclosure.open && fd.getElementById('sitemap').getBoundingClientRect().height===0);
    accordionPage.remove();w.URL.revokeObjectURL(accordionUrl);
  }
  reset();await wait();
  test('No standalone exports JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Focused harness completed',pass:false,error:String(error.stack||error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
