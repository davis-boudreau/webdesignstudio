'use strict';
/* Optional lesson examples only. Never contributes to the website stylesheet. */
(() => {
  const definitions = [
    ['flex', 'display', 'flex'], ['grid', 'display', 'grid'],
    ['flex-col', 'flex-direction', 'column'], ['flex-wrap', 'flex-wrap', 'wrap'],
    ['items-start', 'align-items', 'flex-start'], ['items-center', 'align-items', 'center'],
    ['justify-between', 'justify-content', 'space-between'],
    ['gap-4', 'gap', 'var(--space-4)', '--space-4'],
    ['gap-6', 'gap', 'var(--space-6)', '--space-6'],
    ['p-4', 'padding', 'var(--space-4)', '--space-4'],
    ['p-6', 'padding', 'var(--space-6)', '--space-6'],
    ['bg-surface', 'background-color', 'var(--surface)', '--surface'],
    ['bg-surface-muted', 'background-color', 'var(--surface-muted)', '--surface-muted'],
    ['bg-primary', 'background-color', 'var(--primary)', '--primary'],
    ['text-content', 'color', 'var(--text)', '--text'],
    ['text-content-muted', 'color', 'var(--text-muted)', '--text-muted'],
    ['text-on-primary', 'color', 'var(--on-primary)', '--on-primary'],
    ['rounded-card', 'border-radius', 'var(--radius-base)', '--radius-base'],
    ['font-sans', 'font-family', 'var(--font-body)', '--font-body'],
    ['font-display', 'font-family', 'var(--font-heading)', '--font-heading']
  ].map(([name, property, value, token = null]) => Object.freeze({ name, property, value, token }));
  const rules = new Map(definitions.map(item => [item.name, `.${item.name} { ${item.property}: ${item.value}; }`]));
  const rule = name => rules.get(name) || '';
  const stylesheet = '\n/* OPTIONAL PRACTICE: single-purpose classes using the project tokens.\n' +
    '   Component defaults precede these rules. Use one utility per property;\n' +
    '   class attribute order does not determine the CSS cascade. */\n' +
    definitions.map(item => rule(item.name)).join('\n') + '\n';
  const css = () => stylesheet;
  DSStudio.utilities = Object.freeze({ definitions: Object.freeze(definitions), rule, css });
})();
