'use strict';
/* Teach the tokens produced by the shared export, without a second generator. */
DSStudio.register({
  id:'palette-process', title:'Brand tokens, Main Palette steps and semantic roles',
  init() {
    const get=id=>document.getElementById(id);
    const roles=[['primary','Primary'],['secondary','Supporting'],['accent','Accent'],['neutral','Neutral']];
    const lesson=document.createElement('section'); lesson.id='palette-token-lesson';lesson.className='palette-token-lesson';
    lesson.setAttribute('aria-labelledby','palette-token-lesson-title');
    lesson.innerHTML='<h4 id="palette-token-lesson-title">From brand colours to design tokens</h4><ol class="palette-process-steps"><li><strong>Name the brand colour and its token.</strong> A display name describes the colour; a token gives its value a reusable CSS name. Edit Brand Palette to set the suffix after <code>--brand-</code>.</li><li><strong>Assign Main Palette roles.</strong> Primary, Supporting and Accent copy a selected brand value, or accept a custom colour. Matching values do not create a live alias.</li><li><strong>Generate shade tokens.</strong> Each anchor produces eleven named steps. Step 500 is the exact anchor; other steps follow RGB mix or OKLCH. Neutral borrows the Primary UI hue with a restrained tint and uses its own derived midpoint.</li><li><strong>Apply semantic roles.</strong> Light and dark themes choose shades for a purpose, such as <code>--primary</code>. Custom semantic overrides take precedence. Inspect the resolved values before using them.</li></ol><div id="palette-brand-token-list" class="palette-brand-token-list"></div><p id="palette-method-status"></p><div id="palette-ramp-lessons"></div><p>Use these decisions in Body, Header, Main and Footer backgrounds below. Shade numbers describe a ramp; they do not certify contrast. Review foreground/background pairs in both themes.</p>';
    get('brandPalette').querySelector('.studio-lesson').append(lesson);
    const statusLesson=document.createElement('section');statusLesson.id='status-palette-lesson';statusLesson.className='palette-token-lesson';
    statusLesson.setAttribute('aria-labelledby','status-palette-lesson-title');
    statusLesson.innerHTML='<h4 id="status-palette-lesson-title">Generate state palette steps</h4><p>Success confirms a completed task; Warning highlights a condition needing attention; Danger communicates an error or destructive action. Start with a meaningful semantic colour, generate its shade tokens, then choose foreground/background pairs for feedback. An invalid input uses Danger; a successful input uses Success.</p><p>Each theme generates its own eleven steps from its resolved status colour. Step 500 preserves that colour, including custom overrides. These ramps offer shades for application; generating them keeps existing component state mappings unchanged. Hover, pressed, focus, selected, disabled, loading and read-only retain their component tokens and native behaviour. Include text or icons, check contrast and test real interactions.</p><div id="status-palette-ramp-lessons"></div>';
    lesson.append(statusLesson);
    get('palette-brand-token-list').tabIndex=0;
    get('palette-brand-token-list').setAttribute('aria-label','Brand token declarations');
    const views=[];
    function addRamp(container,role,label,compact,status=false) {
      const article=document.createElement(compact?'details':'section'); article.className='palette-ramp';article.dataset.paletteRole=role;
      const heading=document.createElement(compact?'summary':'h5'); heading.textContent=label+' palette steps';article.append(heading);
      const anchor=document.createElement('p');anchor.className='help';article.append(anchor);
      const list=document.createElement('ol');list.className='palette-step-list';list.setAttribute('aria-label',label+' shade tokens');
      const rows=steps.map(step=>{
        const li=document.createElement('li'),chip=document.createElement('span'),code=document.createElement('code');
        chip.className='brand-palette-chip';chip.setAttribute('aria-hidden','true');li.dataset.shade=String(step);li.append(chip,code);list.append(li);return {step,li,chip,code};
      });article.append(list);
      const chain=document.createElement('p');chain.className='palette-token-chain';article.append(chain);
      const actions=document.createElement('div');actions.className='button-row';
      for(const [label,find] of [['Inspect shade CSS','--'+role+'-500:'],[role==='neutral'?'Inspect background CSS':'Inspect semantic CSS',role==='neutral'?'--background:':'--'+role+':']]) {
        const button=document.createElement('button');button.type='button';button.className='ghost';button.textContent=label;button.addEventListener('click',()=>DSStudio.inspector.show({language:'css',section:'all',find}));actions.append(button);
      }
      if(status) {
        const configure=document.createElement('button');configure.type='button';configure.className='ghost';configure.textContent='Configure '+label+' colour';
        configure.addEventListener('click',()=>window.dssConfigureToken({name:'--'+role,scope:state.theme==='dark'?'Dark':'Light / base'}));actions.append(configure);
      }
      article.append(actions);container.append(article);views.push({role,anchor,rows,chain,status});
    }
    for(const [role,label] of roles) {
      addRamp(get('main-palette-steps'),role,label,true);
      addRamp(get('palette-ramp-lessons'),role,label,false);
    }
    for(const role of STATUS_PALETTE_ROLES) {
      const label=role[0].toUpperCase()+role.slice(1);
      addRamp(get('status-palette-steps'),role,label,true,true);
      addRamp(get('status-palette-ramp-lessons'),role,label,true,true);
    }
    let signature='',brandSignature='';
    function sync() {
      const next=JSON.stringify([state.brandPalette,state.primary,state.secondary,state.accent,state.method,state.semanticOverrides,state.theme]);
      if(next===signature)return;signature=next;
      const tokens=window.dssReadTokens();
      const value=(name,theme='light')=>tokens.find(row=>row.name===name && (theme==='dark'?row.scope==='Dark':row.scope!=='Dark'))?.value;
      const brands=DSStudio.brandPalette.normalize(state.brandPalette);
      const nextBrands=JSON.stringify(brands);
      if(nextBrands!==brandSignature) {
        brandSignature=nextBrands;
        get('palette-brand-token-list').replaceChildren(...brands.map(item=>{
          const p=document.createElement('p'),name=document.createElement('span'),code=document.createElement('code');
          name.textContent=item.name+' → ';code.textContent=`--brand-${item.id}: ${value('--brand-'+item.id)};`;p.append(name,code);return p;
        }));
      }
      get('palette-method-status').textContent='Current generation method: '+(state.method==='oklch'?'OKLCH':'RGB mix')+'. Neutral borrows the Primary UI hue at reduced chroma. The values below come from the current exported CSS.';
      get('neutralPaletteAnchor').textContent='--neutral-500: '+value('--neutral-500')+'; · derived from Primary UI '+state.primary.toUpperCase();
      get('status-palette-theme').textContent='Showing '+(state.theme==='dark'?'Dark':'Light')+' theme status steps. Compare both themes before applying feedback colours.';
      for(const view of views) {
        const neutral=view.role==='neutral';
        const theme=view.status?state.theme:'light';
        const hex=view.status?value('--'+view.role,theme):neutral?value('--neutral-500'):state[view.role].toUpperCase(),matches=brands.filter(item=>item.hex===hex);
        view.anchor.textContent=view.status?`${theme==='dark'?'Dark':'Light'} theme anchor ${hex} · --${view.role} → --${view.role}-500. Configure its semantic colour to regenerate the steps.`:neutral?`Derived midpoint ${hex} · from Primary UI ${state.primary.toUpperCase()} with a restrained tint. No separate colour assignment.`:`Anchor ${hex} · ${matches.length?'matches '+matches.map(item=>'--brand-'+item.id).join(', ')+' (copied value)':'custom Main Palette value'}`;
        for(const row of view.rows) {
          const name='--'+view.role+'-'+row.step,colour=value(name,theme);
          row.code.textContent=name+': '+colour+';'+(row.step===500?(view.status?' ← semantic anchor':neutral?' ← derived midpoint':' ← selected anchor'):'');
          if(validHex(colour))row.chip.style.backgroundColor=colour;
          row.li.dataset.anchor=String(row.step===500);
        }
        if(view.status) {
          view.chain.textContent=['light','dark'].map(theme=>`${theme==='dark'?'Dark':'Light'}: --${view.role}: ${value('--'+view.role,theme)}; = --${view.role}-500`).join(' · ')+'. Use lighter/darker shades as needed; step numbers do not certify contrast. Existing feedback uses the semantic colour.';
          continue;
        }
        if(neutral) {
          view.chain.textContent='Neutral 50–200 can support light backgrounds; 800–950 can support dark backgrounds or text on light surfaces. Choose a step in the background controls or Semantic colours, then check its actual text/link contrast. Existing semantic choices stay unchanged.';
          continue;
        }
        const descriptions=['light','dark'].map(theme=>{
          const shade=theme==='dark'?300:view.role==='secondary'?700:500;
          const overridden=validHex(state.semanticOverrides?.[theme]?.[view.role]);
          return `${theme==='dark'?'Dark':'Light'}: --${view.role}: ${value('--'+view.role,theme)}; (${overridden?'custom semantic override':'generated from --'+view.role+'-'+shade})`;
        });
        view.chain.textContent=descriptions.join(' · ')+'. Exported declarations contain resolved hex values.';
      }
    }
    DSStudio.on('foundation:updated',sync);sync();
    DSStudio.emit('lesson:content');
  }
});
