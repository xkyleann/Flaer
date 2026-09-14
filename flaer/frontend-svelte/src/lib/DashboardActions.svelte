<script>
  let filter = 'next';
  let actions = [
    { id: 'directory', stage: 'Now', title: 'Approve a facility directory source', detail: 'Confirm permission, attribution, refresh cadence, and the exact European fields we can display.', unlocks: 'Named facility map and source provenance', owner: 'Data operations', state: 'next' },
    { id: 'telemetry', stage: 'Required', title: 'Connect operational telemetry', detail: 'Map energy, water, PUE, backup power, and renewable procurement inputs to each facility.', unlocks: 'Metrics, forecasts, benchmarks, and reports', owner: 'Operations', state: 'next' },
    { id: 'evidence', stage: 'Plan', title: 'Validate shortlisted site evidence', detail: 'Request utility capacity, fibre diversity, zoning, water, and climate-resilience evidence for each candidate.', unlocks: 'Investment-ready site planning brief', owner: 'Development', state: 'next' }
  ];

  function updateState(id) { actions = actions.map((action) => action.id === id ? { ...action, state: action.state === 'done' ? 'next' : 'done' } : action); }
  $: visibleActions = filter === 'all' ? actions : filter === 'done' ? actions.filter((action) => action.state === 'done') : actions.filter((action) => action.state !== 'done');
  $: completed = actions.filter((action) => action.state === 'done').length;
</script>

<section class="action-board">
  <header class="action-head">
    <div><span class="eyebrow">WORKSPACE PRIORITIES</span><h3>Make the workspace decision-ready</h3><p>Complete the data and evidence steps that unlock reliable analysis.</p></div>
    <div class="completion"><strong>{completed}/{actions.length}</strong><span>steps complete</span></div>
  </header>
  <div class="action-tabs" aria-label="Action filters">
    {#each [['next', 'Next steps'], ['all', 'All'], ['done', 'Completed']] as [value, label]}
      <button class:active={filter === value} on:click={() => filter = value}>{label}</button>
    {/each}
  </div>
  <div class="action-list">
    {#each visibleActions as action, index}
      <article class:complete={action.state === 'done'} class="action-row">
        <div class="action-number">{action.state === 'done' ? '✓' : index + 1}</div>
        <div class="action-main"><span class="action-stage">{action.stage}</span><h4>{action.title}</h4><p>{action.detail}</p></div>
        <div class="action-unlock"><span>UNLOCKS</span><strong>{action.unlocks}</strong></div>
        <div class="action-owner"><span>OWNER</span><strong>{action.owner}</strong></div>
        <button class="action-toggle" on:click={() => updateState(action.id)}>{action.state === 'done' ? 'Completed' : 'Mark complete'}</button>
      </article>
    {:else}<div class="empty-actions">No actions in this view.</div>
    {/each}
  </div>
</section>

<style>
  .action-board { border: 1px solid rgba(255,255,255,.08); border-radius: 18px; overflow: hidden; background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018)); }
  .action-head { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; padding: 22px 24px 18px; border-bottom: 1px solid rgba(255,255,255,.07); }.eyebrow, .action-stage, .action-unlock span, .action-owner span { color: var(--tm); font-size: 9px; font-weight: 800; letter-spacing: .11em; text-transform: uppercase; }.action-head h3 { margin: 5px 0; color: var(--text); font-size: 20px; letter-spacing: -.04em; }.action-head p { color: var(--ts); font-size: 12px; }.completion { display: grid; gap: 2px; min-width: 80px; padding: 10px 12px; border: 1px solid rgba(44,173,132,.23); border-radius: 12px; background: rgba(44,173,132,.08); text-align: right; }.completion strong { color: #85e9c1; font-size: 17px; }.completion span { color: var(--tm); font-size: 9px; }
  .action-tabs { display: flex; gap: 6px; padding: 12px 24px; border-bottom: 1px solid rgba(255,255,255,.07); }.action-tabs button { border: 1px solid rgba(255,255,255,.09); border-radius: 999px; padding: 6px 10px; background: transparent; color: var(--ts); font: inherit; font-size: 10px; font-weight: 800; cursor: pointer; }.action-tabs button.active { border-color: rgba(44,173,132,.35); background: rgba(44,173,132,.12); color: #b6ffe7; }
  .action-list { display: grid; }.action-row { display: grid; grid-template-columns: 32px minmax(240px, 1.8fr) minmax(150px, 1fr) 110px auto; gap: 18px; align-items: center; padding: 17px 24px; border-bottom: 1px solid rgba(255,255,255,.06); }.action-row:last-child { border-bottom: 0; }.action-number { display: grid; width: 27px; height: 27px; place-items: center; border: 1px solid rgba(127,174,255,.34); border-radius: 50%; color: #a9c8ff; background: rgba(127,174,255,.08); font-size: 11px; font-weight: 900; }.action-row.complete .action-number { border-color: rgba(44,173,132,.45); color: #72e7b9; background: rgba(44,173,132,.13); }.action-main h4 { margin: 4px 0; color: var(--text); font-size: 14px; letter-spacing: -.02em; }.action-main p { color: var(--ts); font-size: 11px; line-height: 1.45; }.action-unlock, .action-owner { display: grid; gap: 5px; }.action-unlock strong, .action-owner strong { color: var(--text); font-size: 10.5px; line-height: 1.35; }.action-toggle { border: 1px solid rgba(255,255,255,.13); border-radius: 9px; padding: 8px 10px; background: rgba(255,255,255,.05); color: var(--text); white-space: nowrap; font: inherit; font-size: 10px; font-weight: 800; cursor: pointer; }.action-row.complete .action-toggle { border-color: rgba(44,173,132,.3); color: #8ceec8; background: rgba(44,173,132,.09); }.empty-actions { padding: 30px; color: var(--tm); text-align: center; font-size: 12px; }
  @media (max-width: 980px) { .action-row { grid-template-columns: 28px 1fr auto; }.action-unlock, .action-owner { display: none; } } @media (max-width: 640px) { .action-head { padding: 18px; }.action-row { grid-template-columns: 28px 1fr; padding: 15px 18px; gap: 12px; }.action-toggle { grid-column: 2; width: fit-content; }.action-tabs { padding: 12px 18px; } }
</style>
