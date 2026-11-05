'use strict';
/* State shade options derive from the same resolved colours as component CSS.
   They supplement existing state rules; native behaviour is never a colour ramp. */
(() => {
  const variants=['primary','secondary','accent','outline','text'];
  const labels={default:'Default',hover:'Hover',focus:'Focus-visible',active:'Active / pressed',selected:'Selected',disabled:'Disabled',loading:'Loading',invalid:'Invalid',success:'Valid / success',readonly:'Read-only'};
  const buttonStates=['default','hover','focus','active','selected','disabled','loading'];
  const generalStates=[...buttonStates,'invalid','success','readonly'];
  const cues={default:'Ready to activate.',hover:'Underline supplements the colour change.',focus:'Keep a visible outline and test actual keyboard focus.',active:'A pressed cue is momentary; it is separate from selection.',selected:'Keep the checkmark and aria-pressed on toggle buttons.',disabled:'Native disabled prevents activation; opacity .55 also affects the displayed colour.',loading:'Keep the progress indicator, busy label and duplicate-action protection.',invalid:'Include an error message and aria-invalid.',success:'Include a success message; colour alone is insufficient.',readonly:'Read-only text stays readable and selectable; it is separate from disabled.'};
  function entries(theme,group='general',buttonData=window.dssGetButtonContrastData(),roles=palette(theme).roles) {
    const semantic={default:'primary',hover:'primary-hover',focus:'focus',active:'primary',selected:'primary',disabled:'primary',loading:'primary',invalid:'danger',success:'success',readonly:'surface-muted'};
    const isButton=variants.includes(group),colours=isButton?buttonData.themes[theme][group]:null;
    return (isButton?buttonStates:generalStates).map(key=>{
      let anchor,source,control,property=null,transparent=false;
      if(isButton) {
        property=key==='hover'?'hover':key==='active'?'active':key==='focus'||key==='selected'?'focus':'bg';
        anchor=property==='focus'?buttonData.settings.focus:colours[property];
        transparent=anchor==='transparent';
        if(transparent){anchor=colours.fg;property='text';}
        source=property==='focus'?'--button-focus':'--button-'+group+'-'+(transparent?'text':property);
        control=property==='focus'?'bdFocus':transparent?'bdText':{bg:'bdDefaultBg',hover:'bdHover',active:'bdActive'}[property];
      } else {
        source='--'+semantic[key];anchor=roles[semantic[key]];control='jSemanticRole';
      }
      return {key,label:labels[key],prefix:isButton?'--button-'+group+'-state-'+key:'--state-'+key,anchor:anchor.toUpperCase(),source,control,property,semantic:isButton?null:semantic[key],variant:isButton?group:null,cue:cues[key]+(transparent?' The background is transparent: this ramp uses the foreground colour; it is not the composited background.':'')};
    });
  }
  const sourceRows=new Map();
  DSStudio.statePalettes={entries,variants,sourceFor:(prefix,theme)=>sourceRows.get(theme+prefix)};
  let signature='',generated='';
  function css() {
    const next=JSON.stringify([state.method,state.primary,state.secondary,state.accent,state.semanticOverrides,state.buttonDesign]);
    if(next===signature)return generated;
    const buttonData=window.dssGetButtonContrastData();
    const themes=['light','dark'].map(theme=>{
      const roles=palette(theme).roles;
      return {theme,rows:['general',...variants].flatMap(group=>entries(theme,group,buttonData,roles))};
    });
    const ramps=new Map();
    for(const {theme,rows} of themes)for(const row of rows)sourceRows.set(theme+row.prefix,row);
    generated='\n/* STATE PALETTES: shade options derived from resolved state colours.\n   500 preserves the source colour; existing component rules and non-colour cues still apply. */\n'+themes.map(({theme,rows})=>{
      const declarations=rows.flatMap(row=>{
        if(!ramps.has(row.anchor))ramps.set(row.anchor,makeRamp(row.anchor,state.method));
        const ramp=ramps.get(row.anchor);
        return steps.map(step=>`  ${row.prefix}-${step}: ${ramp[step]};`);
      }).join('\n');
      return (theme==='dark'?'[data-theme="dark"]':':root')+' {\n'+declarations+'\n}';
    }).join('\n');
    signature=next;return generated;
  }
  const previousCss=cssExport;
  cssExport=function(){return previousCss()+css();};
  DSStudio.register({
    id:'state-palettes',title:'All interaction state palette steps',
    init() {
      const get=id=>document.getElementById(id),views=[];
      let group='general',viewSignature='';
      function defaultColour(row,generalDefaults) {
        if(row.variant)return window.dssGetButtonDefaultContrastColour(row.variant,row.property,state.theme);
        return generalDefaults[row.semantic];
      }
      function changeColour(key,value) {
        const row=entries(state.theme,group).find(item=>item.key===key);
        if(!row || (value!=='default' && !validHex(value))){viewSignature='';sync();return;}
        if(row.variant)window.dssSetButtonContrastColour(row.variant,row.property,value==='default'?null:value);
        else {
          const overrides={...state.semanticOverrides?.[state.theme]};
          if(value==='default')delete overrides[row.semantic];else overrides[row.semantic]=value.toUpperCase();
          state.semanticOverrides={...state.semanticOverrides,[state.theme]:overrides};apply();
        }
      }
      function addView(parent,id) {
        const section=document.createElement('section');section.id=id;section.className='palette-token-lesson';section.setAttribute('aria-labelledby',id+'-title');
        const heading=document.createElement('h4');heading.id=id+'-title';heading.textContent='Generate interaction state palette steps';
        const intro=document.createElement('p');intro.className='help';intro.textContent='Generate eleven shades for every interaction state. Choose a state colour below, or restore its default. The choice edits its existing source and regenerates the steps; shared sources update related states together. Step 500 preserves the source. Check contrast and retain native behaviour and non-colour cues.';
        const label=document.createElement('label');label.htmlFor=id+'-component';label.textContent='Component for state palettes';
        const select=document.createElement('select');select.id=label.htmlFor;
        for(const value of ['general',...variants]) {
          const option=document.createElement('option');option.value=value;option.textContent=value==='general'?'General controls':value[0].toUpperCase()+value.slice(1)+' buttons';select.append(option);
        }
        const field=document.createElement('div');field.className='field interaction-palette-field';field.append(label,select);
        const theme=document.createElement('p');theme.className='help';
        const list=document.createElement('div');list.className='interaction-palette-ramps';
        section.append(heading,intro,field,theme,list);parent.append(section);
        const view={id,select,theme,list,rows:[]};views.push(view);
        select.addEventListener('change',()=>{group=select.value;viewSignature='';sync();});
      }
      addView(get('status-palette-steps-controls'),'interaction-palette-controls');
      addView(get('status-palette-lesson'),'interaction-palette-lesson');
      function sync() {
        const button=state.buttonDesign;
        const rows=entries(state.theme,group),next=JSON.stringify([state.theme,state.method,group,rows,state.brandPalette,state.primary,state.secondary,state.accent,rows.map(row=>row.semantic?state.semanticOverrides?.[state.theme]?.[row.semantic]:null),button?.sources,button?.custom,button?.overrides,button?.focus]);
        if(next===viewSignature)return;viewSignature=next;
        const tokens=window.dssReadTokens();
        const brands=DSStudio.brandPalette.normalize(state.brandPalette);
        const generalDefaults=group==='general'?palette(state.theme,{...state,semanticOverrides:{}}).roles:null;
        const defaultColours=new Map();
        const editors=rows.map(row=>{
          if(!defaultColours.has(row.source))defaultColours.set(row.source,defaultColour(row,generalDefaults));
          const fallback=defaultColours.get(row.source);
          const overridden=row.variant?(row.property==='focus'?row.anchor!==fallback.toUpperCase():validHex(state.buttonDesign?.overrides?.[row.variant]?.[row.property])):validHex(state.semanticOverrides?.[state.theme]?.[row.semantic]);
          const choices=[['default','Default · '+fallback.toUpperCase()]],seen=new Set();
          const add=(value,label)=>{if(validHex(value) && !seen.has(value.toUpperCase())){seen.add(value.toUpperCase());choices.push([value.toUpperCase(),label+' · '+value.toUpperCase()]);}};
          for(const brand of brands)add(brand.hex,'Brand: '+brand.name);
          for(const role of ['primary','secondary','accent'])add(state[role],'Main: '+role);
          for(const step of steps)add(tokens.find(token=>token.name==='--neutral-'+step)?.value,'Neutral '+step);
          for(const step of steps)add(tokens.find(token=>token.name===row.prefix+'-'+step && (token.scope==='Dark')===(state.theme==='dark'))?.value,row.label+' '+step);
          if(overridden)add(row.anchor,'Current colour');
          const shared=rows.filter(other=>other.key!==row.key && other.source===row.source).map(other=>other.label);
          const help='Edits '+row.source+'. '+(row.variant?'Button colours apply to both themes. '+(row.property==='focus'?'Focus colour is shared across button variants. ':''):(state.theme==='dark'?'Dark':'Light')+' theme only. ')+(shared.length?'Also updates '+shared.join(', ')+'. ':'')+'Brand and shade choices copy a colour value.';
          return {choices,selected:overridden?row.anchor:'default',help};
        });
        for(const view of views) {
          view.select.value=group;view.theme.textContent='Showing '+(state.theme==='dark'?'Dark':'Light')+' theme · '+(state.method==='oklch'?'OKLCH':'RGB mix')+'. Compare foreground/background pairs in each state.';
          if(view.rows.map(item=>item.key).join()!==rows.map(item=>item.key).join() || view.list.dataset.component!==group) {
            view.list.dataset.component=group;view.list.replaceChildren();
            view.rows=rows.map(row=>{
              const details=document.createElement('details');details.className='palette-ramp';details.dataset.interactionState=row.key;
              const summary=document.createElement('summary');summary.textContent=row.label+' palette steps';
              const anchor=document.createElement('p');anchor.className='help';
              const colourField=document.createElement('div');colourField.className='field interaction-palette-field';
              const colourLabel=document.createElement('label');colourLabel.htmlFor=view.id+'-'+row.key+'-colour';colourLabel.textContent=row.label+' colour';
              const colour=document.createElement('select');colour.id=colourLabel.htmlFor;colour.dataset.stateColour=row.key;
              const colourHelp=document.createElement('p');colourHelp.className='help';colourHelp.id=colour.id+'-help';colour.setAttribute('aria-describedby',colourHelp.id);
              colour.addEventListener('change',()=>changeColour(row.key,colour.value));colourField.append(colourLabel,colour,colourHelp);
              const list=document.createElement('ol');list.className='palette-step-list';list.setAttribute('aria-label',row.label+' shade tokens');
              const shades=steps.map(step=>{
                const li=document.createElement('li');li.dataset.shade=String(step);li.dataset.anchor=String(step===500);
                const chip=document.createElement('span');chip.className='brand-palette-chip';chip.setAttribute('aria-hidden','true');
                const code=document.createElement('code');li.append(chip,code);list.append(li);return {step,chip,code};
              });
              const cue=document.createElement('p');cue.className='palette-token-chain';
              const actions=document.createElement('div');actions.className='button-row';
              for(const [label,action] of [['Inspect shade CSS',()=>DSStudio.inspector.show({language:'css',section:'all',find:row.prefix+'-500:'})],['Inspect source CSS',()=>DSStudio.inspector.show({language:'css',section:'all',find:row.source+':'})],['Configure state colour',()=>window.dssConfigureToken({name:row.prefix+'-500',scope:state.theme==='dark'?'Dark':'Light / base'})]]) {
                const button=document.createElement('button');button.type='button';button.className='ghost';button.textContent=label;
                // Resolve the latest source on click: transparency may change it.
                button.addEventListener('click',()=>{const current=entries(state.theme,group).find(item=>item.key===row.key);if(label==='Inspect source CSS')DSStudio.inspector.show({language:'css',section:'all',find:current.source+':'});else action();});actions.append(button);
              }
              details.append(summary,anchor,colourField,list,cue,actions);view.list.append(details);return {key:row.key,anchor,cue,shades,colour,colourHelp,choicesSignature:''};
            });
          }
          for(const [index,item] of view.rows.entries()) {
            const row=rows[index];item.anchor.textContent=row.source+': '+row.anchor+'; → '+row.prefix+'-500. The ramp follows this source and the generation method.';item.cue.textContent=row.cue;
            const editor=editors[index],choicesSignature=JSON.stringify(editor.choices);
            if(item.choicesSignature!==choicesSignature) {
              item.colour.replaceChildren(...editor.choices.map(([value,label])=>{const option=document.createElement('option');option.value=value;option.textContent=label;return option;}));item.choicesSignature=choicesSignature;
            }
            item.colour.value=editor.selected;item.colourHelp.textContent=editor.help;
            for(const shade of item.shades) {
              const name=row.prefix+'-'+shade.step,token=tokens.find(token=>token.name===name && (token.scope==='Dark')===(state.theme==='dark'));
              shade.code.textContent=name+': '+token.value+';'+(shade.step===500?' ← state anchor':'');shade.chip.style.backgroundColor=token.value;
            }
          }
        }
      }
      const previousRender=renderCode;renderCode=function(){previousRender();sync();};
      renderCode();DSStudio.emit('lesson:content');
    }
  });
})();
