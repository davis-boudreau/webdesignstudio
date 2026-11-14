'use strict';
/* Coalesce background view work without delaying project mutations or saves.
   Preview documents settle before lessons read their computed styles. */
(() => {
  const phases = ['preview', 'lesson'];
  const tasks = new Map(), pending = new Set();
  let queued = false, flushing = false;

  function enqueue() {
    if (queued || flushing || !pending.size) return;
    queued = true;
    queueMicrotask(flush);
  }

  function flush() {
    if (flushing) return;
    queued = false;
    flushing = true;
    try {
      for (const phase of phases) {
        for (const [id, task] of tasks) {
          if (task.phase !== phase || !pending.delete(id)) continue;
          try { task.run(); }
          catch (error) { console.error(`DSStudio view "${id}" failed`, error); }
        }
      }
    } finally {
      flushing = false;
      // An already-run task invalidated by later work gets the next turn.
      enqueue();
    }
  }

  function subscribe({ id, phase = 'lesson', events = [], run }) {
    if (typeof id !== 'string' || !id || tasks.has(id) || !phases.includes(phase) ||
        typeof run !== 'function' || !Array.isArray(events) || events.some(event => typeof event !== 'string')) {
      throw new TypeError('DSStudio.views.subscribe: unique id, valid phase, events and run function required');
    }
    const task = { phase, run };
    tasks.set(id, task);
    const schedule = () => {
      if (tasks.get(id) !== task) return;
      pending.add(id);
      enqueue();
    };
    const unsubscribe = events.map(event => DSStudio.on(event, schedule));
    return {
      schedule,
      dispose() {
        unsubscribe.forEach(off => off());
        // A disposed handle cannot remove a later registration using its id.
        if (tasks.get(id) === task) { tasks.delete(id); pending.delete(id); }
      }
    };
  }

  DSStudio.views = Object.freeze({ subscribe, flush });
})();
