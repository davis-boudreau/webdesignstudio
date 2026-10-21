'use strict';
/* Keep configuration in the wizard; centre panels explain and demonstrate it.
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
    const previousApply = apply;
    apply = function() { previousApply(); sync(); };
    sync();

    // The old parameter groups already validate, save and synchronize themselves.
    for (const [step, id] of [[5,'advWeight'], [8,'advBorder'], [8,'advColumns'], [9,'advState'], [9,'advReduce']])
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
      ['studio-section-4',0,'See the system working together', 'A page combines foundations, semantic roles and component rules. The same tokens should support narrow and wide layouts.', '--space-unit → --space-4 → page gutters', 'Resize the page, browse its sections, then compare light and dark themes.'],
      ['brandPalette',4,'Brand references and UI decisions', 'Brand swatches record identity colours. Primary, Supporting and Accent assign those colours an interface job; they are independent decisions.', 'Brand reference → Main Palette choice → --primary', 'Compare the current role assignments. Explain why a brand colour may need a different shade for readable UI text.'],
      ['studio-section-1',6,'Ramps become semantic roles', 'A ramp is a family of shades. A semantic token names a purpose, allowing light and dark themes to use different values for that purpose.', '--primary-500 → --primary → action or link', 'Inspect a ramp and the semantic swatches. Compare text, surface and control-border roles in both themes.'],
      ['studio-section-2',5,'Typography creates hierarchy', 'Font family, scale, line-height and tracking work together. Fluid headings interpolate between viewport limits while body text remains readable.', '--font-size-base + --type-ratio → --text-h1 → heading', 'Compare mobile and desktop specimens. Move the calculator viewport slider and explain where the size stops growing.'],
      ['buttonDesignLab',7,'Buttons communicate actions and states', 'Component tokens apply foundation choices to a specific control. Labels, shape, underlines and focus cues communicate more than colour alone.', '--primary → --button-primary-bg → .ds-button--primary', 'Compare one variant across hover, pressed, focus, selected and loading states. Test a real button with the keyboard.'],
      ['studio-section-3',8,'Spacing, surfaces and responsive layout', 'A shared spacing unit creates related gaps and padding. Grid constraints decide when cards wrap; surfaces and borders clarify groups.', '--space-unit → --space-6 → card padding; --grid-gap → card gutters', 'Compare spacing bars with card padding. Resize the page and find the width where the card grid changes columns.'],
      ['stateExplorer',9,'Native behaviour and visual feedback', 'Focus, disabled, invalid and read-only are different behaviours. A simulation teaches appearance; native HTML supplies real interaction.', '--focus + --focus-width → keyboard outline', 'Compare simulated states, then use Tab on real controls. Explain why read-only text still needs readable contrast.'],
      ['studio-section-5',9,'Evaluate accessibility in context', 'Contrast belongs to a foreground/background pair. Check each theme and state, then review keyboard behaviour and meaning without colour.', '--text on --surface; --control-border beside --background', 'Filter required contrast problems. Preview a repair and check whether it creates new problems before applying.'],
      ['studio-section-6',10,'Deliver the decisions, not just a screenshot', 'CSS implements the tokens; sample HTML demonstrates their use; JSON preserves editable project settings.', 'Project settings → tokens.css + index.html + project JSON', 'Export CSS and HTML together. Identify one component class and trace its values back to the catalogue.'],
      ['studio-section-7',0,'Explain and review your decisions', 'A design system records reusable choices and the reasons behind them. Evaluate the result with real content before extending it.', 'Audience → design decision → token → component → review', 'Write one reason for your palette, typography and layout choices, then list what still needs human testing.'],
      ['studio-section-8',10,'Read the token catalogue', 'Direct tokens store a decision. Derived tokens are calculated scales or aliases; configure their source to keep the system consistent.', '--space-unit → --space-2, --space-4, --space-6', 'Choose Configure source beside a token. Change its wizard setting and compare the catalogue, preview and exported CSS.']
    ];
    for (const [id, step, title, explanation, chain, exercise] of lessons) {
      const lesson = document.createElement('section');
      lesson.className = 'studio-lesson';
      lesson.innerHTML = `<h3>${title}</h3><p>${explanation}</p><p><code>${chain}</code></p><p><strong>Practice:</strong> ${exercise}</p><button type="button" class="ghost" data-configure-step="${step}">Configure in wizard · step ${step + 1}</button>`;
      get(id).querySelector(':scope > .panel').prepend(lesson);
    }
    const topics = ['process-brief','process-ia','process-wireframe','process-prototype','brandPalette','studio-section-2','studio-section-1','buttonDesignLab','studio-section-3','stateExplorer','studio-section-6'];
    topics.forEach((id, step) => {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'ghost';
      button.textContent = 'Explore the centre lesson';
      button.addEventListener('click', () => window.dssRevealSection(id));
      pane(step).append(button);
    });
    window.dssConfigureToken = row => {
      const source = window.dssTokenSource(row);
      if (!source) return;
      window.dssShowWizardStep(source.step);
      if (source.semantic || source.variant) {
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
      announce(`${row.name}: ${source.mode}. Configure its source in wizard step ${source.step + 1}.`);
    };
    document.addEventListener('click', event => {
      const button = event.target.closest('[data-configure-step]');
      if (!button) return;
      window.dssShowWizardStep(Number(button.dataset.configureStep));
      const title = pane(button.dataset.configureStep).querySelector('h3');
      title.tabIndex = -1; title.focus();
      title.scrollIntoView({ block: 'center', behavior: 'instant' });
    });
    window.dssUpdateTokenCatalogue();
  }
});
