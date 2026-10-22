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
      ['What you can learn', 'features', [['Give content meaning','basic-structure'],['Let the layout adapt','basic-layout'],['Make the basics easy','basic-usability']]],
      ['Lists', 'lists', [['What to include','list-collection'],['A simple workflow','list-workflow'],['Useful terms','list-terms']]],
      ['Sign up', 'signup'], ['Footer', 'footer']
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
  const samplePages = (mode = state.sampleMode) => inventories[mode === 'basic' ? 'basic' : 'advanced'].flatMap(([label,,children=[]]) => [label,...children.map(([child])=>`${label} > ${child}`)]).join('\n');
  const legacyPages = 'Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact';
  function currentPlan() {
    const plan = normalize(state.designProcess);
    // Upgrade the old starter, and keep complete sample inventories in sync with mode.
    if ([legacyPages,samplePages('basic'),samplePages('advanced')].includes(plan.pages)) plan.pages = samplePages();
    return plan;
  }
  const defaults = () => ({
    ...Object.fromEntries(briefFields.map(({key}) => [key, ''])),
    pages: samplePages('advanced'),
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
    return result;
  }
  function hierarchy(value) {
    const groups = new Map();
    // Bounded depth and counts keep imported or pasted plans readable.
    for (const line of value.split('\n').filter(line => line.trim()).slice(0, 64)) {
      const [parent, child] = line.split('>').slice(0, 2).map(part => part.trim().slice(0, 64));
      if (!parent) continue;
      if (!groups.has(parent)) groups.set(parent, []);
      if (child && !groups.get(parent).includes(child)) groups.get(parent).push(child);
    }
    return [...groups];
  }
  const stages = [
    ['brief', 'Project brief', 'Write a brief for a website project.', 'A website project brief is a short agreement about what you are building, who it serves, what is included and how it will be delivered. Start with a few clear sentences before planning the sitemap or choosing a visual style.', 'Choose a small website, such as a café, portfolio or community group. Answer the seven prompts below in one sentence each. Use the seven matching fields in the first wizard step to save your answers in this order.'],
    ['ia', 'Information architecture', 'Give content a clear, findable home.', 'Group content around audience tasks, use meaningful labels and decide which pages belong together. A sitemap describes relationships; it does not prescribe visual columns.', 'Read the sitemap aloud. Can someone predict where a topic belongs? Check labels with a person from the intended audience.'],
    ['wireframe', 'Wireframing', 'Test hierarchy before decoration.', 'A wireframe is a low-detail plan for content and priority. Begin with the main task, then add navigation, supporting content and a clear next action.', 'Compare the split and stacked arrangements. Explain what a person sees first and how the reading order works on a phone.'],
    ['prototype', 'Prototyping', 'Follow a task before polishing the palette.', 'A prototype connects screens to test a journey. Use the linked Discover, Choose and Review screens below to rehearse one path and record what needs to change.', 'Follow the task without coaching. Record hesitation and missing information, revise the plan, then move to palette design.']
  ];
  const text = value => escapeHtml(value || 'Not recorded yet.');
  function sitemapHtml() {
    const map = hierarchy(currentPlan().pages);
    const destinations = inventories[state.sampleMode === 'basic' ? 'basic' : 'advanced'].flatMap(([label,id,children=[]])=>[[label,id],...children]);
    if (state.sampleMode === 'basic') destinations.push(['Features','features'],['Signup','signup']);
    const key = label => label.toLowerCase().replace(/[\s-]+/g, ' ').trim();
    const targets = new Map();
    for (const [label,id,aliases = []] of destinations)
      for (const name of [label,...aliases]) targets.set(key(name), id);
    const item = label => targets.has(key(label)) ? `<a href="#${targets.get(key(label))}">${text(label)}</a>` : `<span>${text(label)} <small class="sitemap-planned">Planned page</small></span>`;
    return map.length ? `<ul class="sitemap-list">${map.map(([parent,children])=>`<li>${item(parent)}${children.length ? `<ul>${children.map(child=>`<li>${item(child)}</li>`).join('')}</ul>` : ''}</li>`).join('')}</ul>` : '<p>Add page labels in Architecture to create your sitemap.</p>';
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
      <p><strong>Before moving on:</strong> Agree the brief with the project owner. Mark unknowns as &ldquo;to confirm&rdquo;. Use the agreed pages and content to start your sitemap.</p>
      <p class="learning-reference">Optional further reading: <a href="https://www.smashingmagazine.com/2018/02/comprehensive-website-planning-guide-part1/">Smashing Magazine: website planning and needs assessment</a>.</p>${draft}`;
    }
    if (stage === 'ia') return `<div class="process-map"><p><strong>${text(state.project)}</strong> / ${state.sampleMode === 'basic' ? 'Basic' : 'Advanced'} sitemap plan</p>${map.length ? `<ul>${map.map(([parent,children]) => `<li><strong>${text(parent)}</strong>${children.length ? `<ul>${children.map(child=>`<li>${text(child)}</li>`).join('')}</ul>` : ''}</li>`).join('')}</ul>` : '<p>Add page labels in the architecture step to begin the map.</p>'}<p>This maps sections and content groups on a single page. The footer uses the same plan: existing content is linked; new page ideas are labelled Planned page. Navigation can show a shorter selection of key destinations.</p></div>`;
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
  DSStudio.process = { defaults, normalize, hierarchy, stages, briefFields, artifactHtml, sitemapHtml, samplePages, css: processCss };
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
      document.getElementById('plan-use-sample').addEventListener('click', () => {
        state.designProcess = normalize({ ...state.designProcess, pages: samplePages() });
        apply();
      });
      for (const control of controls) control.addEventListener('input', () => {
        state.designProcess = normalize({ ...state.designProcess, [control.dataset.processField]: control.value });
        apply();
      });
      const previousRender = renderCode;
      renderCode = function() {
        const css = processCss();
        if (style.textContent !== css) style.textContent = css;
        const plan = currentPlan();
        document.getElementById('plan-use-sample').textContent = `Use complete ${state.sampleMode === 'basic' ? 'Basic' : 'Advanced'} sitemap`;
        for (const control of controls) if (control.value !== plan[control.dataset.processField]) control.value = plan[control.dataset.processField];
        for (const target of document.querySelectorAll('[data-process-artifact]')) {
          const markup = artifactHtml(target.dataset.processArtifact, 'studio-plan');
          if (rendered.get(target) !== markup) {
            target.innerHTML = markup;
            rendered.set(target, markup);
          }
        }
        previousRender();
      };
      renderCode();
    }
  });
})();
