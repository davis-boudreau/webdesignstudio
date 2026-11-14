'use strict';
/* Architecture is a centre workspace; other configuration stays in the wizard.
   Move existing controls once so their state and event handlers stay shared. */
DSStudio.register({
  id: 'studio-learning',
  title: 'Guided configuration and component lessons',
  init() {
    const get = id => document.getElementById(id);
    const pane = step => document.querySelector(`[data-journey-pane="${step}"]`);
    function group(step, title, nodes) {
      const details = document.createElement('details');
      const summary = document.createElement('summary');
      summary.textContent = title;
      details.append(summary);
      const content = document.createElement('div');
      content.className = 'learning-content';
      for (const node of nodes) content.append(node);
      details.append(content);
      pane(step).append(details);
      return details;
    }
    group(5, 'Heading and body font sources', [get('fontSource').closest('.field'), get('fontSystemOptions'), get('fontGoogleOptions')]);
    get('fontSystemOptions').querySelector('.help').textContent = 'Choose the body font above; choose a separate heading font here if needed.';
    const clampControls = document.querySelector('.clamp-grid');
    document.querySelector('.clamp-result').prepend(get('clampRole').closest('.field'));
    group(5, 'Responsive typography limits', [clampControls, get('clampReset')]);
    // These duplicate tracking controls remain available for older control links.
    group(5, 'Fine typography adjustments', [get('typoHeadingTracking').closest('.grid2')]);
    const headingField = document.createElement('div');
    headingField.className = 'field';
    headingField.innerHTML = '<label for="jHeadingLeading">Heading line-height <output id="jHeadingLeadingOut"></output></label><input id="jHeadingLeading" type="range" min="1" max="1.6" step="0.01" value="1.18">';
    pane(5).append(headingField);
    get('jHeadingLeading').addEventListener('input', event => {
      state.headingLeading = Number(event.target.value);
      apply();
    });
    const sync = () => {
      get('jHeadingLeading').value = state.headingLeading;
      get('jHeadingLeadingOut').textContent = String(round(state.headingLeading, 2));
    };
    DSStudio.on('foundation:updated', sync);
    sync();

    // The old parameter groups already validate, save and synchronize themselves.
    for (const [step, id] of [[5,'advWeight'], [8,'advBorder'], [9,'advColumns'], [10,'advState'], [10,'advReduce']])
      pane(step).append(get(id).closest('details'));
    for (const id of ['jSpacing', 'jRadius']) pane(8).prepend(get(id).closest('.field'));
    // Keep compatibility controls in the wizard, without two visible editors for
    // the same semantic roles. All user-facing editing uses the guided selector.
    const legacyFeedback = get('advColors').closest('details');
    legacyFeedback.hidden = true;
    pane(6).append(legacyFeedback);
    get('semanticEditor').hidden = true;
    pane(6).append(get('semanticEditor'));
    get('advancedTitle').closest('section').hidden = true;
    document.querySelector('.studio-legacy').hidden = true;
    get('jLayoutControls').remove();
    get('jAccessibilityControls').remove();

    const lessons = [
      ['brandPalette',4,'Brand references and UI decisions', 'Brand swatches record identity colours. Primary, Supporting and Accent assign those colours an interface job; they are independent decisions.', 'Brand reference → Main Palette choice → --primary', 'Compare the current role assignments. Explain why a brand colour may need a different shade for readable UI text.'],
      ['studio-section-1',6,'Ramps become semantic roles', 'A ramp is a family of shades. A semantic token names a purpose, allowing light and dark themes to use different values for that purpose.', '--primary-500 → --primary → action or link', 'Inspect a ramp and the semantic swatches. Compare text, surface and control-border roles in both themes.'],
      ['studio-section-2',5,'Typography creates hierarchy', 'Use the content organized in Architecture to establish body and heading fonts, a readable scale, line heights and reading measure. These choices affect wrapping and the space needed by sections, cards and controls. Both wireframe fidelities use these same settings.', '--font-size-base + --type-ratio → --text-h1 → heading', 'Compare mobile and desktop specimens. Move the calculator viewport slider and explain where the size stops growing.'],
      ['buttonDesignLab',7,'Buttons communicate actions and states', 'Component tokens apply foundation choices to a specific control. Labels, shape, underlines and focus cues communicate more than colour alone.', '--primary → --button-primary-bg → .ds-button--primary', 'Compare one variant across hover, pressed, focus, selected and loading states. Test a real button with the keyboard.'],
      ['studio-section-3',8,'Spacing, surfaces and responsive layout', 'A shared spacing unit creates related gaps and padding. Grid constraints decide when cards wrap; surfaces and borders clarify groups.', '--space-unit → --space-6 → card padding; --grid-gap → card gutters', 'Compare spacing bars with card padding. Resize the page and find the width where the card grid changes columns.'],
      ['stateExplorer',10,'Native behaviour and visual feedback', 'Focus, disabled, invalid and read-only are different behaviours. A simulation teaches appearance; native HTML supplies real interaction.', '--focus + --focus-width → keyboard outline', 'Compare simulated states, then use Tab on real controls. Explain why read-only text still needs readable contrast.'],
      ['studio-section-5',10,'Evaluate accessibility in context', 'Contrast belongs to a foreground/background pair. Check each theme and state, then review keyboard behaviour and meaning without colour.', '--text on --surface; --control-border beside --background', 'Filter required contrast problems. Preview a repair and check whether it creates new problems before applying.'],
      ['studio-section-6',11,'Deliver the decisions, not just a screenshot', 'Local component CSS applies the tokens; semantic HTML uses those classes; JSON preserves editable project settings. Optional exercises continue from a locally authored utility to a Tailwind-generated utility using the mapped theme.', 'Project settings → tokens.css + index.html + project JSON', 'Export CSS and HTML together. Identify one component class and trace its values back to the catalogue.'],
      ['studio-section-7',0,'Explain and review your decisions', 'A design system records reusable choices and the reasons behind them. Evaluate the result with real content before extending it.', 'Audience → design decision → token → component → review', 'Write one reason for your palette, typography and layout choices, then list what still needs human testing.'],
      ['studio-section-8',11,'Read the token catalogue', 'Tokens store design decisions; classes apply them to HTML. Direct tokens store a value; derived tokens are calculated scales or aliases. Start by using them in local component CSS, then explore an optional local utility and its Tailwind theme mapping.', '--space-unit → --space-6 → .card padding', 'Choose Configure source beside a token. Change its wizard setting and compare the catalogue, preview and exported CSS.']
    ];
    for (const [id, step, title, explanation, chain, exercise] of lessons) {
      const lesson = document.createElement('section');
      lesson.className = 'studio-lesson';
      lesson.innerHTML = `<h3>${title}</h3><p>${explanation}</p><p><code>${chain}</code></p><p><strong>Practice:</strong> ${exercise}</p><button type="button" class="ghost" data-configure-step="${step}">Configure in wizard · step ${step + 1}</button>`;
      get(id).querySelector(':scope > .panel').prepend(lesson);
    }
    const main = get('main'), preview = get('studio-section-4');
    const sections = [...main.querySelectorAll(':scope > .studio-section')];
    const focusHeading = heading => {
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
      heading.closest('.studio-section').scrollIntoView({ block: 'start', behavior: 'instant' });
    };
    // Short lesson first; detailed laboratories stay available in-place.
    for (const stage of DSStudio.stages) {
      const section = get(stage.lesson), panel = section.querySelector(':scope > .panel');
      const lesson = panel.querySelector(':scope > .studio-lesson');
      section.dataset.stage = String(stage.index);
      const heading = section.querySelector(':scope > summary h2');
      heading.textContent = `Step ${stage.position + 1} of ${DSStudio.stages.length}: ${stage.label}`;
      pane(stage.index).querySelector('.journey-stage-title').textContent = stage.index === 0 ? 'Develop the project brief' : stage.label;
      document.querySelector(`[data-journey-step="${stage.index}"]`).textContent = `${stage.position + 1} · ${stage.label}`;
      const task = document.createElement('p'); task.className = 'step-task';
      task.textContent = stage.task;
      lesson.replaceChildren(lesson.querySelector('h3'), lesson.querySelector('p'), task);
      if(stage.id==='architecture') {
        const overview=document.createElement('details');overview.className='architecture-overview';
        overview.innerHTML='<ol><li><strong>Identify tasks.</strong> Prioritise the main audience’s goals and the information or functions needed to complete them.</li><li><strong>Define scope.</strong> List essential pages and content. Confirm content owners, accessibility needs and dependencies in the brief; note open questions.</li><li><strong>Group and label.</strong> Organise the full agreed content into a clear hierarchy using language the audience understands, including information within pages.</li><li><strong>Develop the content plan.</strong> Select an item, understand its properties and current content, then propose what the audience needs. Record who will supply it and the next action. Save and review the plan before selecting another item.</li><li><strong>Select sitemap destinations.</strong> Choose which IA entries belong in visitor navigation without removing their content. Ask someone where they would start a key task. Revise unclear labels before wireframing.</li></ol><p><strong>Outcome:</strong> An agreed information architecture with a selected visitor sitemap, ready to guide the wireframe.</p>';
        const overviewSummary=document.createElement('summary');overviewSummary.textContent='About content structure and navigation';overview.prepend(overviewSummary);
        const guide=get('ia-content-editor').querySelector('.ia-learning-guide');
        while(guide.children.length>1)overview.append(guide.children[1]);guide.remove();
        lesson.querySelector('h3').textContent='Organise your website';
        lesson.querySelector('p').textContent='Organise your website’s content, plan what each item needs, then choose which sections visitors can reach through the sitemap.';
        task.remove();lesson.append(overview);
        const workspace=document.createElement('section');workspace.id='architecture-workspace';workspace.className='architecture-workspace';workspace.setAttribute('aria-labelledby','architecture-workspace-title');
        workspace.innerHTML='<header><h3 id="architecture-workspace-title" tabindex="-1">Architecture workspace</h3></header>';
        const sitemapAdvanced=get('architecture-sitemap-advanced');
        sitemapAdvanced.append(get('sitemap-outline-editor'));
        get('section-sitemap-editor').insertBefore(get('sitemap-destination-editor'),sitemapAdvanced);
        const sitemap=document.createElement('details');sitemap.id='architecture-sitemap';sitemap.className='architecture-options';
        const sitemapSummary=document.createElement('summary');sitemapSummary.textContent='Visitor sitemap';sitemap.append(sitemapSummary,get('section-sitemap-editor'));
        const contentPlan=get('ia-content-plan');
        for(const control of contentPlan.querySelectorAll('input,textarea,select,button'))control.setAttribute('form','ia-form');
        workspace.append(contentPlan,get('ia-content-editor'),sitemap);
        lesson.after(workspace);
        const review=document.createElement('details');review.id='architecture-saved-review';review.className='architecture-options';
        const artifact=panel.querySelector('[data-process-artifact="ia"]'),guidance=document.createElement('div');guidance.id='architecture-review-guidance';
        guidance.append(artifact.querySelector('.process-ia-guidance'));
        const reviewSummary=document.createElement('summary');reviewSummary.textContent='Review the Content Plan';review.append(reviewSummary,guidance,artifact);workspace.append(review);
        const advanced=document.createElement('details');advanced.id='architecture-advanced';advanced.className='architecture-options';
        const advancedSummary=document.createElement('summary');advancedSummary.textContent='Advanced tools';advanced.append(advancedSummary);workspace.append(advanced);
        const viewSitemap=document.createElement('button');viewSitemap.type='button';viewSitemap.className='ghost';viewSitemap.id='architecture-view-sitemap';viewSitemap.textContent='Review visitor sitemap';
        viewSitemap.addEventListener('click',()=>{sitemap.open=true;sitemapSummary.focus();sitemap.scrollIntoView({block:'start',behavior:'instant'});});get('ia-save').closest('.ia-save-area').append(viewSitemap);
        const open=document.createElement('button');open.type='button';open.className='ghost';open.id='open-architecture-workspace';open.textContent='Open Architecture workspace';
        open.addEventListener('click',()=>{window.dssRevealSection('process-ia',false);get('architecture-workspace-title').focus();get('architecture-workspace-title').scrollIntoView({block:'start',behavior:'instant'});});
        pane(1).querySelector('p.help').after(open);
      }
      const actions = document.createElement('div'); actions.className = 'button-row step-output';
      const inspect = (label, language, find = '') => {
        const button = document.createElement('button');
        button.type = 'button'; button.className = 'ghost'; button.textContent = label;
        button.dataset.inspect = language;
        button.addEventListener('click', () => DSStudio.inspector.show({ language, section: 'all', find }));
        actions.append(button);
      };
      if (stage.index < 4) inspect('Inspect project data', 'json');
      if (stage.index >= 4 || stage.id === 'prototype') {
        inspect('Inspect CSS', 'css', stage.find);
        inspect('Inspect HTML', 'html', stage.index === 7 ? 'ds-button--primary' : '<main');
      }
      lesson.append(actions);
      if(stage.id==='architecture')get('architecture-advanced').append(actions);
      if (stage.id === 'prototype') {
        const previewButton = document.createElement('button'); previewButton.type='button'; previewButton.className='ghost'; previewButton.id='reviewFinalPrototype'; previewButton.textContent='Review live prototype';
        previewButton.addEventListener('click',()=>{preview.open=true;const summary=preview.querySelector('summary');summary.focus();preview.scrollIntoView({block:'start',behavior:'instant'});});
        actions.prepend(previewButton);
        const exportButton = document.createElement('button'); exportButton.type='button';exportButton.className='ghost';exportButton.id='reviewPrototypeExport';exportButton.textContent='Review export files';exportButton.addEventListener('click',()=>window.dssShowWizardStep(11));actions.append(exportButton);
      }
      if (stage.index >= 4 || stage.id === 'prototype') {
        const more = document.createElement('details'); more.className = 'step-more';
        const summary = document.createElement('summary'); summary.textContent = stage.id==='prototype'?'Earlier task rehearsal and notes':`More about ${stage.label.toLowerCase()}`;
        more.append(summary);
        for (const child of [...panel.children]) if (child !== lesson) more.append(child);
        panel.append(more);
      }
    }
    // Group headings describe the one step list; they are not another menu.
    const stageEnd=document.createComment('ordered wizard lessons');preview.after(stageEnd);
    for (const stage of DSStudio.orderedStages) {
      document.querySelector('.journey-steps').append(document.querySelector(`[data-journey-step="${stage.index}"]`));
      main.insertBefore(get(stage.lesson),stageEnd);
    }
    let previousPhase = '';
    for (const stage of DSStudio.orderedStages) {
      if (stage.phase !== previousPhase) {
        const title = document.createElement('span'); title.className = 'journey-phase'; title.textContent = stage.phase;
        document.querySelector(`[data-journey-step="${stage.index}"]`).before(title);
        previousPhase = stage.phase;
      }
    }
    for (const section of sections) {
      if (!section.dataset.stage) {
        const heading = section.querySelector(':scope > summary h2');
        if (heading) heading.textContent = heading.textContent.replace(/^\d+\.\s*/, '');
      }
    }
    // Brief controls always live in the centre; other stages join their lesson
    // on narrow layouts. Put the real controls immediately after the short lesson,
    // preserving nodes/listeners rather than creating a second set of editors.
    const narrow = matchMedia('(max-width: 900px)');
    const stepList = document.createElement('details'); stepList.className = 'journey-step-list';
    stepList.open = true;
    const stepSummary = document.createElement('summary'); stepSummary.textContent = 'Choose a step';
    const stepButtons = document.querySelector('.journey-steps');
    stepButtons.before(stepList); stepList.append(stepSummary, stepButtons);
    stepList.before(get('jProgress'));
    const navigation = document.querySelector('.journey-actions');
    const navigationHome = document.createComment('wizard navigation'); navigation.before(navigationHome);
    const controlHomes = DSStudio.stages.map(stage => {
      const controls = pane(stage.index), home = document.createComment(`controls: ${stage.id}`);
      controls.before(home);
      return home;
    });
    const placeControls = () => {
      for (const stage of DSStudio.stages) {
        const controls = pane(stage.index);
        const destination = stage.index === 0 || narrow.matches ? get(stage.lesson).querySelector('[data-stage-controls]') || get(stage.lesson).querySelector('.studio-lesson') : controlHomes[stage.index];
        // Avoid reinserting correctly placed nodes: even a no-op DOM move can
        // discard focus during a delayed resize notification.
        if (destination.nextSibling !== controls) destination.after(controls);
      }
      if (narrow.matches) {
        const right = document.querySelector('.studio-right');
        if (navigation.parentElement !== right) right.append(navigation);
      } else if (navigationHome.nextSibling !== navigation) navigationHome.after(navigation);
    };
    placeControls();
    narrow.addEventListener('change', placeControls);
    DSStudio.on('lesson:content', placeControls);
    const activate = ({ stage, focus }) => {
      // A step can be selected before a queued media-query change is delivered.
      // Place the existing controls using the current viewport on every route.
      placeControls();
      for (const section of sections) {
        const active = section.id === stage.lesson;
        section.hidden = false;
        if (section !== preview) section.open = active;
      }
      const section = get(stage.lesson);
      if (focus) focusHeading(section.querySelector(':scope > summary h2'));
    };
    DSStudio.on('stage:change', activate);
    DSStudio.activateLesson = (id, focus = false) => {
      const target = get(id), section = target?.closest('.studio-section');
      if (!section || section === preview) return;
      const stage = DSStudio.stages.find(item => item.lesson === section.id);
      if (stage && DSStudio.activeStage !== stage.index) window.dssShowWizardStep(stage.index, focus);
      section.hidden = false;
    };
    // The lesson and controls are already connected; remove reciprocal navigation.
    document.querySelectorAll('[data-configure-step]').forEach(button => button.remove());
    for (const stage of DSStudio.stages) {
      const controls = pane(stage.index), section = get(stage.lesson);
      const more = section.querySelector('.step-more');
      if (more) controls.querySelectorAll(':scope > .build-guide, :scope > .journey-tip').forEach(note => more.append(note));
      else controls.querySelectorAll(':scope > .build-guide').forEach(note => note.remove());
      if (stage.index >= 4) controls.querySelector(':scope > p.help')?.remove();
    }
    // Secondary references are deliberate destinations and have a clear return.
    for (const section of sections.filter(item => !item.dataset.stage && item !== preview)) {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'ghost';
      button.textContent = 'Return to current step';
      button.addEventListener('click', () => window.dssShowWizardStep(DSStudio.activeStage));
      section.querySelector('.panel').prepend(button);
    }
    activate({ stage: DSStudio.stages[DSStudio.activeStage || 0], focus: false });
    window.dssConfigureToken = row => {
      const source = window.dssTokenSource(row);
      if (!source) return;
      window.dssShowWizardStep(source.step, false);
      if (source.semantic || source.variant || source.background) {
        state.theme = row.scope === 'Dark' ? 'dark' : 'light';
        if (source.semantic) get('jSemanticRole').value = source.semantic;
        apply();
      }
      if (source.variant) {
        get('bdVariant').value = source.variant;
        get('bdVariant').dispatchEvent(new Event('input', { bubbles: true }));
      }
      let control = get(source.control);
      if (source.brand) control = [...get('jBrandEditor').querySelectorAll('[data-brand-id]')].find(item => item.dataset.brandId === source.brand)?.querySelector('[data-brand-field="hex"]') || control;
      window.dssRevealSection(control.id || control.closest('[id]').id, false);
      control.scrollIntoView({ block: 'center', behavior: 'instant' });
      control.focus();
      announce(`${row.name}: ${source.mode}. Configure its source in wizard step ${DSStudio.stages[source.step].position + 1}.`);
    };
    window.dssUpdateTokenCatalogue();
  }
});
