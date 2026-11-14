'use strict';
/* One set of theme overrides drives controls, lessons, preview and exports. */
DSStudio.register({
  id: 'webpage-backgrounds', title: 'Body, Header, Main and Footer backgrounds',
  init() {
    const get = id => document.getElementById(id);
    const regions = ['body', 'header', 'main', 'footer'];
    const title = value => value[0].toUpperCase() + value.slice(1);
    const keyFor = region => region === 'body' ? 'background' : region + '-background';
    const controls = regions.map(region => ({ id: region === 'body' ? 'page-background' : region + '-background', key: keyFor(region), label: title(region) }));
    get('webpage-region-controls').innerHTML = controls.slice(1).map(({id, label}) => `<fieldset class="background-region">
      <legend>${label} background</legend>
      <label for="${id}-brand">${label} · Brand or Neutral Palette</label><select id="${id}-brand"></select>
      <label for="${id}-colour">${label} custom colour</label><input id="${id}-colour" type="color">
      <label for="${id}-hex">${label} hex colour</label><input id="${id}-hex" type="text" maxlength="7" pattern="#[0-9A-Fa-f]{6}" aria-describedby="${id}-current">
      <label for="${id}-opacity">${label} background opacity <output id="${id}-opacity-value">100%</output></label><input id="${id}-opacity" type="range" min="0" max="100" step="1" value="100" aria-describedby="background-opacity-help">
      <p id="${id}-current" class="help"></p><button id="${id}-reset" type="button" class="ghost">Use default ${label.toLowerCase()} background</button>
    </fieldset>`).join('');

    const lesson = document.createElement('section');
    lesson.id = 'webpage-background-lesson';
    lesson.className = 'webpage-background-lesson';
    lesson.setAttribute('aria-labelledby', 'webpage-background-lesson-title');
    lesson.innerHTML = `<h4 id="webpage-background-lesson-title">Webpage backgrounds</h4>
      <p>Start with your Brand Palette, assign the Main Palette, then choose Body, Header, Main and Footer backgrounds. Body is the outer canvas containing the three page regions. These are separate decisions from button and card colours.</p>
      <p id="background-lesson-theme"></p>
      <div class="background-page-model" aria-label="Current webpage background colours"></div>
      <p>Try a brand colour for Body, then choose a different Main background to see the distinction. Compare the responsive preview, switch themes and inspect the generated files. Header and Footer default to Surface; Main follows Body until overridden. Reset a region to follow that default again.</p>
      <p>Background opacity changes only the paint behind content. Body blends over an opaque Surface canvas; Header, Main and Footer blend over Body. Text and controls keep their own opacity. The ratios below use the resulting blended colours; check focus and interactive states in Accessibility.</p>`;
    const model = lesson.querySelector('.background-page-model');
    let innerRegions;
    for (const region of regions) {
      const card = document.createElement('section');
      card.className = 'background-model-region';
      card.innerHTML = `<h5>${title(region)}</h5><code id="${region}-background-value"></code><p><code id="${region}-background-opacity-code"></code></p><p id="${region}-background-composite" class="help"></p><p id="${region}-background-contrast"></p><div class="button-row"><button type="button" class="ghost" data-background-inspect="css">Inspect ${title(region)} CSS</button><button type="button" class="ghost" data-background-inspect="html">Inspect ${title(region)} HTML</button></div>`;
      if(region!=='body') {
        const padding=document.createElement('div');padding.className='region-padding-example';
        padding.innerHTML=`<p><strong>Region padding</strong> · top / right / bottom / left</p><p><code id="${region}-padding-code"></code></p><p class="help">The inset below shows the extra region padding. Existing page gutters and component spacing remain.</p><div id="${region}-padding-demo" class="region-padding-demo"><span>Content</span></div><button type="button" class="ghost">Inspect padding CSS</button>`;
        padding.querySelector('button').addEventListener('click',()=>DSStudio.inspector.show({language:'css',section:'all',find:'--'+region+'-padding-top:'}));
        card.insertBefore(padding,card.querySelector('.button-row'));
      }
      for (const button of card.querySelectorAll('[data-background-inspect]')) button.addEventListener('click', () => {
        const language = button.dataset.backgroundInspect;
        DSStudio.inspector.show({language, section:'all', find:language==='css'?'--'+keyFor(region)+':':'<'+region});
      });
      if (region === 'body') {
        card.classList.add('background-model-body');
        const explanation = document.createElement('p');
        explanation.textContent = 'Body contains Header, Main and Footer. Its background shows around the page content; opaque region and card backgrounds cover it.';
        innerRegions = document.createElement('div');
        innerRegions.className = 'background-contained-regions';
        card.append(explanation, innerRegions);
        model.append(card);
      } else innerRegions.append(card);
    }
    get('brandPalette').querySelector('.studio-lesson').append(lesson);
    // Surface decisions come before interaction-state colour decisions in both panes.
    document.querySelector('.page-background-editor').after(get('interaction-palette-controls'));
    lesson.after(get('interaction-palette-lesson'));
    let brandSignature = '';
    const set = (key, value) => {
      if (!validHex(value)) return;
      state.semanticOverrides = {...state.semanticOverrides, [state.theme]:{...state.semanticOverrides?.[state.theme], [key]:value.toUpperCase()}};
      apply();
    };
    for (const {id, key} of controls) {
      const region=id==='page-background'?'body':id.split('-')[0];
      if(region!=='body') {
        const details=document.createElement('details');details.className='region-padding-controls';details.id=region+'-padding-controls';
        details.innerHTML=`<summary id="${region}-padding-summary">${title(region)} padding</summary><p class="help" id="${region}-padding-help">Extra space inside ${title(region)}, shared across themes and samples. Existing content gutters and section spacing still apply. Order: top, right, bottom, left. Each side is 0–64 px.</p>`+PADDING_SIDES.map(side=>`<label for="${region}-padding-${side}">${title(side)} padding <output id="${region}-padding-${side}-value">0 px</output></label><input id="${region}-padding-${side}" type="range" min="0" max="64" step="1" value="0" aria-describedby="${region}-padding-help">`).join('')+`<button id="${region}-padding-reset" type="button" class="ghost">Reset ${region} padding</button>`;
        get(id+'-reset').after(details);
        for(const side of PADDING_SIDES)get(region+'-padding-'+side).addEventListener('input',event=>{
          const value=Number(event.target.value);if(!Number.isFinite(value))return;
          state.regionPadding={...state.regionPadding,[region]:{...state.regionPadding?.[region],[side]:Math.round(clamp(value,0,64))}};apply();
        });
        get(region+'-padding-reset').addEventListener('click',()=>{if(state.regionPadding)delete state.regionPadding[region];apply();});
      }
      get(id+'-opacity').addEventListener('input',event=>{
        const value=Number(event.target.value);if(!Number.isFinite(value))return;
        state.backgroundOpacity={...state.backgroundOpacity,[state.theme]:{...state.backgroundOpacity?.[state.theme],[region]:Math.round(clamp(value,0,100))}};
        apply();
      });
      get(id+'-colour').addEventListener('input', event => {get(id+'-hex').value=event.target.value.toUpperCase();set(key,event.target.value);});
      get(id+'-hex').addEventListener('input', event => {
        const value=event.target.value;
        event.target.setAttribute('aria-invalid', String(!validHex(value)));
        set(key,value);
      });
      get(id+'-brand').addEventListener('change', event => {
        if (validHex(event.target.value)) {get(id+'-hex').value=event.target.value;set(key,event.target.value);}
      });
      get(id+'-reset').addEventListener('click', () => {
        if (state.semanticOverrides?.[state.theme]) delete state.semanticOverrides[state.theme][key];
        if (state.backgroundOpacity?.[state.theme]) delete state.backgroundOpacity[state.theme][region];
        get(id+'-hex').removeAttribute('aria-invalid');
        get(id+'-hex').value=palette().roles[key];
        apply();
      });
    }
    function sync() {
      const {roles,n} = palette(), items = DSStudio.brandPalette.normalize(state.brandPalette);
      const layers=backgroundLayers(state.theme,state,roles);
      const next=JSON.stringify([items,n]);
      if (next!==brandSignature) {
        brandSignature=next;
        for (const {id} of controls) {
          const neutrals=document.createElement('optgroup');neutrals.label='Neutral palette · from Primary UI';
          neutrals.append(...steps.map(step=>new Option(`Neutral ${step} · ${n[step]} (--neutral-${step})`,n[step])));
          get(id+'-brand').replaceChildren(new Option('Custom colour (use picker or hex)', ''), ...items.map(item => new Option(`${item.name} · ${item.hex}`, item.hex)),neutrals);
        }
      }
      const theme=state.theme==='dark'?'Dark':'Light';
      get('background-lesson-theme').textContent=theme+' theme · changes apply to both Basic and Advanced samples.';
      model.style.backgroundColor=roles.surface;
      for (const {id, key} of controls) {
        const region=id==='page-background'?'body':id.split('-')[0],alpha=backgroundOpacity(region);
        const colour=roles[key], hex=get(id+'-hex');
        get(id+'-colour').value=colour;
        if (document.activeElement!==hex) {hex.value=colour;hex.removeAttribute('aria-invalid');}
        else if (validHex(hex.value)) hex.removeAttribute('aria-invalid');
        get(id+'-brand').value=items.some(item=>item.hex===colour)||Object.values(n).includes(colour)?colour:'';
        get(id+'-opacity').value=String(Math.round(alpha*100));
        get(id+'-opacity-value').textContent=Math.round(alpha*100)+'%';
        get(id+'-opacity').setAttribute('aria-valuetext',Math.round(alpha*100)+'% opaque');
        get(id+'-reset').disabled=!state.semanticOverrides?.[state.theme]?.[key] && alpha===1;
        get(id==='page-background'?'page-background-theme':id+'-current').textContent=`${theme} theme · ${colour} · ${state.semanticOverrides?.[state.theme]?.[key]?'custom choice':'default'}`;
      }
      for (const region of regions) {
        if(region!=='body') {
          const values=PADDING_SIDES.map(side=>regionPadding(region,side));
          for(const [index,side] of PADDING_SIDES.entries()) {
            get(region+'-padding-'+side).value=String(values[index]);
            get(region+'-padding-'+side+'-value').textContent=values[index]+' px';
            get(region+'-padding-'+side).setAttribute('aria-valuetext',values[index]+' pixels');
          }
          get(region+'-padding-summary').textContent=title(region)+' padding · '+values.join(' / ')+' px';
          get(region+'-padding-reset').disabled=values.every(value=>value===0);
          get(region+'-padding-code').textContent=PADDING_SIDES.map((side,index)=>`--${region}-padding-${side}: ${values[index]}px;`).join(' ');
          get(region+'-padding-demo').style.padding=values.map(value=>value+'px').join(' ');
        }
        const key=keyFor(region), colour=roles[key];
        // Validated colours only; imported names never become HTML or selectors.
        const alpha=backgroundOpacity(region);
        get(region+'-background-value').closest('section').style.backgroundColor=`rgb(${hexRgb(colour).join(' ')} / ${alpha})`;
        get(region+'-background-value').textContent=`--${key}: ${colour};`;
        get(region+'-background-opacity-code').textContent=`--${region}-background-opacity: ${alpha};`;
        const visible=rgbHex(layers[region]);
        get(region+'-background-composite').textContent=`${Math.round(alpha*100)}% opaque · blended background ${visible}`;
        const text=contrast(roles.text,visible), link=contrast(roles.primary,visible);
        get(region+'-background-contrast').textContent=`Text ${text.toFixed(2)}:1 · Links ${link.toFixed(2)}:1 · ${text>=4.5&&link>=4.5?'both meet 4.5:1':'review text/link contrast'}`;
      }
    }
    DSStudio.on('foundation:updated',sync);
    sync();
    DSStudio.emit('lesson:content');
  }
});
