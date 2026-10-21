'use strict';
/* Project planning is data, never executable HTML or CSS. Shared artifacts are
   rendered in the centre lessons and static sample from the same validated data. */
(() => {
  const defaults = () => ({
    audience: '',
    goal: '',
    scope: '',
    success: '',
    constraints: '',
    pages: 'Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact',
    layout: 'split',
    wireframeNotes: 'Lead with the main task, group related lessons and keep supporting notes close.',
    prototypeTask: 'Find a useful lesson and decide what to practise next.',
    prototypeNotes: 'Ask someone to follow the task without coaching. Record hesitation, missing information and the next change.'
  });
  const limits = { audience: 600, goal: 600, scope: 1200, success: 600, constraints: 1200, pages: 1600, wireframeNotes: 1200, prototypeTask: 600, prototypeNotes: 1600 };
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
    for (const line of value.split('\n').filter(line => line.trim()).slice(0, 12)) {
      const [parent, child] = line.split('>').slice(0, 2).map(part => part.trim().slice(0, 64));
      if (!parent) continue;
      if (!groups.has(parent)) groups.set(parent, []);
      if (child && !groups.get(parent).includes(child)) groups.get(parent).push(child);
    }
    return [...groups];
  }
  const stages = [
    ['brief', 'Project brief', 'How to create a simple project brief.', 'A brief explains who a website is for and what it needs to help them do. Write a few plain sentences before choosing colours or layouts.', 'Answer these five questions, then use the first wizard step to write your own short draft. Check your assumptions with the people who will use the website.'],
    ['ia', 'Information architecture', 'Give content a clear, findable home.', 'Group content around audience tasks, use meaningful labels and decide which pages belong together. A sitemap describes relationships; it does not prescribe visual columns.', 'Read the sitemap aloud. Can someone predict where a topic belongs? Check labels with a person from the intended audience.'],
    ['wireframe', 'Wireframing', 'Test hierarchy before decoration.', 'A wireframe is a low-detail plan for content and priority. Begin with the main task, then add navigation, supporting content and a clear next action.', 'Compare the split and stacked arrangements. Explain what a person sees first and how the reading order works on a phone.'],
    ['prototype', 'Prototyping', 'Follow a task before polishing the palette.', 'A prototype connects screens to test a journey. Use the linked Discover, Choose and Review screens below to rehearse one path and record what needs to change.', 'Follow the task without coaching. Record hesitation and missing information, revise the plan, then move to palette design.']
  ];
  const text = value => escapeHtml(value || 'Not recorded yet.');
  function artifactHtml(stage, prefix = 'plan') {
    const plan = normalize(state.designProcess), map = hierarchy(plan.pages);
    if (stage === 'brief') {
      const fields = [['Audience','audience'],['Main task','goal'],['Scope','scope'],['Success signal','success'],['Constraints','constraints']];
      const draft = fields.some(([,key]) => plan[key].trim()) ? `<details class="process-brief-draft"><summary>Your draft brief</summary><dl class="process-brief">${fields.map(([label,key])=>`<div><dt>${label}</dt><dd>${text(plan[key])}</dd></div>`).join('')}</dl></details>` : '';
      return `<ol class="process-brief-guide"><li><strong>Audience:</strong> Who will use this website?</li><li><strong>Main task:</strong> What is the main thing they need to do?</li><li><strong>Scope:</strong> Which pages or features are needed first?</li><li><strong>Success:</strong> How will you know the website helps?</li><li><strong>Constraints:</strong> What limits or requirements must you consider, such as time, content and accessibility?</li></ol><p class="process-brief-template"><strong>Start with:</strong> We are making [website] for [audience], so they can [main task]. Start with [scope]. We will know it works when [success].</p><p>Keep it short. Describe the user need before proposing a solution, and revise the brief as you learn.</p><p class="learning-reference"><a href="https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs">GOV.UK: start by learning about user needs</a></p>${draft}`;
    }
    if (stage === 'ia') return `<div class="process-map"><p><strong>${text(state.project)}</strong> / content map</p>${map.length ? `<ul>${map.map(([parent,children]) => `<li><strong>${text(parent)}</strong>${children.length ? `<ul>${children.map(child=>`<li>${text(child)}</li>`).join('')}</ul>` : ''}</li>`).join('')}</ul>` : '<p>Add page labels in the architecture step to begin the map.</p>'}</div>`;
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
  DSStudio.process = { defaults, normalize, hierarchy, stages, artifactHtml, css: processCss };
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
      const controls = [...document.querySelectorAll('[data-process-field]')];
      const rendered = new Map();
      for (const control of controls) control.addEventListener('input', () => {
        state.designProcess = normalize({ ...state.designProcess, [control.dataset.processField]: control.value });
        apply();
      });
      const previousRender = renderCode;
      renderCode = function() {
        const css = processCss();
        if (style.textContent !== css) style.textContent = css;
        const plan = normalize(state.designProcess);
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
