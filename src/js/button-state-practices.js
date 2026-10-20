'use strict';
/* One set of non-colour state cues for studio specimens and exported buttons.
   These styles supplement native semantics; application logic owns actions. */
(() => {
  function css(selector, simulationAttribute = '') {
    const button = `:is(${selector})`;
    const available = ':not(:disabled):not([aria-disabled="true"]):not([aria-busy="true"])';
    const simulated = state => simulationAttribute ? [`${button}[${simulationAttribute}="${state}"]${available}`,
      ...(simulationAttribute === 'data-sim' ? [`.state-tile[data-state="${state}"] ${button}${available}`] : [])] : [];
    const hover = [`${button}:hover${available}`, ...simulated('hover')].join(', ');
    const activeSelectors = [`${button}:active${available}`];
    activeSelectors.push(...simulated('active'));
    const active = activeSelectors.join(', ');
    return `/* State best practices: colour + shape/text; hover/pressed cues preserve geometry.
   Focus outlines remain defined by the component's focus tokens.
   Toggle buttons keep their label and expose aria-pressed=true/false.
   Busy controls need a visible label, status announcements and duplicate-action protection in application code. */
${button} { display: inline-flex; align-items: center; justify-content: center; gap: .5em; text-decoration: none; text-underline-offset: .2em; text-decoration-thickness: .1em; }
${hover} { text-decoration-line: underline; }
${active} { box-shadow: inset 0 0 0 2px currentColor; }
${button}[aria-pressed]::before { content: ""; display: inline-block; flex: none; width: .4em; height: .7em; border: solid currentColor; border-width: 0 .125em .125em 0; transform: rotate(45deg); margin-inline: .125em; }
${button}[aria-pressed="false"]::before { visibility: hidden; }
${button}[aria-busy="true"] { opacity: 1; cursor: progress; }
${button}[aria-busy="true"]::after { content: ""; display: inline-block; flex: none; width: 1em; height: 1em; box-sizing: border-box; border: .125em solid currentColor; border-inline-end-color: transparent; border-radius: 50%; animation: var(--button-progress-animation, dss-button-progress) 1s linear infinite; }
@keyframes dss-button-progress { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { ${button}[aria-busy="true"]::after { animation: none; } }
@media (forced-colors: active) { ${activeSelectors.map(value => value + ':not(:focus-visible)').join(', ')} { outline: 2px solid ButtonText; outline-offset: -4px; } }
`;
  }
  DSStudio.buttonStates = { css };
  DSStudio.register({
    id: 'button-state-practices',
    title: 'Button state best practices',
    init() {
      const style = document.createElement('style');
      style.id = 'buttonStatePractices';
      style.textContent = css('.bd-button, .demo-btn', 'data-sim');
      document.head.append(style);
    }
  });
})();
