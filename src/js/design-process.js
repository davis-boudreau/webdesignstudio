'use strict';
/* Project planning is data, never executable HTML or CSS. Shared artifacts are
   rendered in the centre lessons and static sample from the same validated data. */
(() => {
  // One approved sequence supplies the wizard, centre guide and saved draft.
  const briefFields = [
    { key: 'goal', label: 'Purpose', prompt: 'Why does this website need to exist? Name its main goal and the action visitors should take.', limit: 600 },
    { key: 'audience', label: 'Audience', prompt: 'Who is it for, and what information or task brings them to the website?', limit: 600 },
    { key: 'scope', label: 'Pages and features', prompt: 'What is needed for the first release? List the pages and functions, and say what is out of scope.', limit: 1200 },
    { key: 'content', label: 'Content', prompt: 'What text, images and logos are needed? Name who will supply them and when.', limit: 1200 },
    { key: 'constraints', label: 'Design and requirements', prompt: 'Note the brand or tone, mobile and keyboard needs, and any required platform or hosting.', limit: 1200 },
    { key: 'delivery', label: 'Delivery', prompt: 'Agree a deadline, budget or time limit, what will be handed over, and who approves and maintains the website.', limit: 1200 },
    { key: 'success', label: 'Success', prompt: 'Describe one observable result or a simple task you can test with a visitor.', limit: 600 }
  ];
  // Content inventory: only authored, fixed IDs may become exported destinations.
  const inventories = {
    basic: [
      ['Home', 'home'],
      ['Components', 'features', [['Content card','basic-structure',['Website design','Semantic HTML','Give content meaning']],['Profile row','basic-layout',['Content planning','Flexbox layout','Let the layout adapt']],['FAQ disclosure','basic-usability',['Responsive websites','Responsive navigation','Make the basics easy']]]],
      ['Layouts', 'lists', [['Card grid','cards-grid'],['Unordered list','list-collection',['Project checklist','Unordered lists','What to include']],['Ordered list','list-workflow',['How we work','Ordered lists','A simple workflow']],['Description list','list-terms',['Useful terms','Description lists']],['Content and sidebar','sidebar-example-title']]],
      ['Forms', 'signup', [['Form controls','contact-form',['Enquiry form']],['Grouped choices','form-options'],['Form feedback','basic-signup-note']]], ['Footer', 'footer']
    ],
    advanced: [
      ['Home','home'], ['About','about'],
      ['Design process','design-process', [['Project brief','brief-lab'],['Information architecture','ia-lab'],['Wireframing','wireframe-lab'],['Prototyping','prototype-lab']]],
      ['Lessons','services', ['Brief','Architecture','Wireframe','Prototype','Colour','Typography','Structure','Layout','Components','Review'].map(label=>[`${label} lesson`, `lesson-${label.toLowerCase()}`])],
      ['Layout workshop','grid-lab', [['CSS Grid','grid-example'],['Flexbox','flex-lab'],['Choosing a layout system','layout-choice-title'],['Layout comparison','layout-comparison']]],
      ['Visual language','type-lab', [['Typography','type-specimen'],['Colour','colour-lab']]],
      ['Resources','resources', [['Resource library','resource-library'],['Getting started','getting-started'],['Review checklist','working-together'],['Learning from exports','learning-from-exports'],['Practice tip','practice-tip']]],
      ['Contact','contact'],
      ['Components','components', [['Actions','component-actions'],['Feedback','component-feedback'],['Progress and controls','component-progress']]],
      ['Footer','footer']
    ]
  };
  const sampleInformation = {
    basic: {
      'basic-structure': ['Heading and introduction','Card destination link'],
      'basic-layout': ['Name and role','Availability status'],
      'basic-usability': ['Question and answer'],
      'list-collection': ['Checklist items'], 'list-workflow': ['Workflow steps'],
      'list-terms': ['Terms and definitions'],
      'contact-form': ['Name and email','Enquiry topic and message'],
      'form-options': ['Preferred contact method'], 'basic-signup-note': ['Validation and delivery note']
    },
    advanced: {
      'brief-lab': ['Purpose and audience','Scope and delivery'],
      'ia-lab': ['Content relationships','Sitemap choices'],
      'lesson-brief': ['Learning objective','Practice destination'],
      'grid-example': ['Tracks and column spans'],
      'resource-library': ['Resource name and category'],
      'component-actions': ['Button variants and labels'],
      'component-feedback': ['Status and recovery guidance'],
      'component-progress': ['Progress and confidence values']
    }
  };
  const twoLevelPages = mode => inventories[mode].flatMap(([label,,children=[]])=>[label,...children.map(([child])=>`${label} > ${child}`)]).join('\n');
  const samplePages = (mode = state.sampleMode) => {
    mode = mode === 'basic' ? 'basic' : 'advanced';
    return inventories[mode].flatMap(([label,,children=[]])=>[label,...children.flatMap(([child,id])=>[`${label} > ${child}`,...(sampleInformation[mode][id] || []).map(info=>`${label} > ${child} > ${info}`)])]).join('\n');
  };
  const previousMockPages = "Home\nServices\nServices > Website design\nServices > Content planning\nServices > Responsive websites\nResources\nResources > Project checklist\nResources > How we work\nResources > Useful terms\nContact\nContact > Enquiry form\nContact > Common questions\nFooter";
  const previousTutorialPages = 'Hero\nFlexbox\nFlexbox > Semantic HTML\nFlexbox > Flexbox layout\nFlexbox > Responsive navigation\nGrid & lists\nGrid & lists > Unordered lists\nGrid & lists > Ordered lists\nGrid & lists > Description lists\nForms\nFooter';
  const previousBasicPages = 'Home\nWhat you can learn\nWhat you can learn > Give content meaning\nWhat you can learn > Let the layout adapt\nWhat you can learn > Make the basics easy\nLists\nLists > What to include\nLists > A simple workflow\nLists > Useful terms\nSign up\nFooter';
  const legacyPages = 'Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact';
  function currentPlan() {
    const plan = normalize(state.designProcess);
    // Upgrade the old starter, and keep complete sample inventories in sync with mode.
    if ([legacyPages,previousBasicPages,previousTutorialPages,previousMockPages,twoLevelPages('basic'),twoLevelPages('advanced'),samplePages('basic'),samplePages('advanced')].includes(plan.pages)) plan.pages = samplePages();
    return plan;
  }
  const defaults = () => ({
    ...Object.fromEntries(briefFields.map(({key}) => [key, ''])),
    pages: samplePages('advanced'),
    pageLinks: { basic: {}, advanced: {} },
    iaEntries: { basic: [], advanced: [] },
    contentPlan: { basic: null, advanced: null },
    websiteContent: { basic: [], advanced: [] },
    sitemapSource: { basic: 'auto', advanced: 'auto' },
    sitemapExcluded: { basic: [], advanced: [] },
    showPlanned: false,
    layout: 'split',
    wireframeNotes: 'Lead with the main task, group related lessons and keep supporting notes close.',
    prototypeTask: 'Find a useful lesson and decide what to practise next.',
    prototypeNotes: 'Ask someone to follow the task without coaching. Record hesitation, missing information and the next change.'
  });
  const limits = { ...Object.fromEntries(briefFields.map(({key,limit}) => [key,limit])), pages: 8400, wireframeNotes: 1200, prototypeTask: 600, prototypeNotes: 1600 };
  function normalize(value) {
    const result = defaults();
    if (!value || typeof value !== 'object' || Array.isArray(value)) return result;
    for (const [key, limit] of Object.entries(limits))
      if (typeof value[key] === 'string') result[key] = value[key].slice(0, limit);
    if (['split', 'stack'].includes(value.layout)) result.layout = value.layout;
    result.showPlanned = value.showPlanned === true;
    for (const mode of ['basic', 'advanced']) {
      result.contentPlan[mode] = DSStudio.contentArchitecture?.normalizeNodes(value.contentPlan?.[mode],mode) ?? null;
      result.websiteContent[mode] = DSStudio.websiteContent?.normalize(value.websiteContent?.[mode]) ?? [];
      const allowed = new Set(inventories[mode].flatMap(([,id,children=[]]) => [id,...children.map(([,childId])=>childId)]));
      result.sitemapSource[mode] = ['auto','sections','custom'].includes(value.sitemapSource?.[mode]) ? value.sitemapSource[mode] : 'auto';
      result.sitemapExcluded[mode] = [...new Set((Array.isArray(value.sitemapExcluded?.[mode]) ? value.sitemapExcluded[mode] : []).slice(0,192).filter(id=>allowed.has(id)))];
      const links = value.pageLinks?.[mode];
      if (links && typeof links === 'object' && !Array.isArray(links)) result.pageLinks[mode] = Object.fromEntries(Object.entries(links).slice(0,64).filter(([label,id]) => label.trim() && label.length<=64 && !/[>\r\n]/.test(label) && (id==='' || allowed.has(id))));
      const ids = new Set(), paths = new Set();
      for (const entry of (Array.isArray(value.iaEntries?.[mode]) ? value.iaEntries[mode] : []).slice(0,192)) {
        if (!entry || typeof entry !== 'object' || !/^ia-[1-9]\d{0,4}$/.test(entry.id || '') || ids.has(entry.id) ||
            !Array.isArray(entry.path) || ![1,2,3].includes(entry.path.length) || entry.path.some(part=>typeof part!=='string' || !part.trim() || part.length>64 || /[>\r\n]/.test(part))) continue;
        const path = entry.path.map(part=>part.trim()), key = JSON.stringify(path);
        if (paths.has(key)) continue;
        ids.add(entry.id); paths.add(key);
        result.iaEntries[mode].push({id:entry.id,path,type:['page','section','group','content'].includes(entry.type)?entry.type:'section',includeInSitemap:entry.includeInSitemap!==false});
      }
    }
    return result;
  }
  function tree(value) {
    const roots = [];
    // At most 64 lines, three levels and 64 characters per label.
    for (const line of value.split('\n').filter(line=>line.trim()).slice(0,64)) {
      const parts=line.split('>').map(part=>part.trim().slice(0,64));
      if(parts.length>3)continue;
      while(parts.length && !parts.at(-1))parts.pop();
      if(!parts.length || parts.some(part=>!part))continue;
      let siblings=roots;
      for(const label of parts){
        let node=siblings.find(node=>node.label===label);
        if(!node){node={label,children:[]};siblings.push(node);}
        siblings=node.children;
      }
    }
    return roots;
  }
  // Compatibility projection for existing top-level wireframe/lesson readers.
  const hierarchy = value => tree(value).map(node=>[node.label,node.children.map(child=>child.label)]);
  const labelKey = label => label.toLowerCase().replace(/[\s-]+/g, ' ').trim();
  function linkTargets(plan, mode = state.sampleMode) {
    const destinations = inventories[mode === 'basic' ? 'basic' : 'advanced'].flatMap(([label,id,children=[]])=>[[label,id],...children]);
    if (mode === 'basic') destinations.push(['Services','features'],['Resources','lists'],['Contact','signup'],['Common questions','basic-faq'],['Hero','home'],['Flexbox','features'],['Grid & lists','lists'],['Forms','signup'],['What you can learn','features'],['Features','features'],['Lists','lists'],['Project toolkit','lists'],['Sign up','signup'],['Signup','signup']);
    const targets = new Map();
    for (const [label,id,aliases=[]] of destinations) for (const name of [label,...aliases]) targets.set(labelKey(name),id);
    for (const [label,id] of Object.entries(plan.pageLinks[mode])) {
      if (id) targets.set(labelKey(label),id); else targets.delete(labelKey(label));
    }
    return targets;
  }
  function entries(plan = currentPlan(), mode = state.sampleMode) {
    const stored = plan.iaEntries[mode], targets = linkTargets(plan,mode);
    const byPath = new Map(stored.map(entry=>[JSON.stringify(entry.path),entry]));
    const used = new Set(stored.map(entry=>entry.id)); let next = 1;
    const result = [];
    const add = (path,parentId=null,position=[]) => {
      const existing = byPath.get(JSON.stringify(path));
      while (used.has('ia-'+next)) next++;
      const id = existing?.id || 'ia-'+next++;
      used.add(id);
      const label = path.at(-1);
      const defaultType=targets.has(labelKey(label))?'section':path.length===3?'content':'page';
      const entry = {id,path,label,parentId,position,depth:path.length,type:existing?.type || defaultType,includeInSitemap:existing?.includeInSitemap ?? (defaultType!=='content' && !(mode==='basic' && path.length===1 && ['home','footer'].includes(targets.get(labelKey(label)))))};
      result.push(entry); return entry;
    };
    function visit(nodes,path=[],parentId=null,position=[]) {
      nodes.forEach((node,index)=>{
        const entry=add([...path,node.label],parentId,[...position,index]);
        visit(node.children,entry.path,entry.id,entry.position);
      });
    }
    visit(tree(plan.pages));
    return result;
  }
  const stages = [
    ['brief', 'Project brief', 'Write a brief for a website project.', 'A website project brief is a short agreement about what you are building, who it serves, what is included and how it will be delivered. Start with a few clear sentences before organizing information or choosing a visual style.', 'Choose a small website, such as a café, portfolio or community group. Answer the seven prompts below in one sentence each. Use the seven matching fields in the first wizard step to save your answers in this order.'],
    ['ia', 'Information architecture', 'Organize the information, then choose sitemap destinations.', 'The Brief sets the agreed release scope. Information architecture organizes the content, labels and relationships needed to fulfil it. A sitemap is one view of that architecture, not the whole IA.', 'Keep the full information structure visible. Choose which entries belong in the visitor sitemap, then test whether someone can find one important item.'],
    ['wireframe', 'Wireframing', 'Test hierarchy before decoration.', 'A wireframe is a low-detail plan for content and priority. Begin with the main task, then add navigation, supporting content and a clear next action.', 'Compare the split and stacked arrangements. Explain what a person sees first and how the reading order works on a phone.'],
    ['prototype', 'Prototyping', 'Review your finished website prototype.', 'The live page and exported HTML/CSS are this studio’s prototype output. Use the brief and your task to review the assembled colours, typography, components and responsive layout. Earlier paper-style task screens remain supporting rehearsal material.', 'Ask someone to try the live prototype without coaching. Record hesitation, check keyboard use and narrow layouts, then revise and export the files.']
  ];
  const text = value => escapeHtml(value || 'Not recorded yet.');
  const renderTree = (nodes,depth=0) => `<ul>${nodes.map(node=>`<li>${depth<2?`<strong>${text(node.label)}</strong>`:text(node.label)}${node.children.length?renderTree(node.children,depth+1):''}</li>`).join('')}</ul>`;
  function sitemapHtml({ topLevelLinksOnly = false, linksOnly = false, previewLinks = false } = {}) {
    if(DSStudio.sectionSitemap?.source()==='sections')return DSStudio.sectionSitemap.markup({topLevelLinksOnly,previewLinks});
    const plan = currentPlan(), nodes = entries(plan), targets = linkTargets(plan);
    const eligible = node => node.includeInSitemap && (targets.has(labelKey(node.label)) || node.type==='group' || !linksOnly || plan.showPlanned);
    const item = node => node.type==='group' ? `<span>${text(node.label)}</span>` : targets.has(labelKey(node.label)) ? `<a href="#${previewLinks?'previewShell':targets.get(labelKey(node.label))}"${previewLinks?` data-sitemap-target="${targets.get(labelKey(node.label))}"`:''}>${text(node.label)}</a>` : `<span>${text(node.label)} <small class="sitemap-planned">${node.type==='content'?'No linked destination':'Planned page'}</small></span>`;
    function branch(parentId=null) {
      return nodes.filter(node=>node.parentId===parentId && eligible(node)).map(node=>{
        const children=branch(node.id);
        if(node.type==='group' && !children)return '';
        return `<li>${item(node)}${!topLevelLinksOnly && children?`<ul>${children}</ul>`:''}</li>`;
      }).join('');
    }
    const markup=branch();
    return markup?`<ul class="sitemap-list">${markup}</ul>`:'<p>No sitemap destinations selected. Review inclusion and link destinations in Architecture.</p>';
  }
  function artifactHtml(stage, prefix = 'plan') {
    const plan = currentPlan(), map = hierarchy(plan.pages);
    if (stage === 'brief') {
      const draft = briefFields.some(({key}) => plan[key].trim()) ? `<details class="process-brief-draft"><summary>Your draft brief</summary><dl class="process-brief">${briefFields.map(({label,key})=>`<div data-brief-field="${key}"><dt>${label}</dt><dd>${text(plan[key])}</dd></div>`).join('')}</dl></details>` : '';
      return `<ol class="process-brief-guide">
        ${briefFields.map(({label,prompt})=>`<li><strong>${label}:</strong> ${prompt}</li>`).join('\n        ')}
      </ol>
      <p class="process-brief-template"><strong>Start with:</strong> Build [website] for [audience] so they can [main action]. Include [pages and features]; leave out [not included]. [Owner] supplies [content] by [date]. Deliver [website or files] by [deadline] within [budget or time limit]. Check success by [test].</p>
      <section class="process-brief-example" aria-label="Example website project brief"><h4>Example: a small café website</h4><p>Build a three-page website for local customers to check the menu and plan a visit. Include Home, Menu and Visit pages with opening hours, an address and a map link; online ordering is out of scope. The owner supplies the logo, menu and photos in week one. Use the café's existing branding and support phones and keyboard use. Hand over HTML/CSS files within two weeks and the agreed budget; the owner approves the content and arranges updates. Test whether a new visitor can find today's opening hours and the menu without help.</p></section>
      <p><strong>Before moving on:</strong> Agree the brief with the project owner. Mark unknowns as &ldquo;to confirm&rdquo;. Use the agreed pages and content to start your information architecture.</p>
      <p class="learning-reference">Optional further reading: <a href="https://www.smashingmagazine.com/2018/02/comprehensive-website-planning-guide-part1/">Smashing Magazine: website planning and needs assessment</a>.</p>${draft}`;
    }
    if (stage === 'ia') {
      const basic = state.sampleMode === 'basic';
      return `<section class="process-ia-guidance"><h4>Information architecture and sitemap: different jobs</h4><p>The Brief agrees what belongs in this release. Information architecture organizes that information: its labels, groups and relationships, including content inside pages. A sitemap represents part of that structure. Here, the footer Sitemap is a visitor-facing navigation list.</p><p>For example, Contact and Opening hours both belong in the information architecture. Contact can appear in the sitemap while Opening hours remains content on the page. Unchecking its sitemap choice does not remove those hours from the website.</p><p>Keep the full Website content structure in view. The default Sitemap follows visible eyebrow text, with existing headings as fallbacks. Each link goes directly to its section or container; nested links follow containment on the page. Slashes remain part of the label. Select useful sections, then test whether someone can find an important item. Custom destination plans remain available for saved projects.</p><p class="learning-reference">Further reading: <a href="https://www.nngroup.com/articles/information-architecture-sitemaps/">Nielsen Norman Group: Information Architecture vs. Sitemaps</a>. IA includes ongoing decisions about content and findability; a sitemap is one of its artifacts.</p></section>
      <p>Plan meaningful containers, subcontainers and actual content, as deeply as needed. For example: Header &gt; Main navigation &gt; Home, and Home &gt; Hero &gt; Hero image &gt; Alternative text. Navigation items reference destinations; they do not duplicate those destinations. A deeper content outline does not require extra pages or clicks. Keep it shallow where clear labels suffice. <a href="https://www.nngroup.com/articles/flat-vs-deep-hierarchy/">NN/g: balancing flat and deep hierarchies</a>.</p>
      ${DSStudio.contentArchitecture?.markup() || ''}
      <details class="ia-destination-map"><summary>Custom destination outline (optional)</summary><p>This separate navigation plan includes selected and unselected entries. Content containment, such as a link inside Header, does not determine sitemap ancestry. Manage destinations in the sitemap controls.</p><div class="process-map${basic ? ' process-map--basic' : ''}"><p><strong>${text(state.project)}</strong> / sitemap destination outline</p>${tree(plan.pages).length ? renderTree(tree(plan.pages)) : '<p>Add destination labels in Architecture to begin the sitemap plan.</p>'}<p>This is the destination outline, including entries excluded from the sitemap. Sitemap choices do not remove website content or create new pages.</p></div></details>
      <section class="process-sitemap-preview" aria-label="Visitor sitemap preview"><h4>Visitor sitemap preview</h4>${sitemapHtml({linksOnly:true,previewLinks:prefix==='studio-plan'})}<p>This preview and the footer use the same Sitemap configuration. Section labels come from eyebrows or existing headings. Excluding a parent hides its branch while retaining child choices and all website content.</p></section>`;
    }
    if (stage === 'wireframe') return `<figure class="process-wireframe process-wireframe--${plan.layout}"><div class="process-wire-header"><strong>Header / project identity</strong><p>${text(state.project)}</p></div><div class="process-wire-nav"><strong>Navigation</strong><p>${map.map(([label])=>text(label)).join(' / ') || 'Add navigation labels in the architecture step.'}</p></div><div class="process-wire-main"><strong>Main content / first priority</strong><p>${text(plan.goal)}</p><span class="process-wire-action">Main action / choose a lesson</span></div><div class="process-wire-aside"><strong>Supporting content</strong><p>${text(plan.scope)}</p></div><div class="process-wire-footer"><strong>Footer / next steps</strong></div><figcaption>${text(plan.wireframeNotes)} This is a structural sketch; neutral surfaces keep attention on hierarchy.</figcaption></figure>`;
    return `<div class="process-prototype"><p><strong>Task:</strong> ${text(plan.prototypeTask)}</p><p>Follow these fragment links between three paper-style screens. They demonstrate navigation, not a working registration or submission.</p><ol class="process-screens">
      <li id="${prefix}-discover" tabindex="-1"><h4>1. Discover</h4><p>${text(plan.goal)}</p><a href="#${prefix}-choose">Browse the lesson choices →</a></li>
      <li id="${prefix}-choose" tabindex="-1"><h4>2. Choose</h4><p>Choose what to explore: ${map.map(([label])=>text(label)).join(', ') || 'Add topics in the architecture step.'}</p><a href="#${prefix}-review">Choose a lesson and review →</a><a href="#${prefix}-discover">← Back to discover</a></li>
      <li id="${prefix}-review" tabindex="-1"><h4>3. Review</h4><p><strong>Success signal:</strong> ${text(plan.success)}</p><p>Did the path support the task? Record what happened in the prototype notes before refining the design.</p><a href="#${prefix}-discover">Restart the task</a></li>
      </ol><p class="process-note"><strong>Observation notes:</strong> ${text(plan.prototypeNotes)}</p></div>`;
  }
  const artifactCss = `/* Planning artifacts: normal flow, sitemap, low-detail wireframe and linked screens. */
.process-brief { margin: 0; display: grid; gap: calc(var(--space-unit) * 4); }
.process-brief dt { font-weight: 700; }
.process-brief dd { margin: calc(var(--space-unit) * 2) 0 0; white-space: pre-wrap; overflow-wrap: anywhere; }
.process-brief-guide { padding-inline-start: 1.5rem; }
.process-brief-guide li { margin-bottom: .75rem; }
.process-brief-template { padding: 1rem; background: var(--surface-muted); border-inline-start: 3px solid var(--primary); overflow-wrap: anywhere; }
.process-brief-draft { margin-top: 1.5rem; }
.process-map { padding: calc(var(--space-unit) * 4); border: 1px solid var(--border); border-radius: var(--radius-base); background: var(--surface); overflow-wrap: anywhere; }
.process-map ul { padding-inline-start: calc(var(--space-unit) * 6); }
.process-map li { margin-block: calc(var(--space-unit) * 2); }
.process-ia-guidance, .process-sitemap-preview { min-width: 0; margin-block: var(--space-4); overflow-wrap: anywhere; }
.process-sitemap-preview { padding: var(--space-4); border: 1px solid var(--border); border-radius: var(--radius-base); }
.process-sitemap-preview a { display: inline-flex; align-items: center; min-height: 44px; max-width: 100%; overflow-wrap: anywhere; }
.process-map--basic > ul { display: flex; flex-wrap: wrap; align-items: flex-start; gap: calc(var(--space-unit) * 6); margin-block: calc(var(--space-unit) * 4); padding: 0; list-style: none; }
.process-map--basic > ul > li { flex: 1 1 9rem; min-width: 0; margin: 0; }
.process-map--basic > ul > li > ul { margin: calc(var(--space-unit) * 2) 0 0; padding: 0; list-style: none; }

.ia-content-map { min-width: 0; padding: var(--space-4, 1rem); border: 1px solid var(--border); border-radius: var(--radius-base); overflow-wrap: anywhere; }
.ia-content-map ul { list-style: none; padding-inline-start: .75rem; margin: .5rem 0; min-width: 0; border-inline-start: 1px solid var(--border); }
.ia-content-map li { margin-block: .5rem; min-width: 0; }
.ia-content-map summary, .ia-destination-map > summary { cursor: pointer; min-height: 44px; align-content: center; }
.ia-content-map p { white-space: pre-wrap; margin-block: .5rem; }
.ia-content-map small { font-weight: 400; }
.ia-destination-map { margin-block: 1rem; }
.process-wireframe { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: calc(var(--space-unit) * 4); margin: 0; }
.process-wireframe > div { min-width: 0; padding: calc(var(--space-unit) * 4); border: 1px dashed var(--text-muted); background: var(--surface-muted); color: var(--text); overflow-wrap: anywhere; }
.process-wireframe p { margin: calc(var(--space-unit) * 2) 0 0; }
.process-wire-header, .process-wire-nav, .process-wire-footer, .process-wireframe figcaption { grid-column: 1 / -1; }
.process-wire-action { display: inline-block; margin-top: calc(var(--space-unit) * 4); padding: calc(var(--space-unit) * 2); border: 2px solid currentColor; }
.process-wireframe figcaption { overflow-wrap: anywhere; }
.process-wireframe--stack { grid-template-columns: minmax(0, 1fr); }
.process-screens { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr)); gap: calc(var(--space-unit) * 4); list-style: none; padding: 0; }
.process-prototype .process-screens > li { margin: 0; min-width: 0; padding: calc(var(--space-unit) * 4); border: 1px solid var(--border); border-radius: var(--radius-base); background: var(--surface); overflow-wrap: anywhere; scroll-margin-block: 2rem; }
.process-screens > li:target { outline: 3px solid var(--focus); outline-offset: 3px; }
.process-screens h4 { margin-top: 0; }
.process-screens a { display: block; padding-block: calc(var(--space-unit) * 3); min-height: 44px; overflow-wrap: anywhere; }
.process-note { white-space: pre-wrap; overflow-wrap: anywhere; }
@media (max-width: 48rem) { .process-wireframe { grid-template-columns: minmax(0, 1fr); } }
`;
  const processCss = () => artifactCss.replace('@media (max-width: 48rem)', `@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)})`);
  DSStudio.process = { defaults, normalize, hierarchy, tree, entries, stages, briefFields, artifactHtml, sitemapHtml, samplePages, currentPlan, destinationId:(label,plan=currentPlan(),mode=state.sampleMode)=>linkTargets(plan,mode).get(labelKey(label))||'', inventory: mode => inventories[mode === 'basic' ? 'basic' : 'advanced'].flatMap(([label,id,children=[]])=>[[label,id],...children.map(([name,target])=>[name,target])]), css: processCss };
  DSStudio.register({
    id: 'design-process',
    title: 'Brief, architecture, wireframes and prototypes',
    init() {
      const style = document.createElement('style');
      style.textContent = processCss(); document.head.append(style);
      const previousCss = cssExport;
      cssExport = () => previousCss() + '\n' + processCss();
      for (const [index, [id,title,heading,explanation,exercise]] of stages.entries()) {
        const panel = document.querySelector(`#process-${id} > .panel`);
        panel.innerHTML = `<section class="studio-lesson"><h3>${heading}</h3><p>${explanation}</p><p><strong>Practice:</strong> ${exercise}</p><button class="ghost" type="button" data-configure-step="${index}">Configure in wizard · step ${index+1}</button></section><div data-process-artifact="${id}"></div>`;
      }
      document.getElementById('plan-brief-fields').innerHTML = briefFields.map(({key,label,prompt,limit},index)=>`<div class="field process-editor"><label for="plan-${key}">${index+1}. ${label}</label><p class="help" id="plan-${key}-help">${escapeHtml(prompt)}</p><textarea id="plan-${key}" data-process-field="${key}" aria-describedby="plan-${key}-help" placeholder="Write one or two sentences." maxlength="${limit}" rows="3"></textarea></div>`).join('');
      const controls = [...document.querySelectorAll('[data-process-field]')];
      const rendered = new Map();
      document.getElementById('process-ia').addEventListener('click',event=>{
        const link=event.target.closest('a[data-sitemap-target]');if(!link || event.defaultPrevented || event.button!==0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)return;
        event.preventDefault();
        const frame=document.getElementById('previewPage'), target=frame.contentDocument?.getElementById(link.dataset.sitemapTarget);
        if(!target)return;
        window.dssRevealSection('previewShell',false);
        const shell=document.getElementById('previewShell');shell.scrollIntoView({block:'start',behavior:'instant'});shell.focus({preventScroll:true});
        frame.contentWindow.scrollTo({top:frame.contentWindow.scrollY+target.getBoundingClientRect().top-24,behavior:'instant'});
        target.tabIndex=-1;target.focus({preventScroll:true});
      });
      document.getElementById('plan-use-sample').addEventListener('click', () => {
        const pages = samplePages(state.sampleMode);
        const alreadyApplied = currentPlan().pages === pages;
        state.designProcess = normalize({ ...state.designProcess, pages, pageLinks: { ...currentPlan().pageLinks, [state.sampleMode]: {} }, iaEntries: { ...currentPlan().iaEntries, [state.sampleMode]: [] }, showPlanned: false });
        apply();
        feedbackPages = pages;
        const groups = hierarchy(pages);
        const topics = entries(currentPlan()).filter(node=>node.depth>1).length;
        document.getElementById('plan-sample-status').textContent = `${state.sampleMode === 'basic' ? 'Basic' : 'Advanced'} destination outline ${alreadyApplied ? 'already complete' : 'applied'}: ${groups.length} sections and ${topics} content groups. Review the centre map or open Sitemap in the preview footer. This updates the plan; it does not create new pages.`;
        window.dssRevealSection('process-ia', false);
      });
      for (const control of controls) control.addEventListener('input', () => {
        control.setCustomValidity(control.dataset.processField==='pages' && control.value.split('\n').some(line=>line.split('>').length>3)?'Use at most three information levels: Parent > Child > Detail.':'');
        state.designProcess = normalize({ ...state.designProcess, [control.dataset.processField]: control.value });
        apply();
        document.getElementById('plan-sample-status').textContent = control.validationMessage;
      });
      let feedbackMode = state.sampleMode, feedbackPages = null;
      const previousRender = renderCode;
      renderCode = function() {
        const css = processCss();
        if (style.textContent !== css) style.textContent = css;
        const plan = currentPlan();
        if (feedbackMode !== state.sampleMode || plan.pages !== feedbackPages) document.getElementById('plan-sample-status').textContent = '';
        feedbackMode = state.sampleMode;
        document.getElementById('plan-use-sample').textContent = `Use complete ${state.sampleMode === 'basic' ? 'Basic' : 'Advanced'} destination outline`;
        for (const control of controls) {
          if (control.value !== plan[control.dataset.processField]) control.value = plan[control.dataset.processField];
          if (control.dataset.processField==='pages') control.setCustomValidity(control.value.split('\n').some(line=>line.split('>').length>3)?'Use at most three information levels: Parent > Child > Detail.':'');
        }
        for (const target of document.querySelectorAll('[data-process-artifact]')) {
          let markup = artifactHtml(target.dataset.processArtifact, 'studio-plan');
          const sitemapPreview=document.getElementById('architecture-sitemap-preview');
          if(target.dataset.processArtifact==='ia' && sitemapPreview) {
            // Reuse the exported artifact renderer while showing its visitor map
            // beside the studio's sitemap controls, only once.
            const template=document.createElement('template');template.innerHTML=markup;
            const map=template.content.querySelector('.process-sitemap-preview');
            if(map)map.tabIndex=0;
            const previewMarkup=map?.outerHTML||'';
            if(sitemapPreview.innerHTML!==previewMarkup)sitemapPreview.innerHTML=previewMarkup;
            const guidanceHost=document.getElementById('architecture-review-guidance');
            if(guidanceHost) {
              const guidance=template.content.querySelector('.process-ia-guidance'),guidanceMarkup=guidance?.outerHTML||'';
              if(guidanceHost.innerHTML!==guidanceMarkup)guidanceHost.innerHTML=guidanceMarkup;
              guidance?.remove();
            }
            map?.remove();markup=template.innerHTML;
          }
          if (rendered.get(target) !== markup) {
            const openBranches=new Set([...target.querySelectorAll('.ia-content-map details[open][data-content-branch]')].map(node=>node.dataset.contentBranch));
            const destinationOpen=target.querySelector('.ia-destination-map')?.open;
            target.innerHTML = markup;
            for(const branch of target.querySelectorAll('.ia-content-map details[data-content-branch]'))branch.open=openBranches.has(branch.dataset.contentBranch);
            if(destinationOpen && target.querySelector('.ia-destination-map'))target.querySelector('.ia-destination-map').open=true;
            rendered.set(target, markup);
          }
        }
        previousRender();
      };
      renderCode();
    }
  });
})();
