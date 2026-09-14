<script>
  import { capabilityCards } from './data.js';
  import Icon from './Icon.svelte';

  const filters = [
    { id: 'all',        label: 'All' },
    { id: 'risk',       label: 'By Risk' },
    { id: 'region',     label: 'By Region' },
    { id: 'compliance', label: 'By Compliance' },
  ];

  let activeFilter = $state('all');

  let visibleCards = $derived(
    activeFilter === 'all'
      ? capabilityCards
      : capabilityCards.filter(c => c.category === activeFilter)
  );
</script>

<section id="capabilities">
  <div class="inner w">
    <!-- Header -->
    <div class="section-head">
      <div class="left">
        <div class="eyebrow-light">How Flaer helps</div>
        <h2>Start with the decision your team needs to make.</h2>
      </div>
      <p class="head-body">Bring the operating, grid, and reporting context for each carbon decision into one focused workflow.</p>
    </div>

    <!-- Filter chips -->
    <div class="filters">
      {#each filters as f}
        <button
          class="chip"
          class:active={activeFilter === f.id}
          onclick={() => activeFilter = f.id}
        >
          {f.label}
        </button>
      {/each}
    </div>

    <!-- Cards -->
    <div class="cards">
      {#each visibleCards as card (card.id)}
        <div class="card">
          <div class="card-top-border" style="background: {card.borderColor};"></div>
          <div class="card-body">
            <div class="card-icon">
            <Icon name={card.icon} size={18} />
          </div>
            <h3>{card.title}</h3>
            <p>{card.body}</p>
          </div>
          <div class="card-footer">
            <span class="metric-badge">{card.metric}</span>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  section {
    background: var(--paper);
    padding: 100px 0;
  }

  .inner {
    display: flex;
    flex-direction: column;
    gap: 40px;
  }

  .section-head {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: end;
  }

  .eyebrow-light {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 14px;
  }

  h2 {
    font-size: clamp(24px, 3vw, 36px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.025em;
    color: var(--ink);
  }

  .head-body {
    font-size: 15px;
    line-height: 1.65;
    color: var(--ink-soft);
    align-self: end;
  }

  .filters {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .chip {
    padding: 8px 18px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid rgba(0,0,0,0.12);
    color: var(--ink-soft);
    background: rgba(255,255,255,0.7);
    transition: all 0.18s;
    cursor: pointer;
  }

  .chip:hover {
    border-color: var(--green);
    color: var(--green);
    background: rgba(35,145,108,0.05);
  }

  .chip.active {
    background: var(--green);
    color: #fff;
    border-color: var(--green);
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }

  .card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: var(--radius-lg);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }

  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.10);
  }

  .card-top-border {
    height: 3px;
    width: 100%;
  }

  .card-body {
    flex: 1;
    padding: 24px 24px 16px;
  }

  .card-icon {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: rgba(35,145,108,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
    color: var(--green);
  }

  h3 {
    font-size: 15px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 10px;
    line-height: 1.3;
    letter-spacing: -0.01em;
  }

  p {
    font-size: 13.5px;
    line-height: 1.65;
    color: var(--ink-soft);
  }

  .card-footer {
    padding: 12px 24px 16px;
    border-top: 1px solid rgba(0,0,0,0.05);
  }

  .metric-badge {
    font-size: 11px;
    font-weight: 700;
    color: var(--green);
    background: rgba(35,145,108,0.08);
    border: 1px solid rgba(35,145,108,0.15);
    padding: 4px 10px;
    border-radius: 99px;
    letter-spacing: 0.03em;
  }

  @media (max-width: 900px) {
    .cards { grid-template-columns: 1fr 1fr; }
    .section-head { grid-template-columns: 1fr; }
  }

  @media (max-width: 600px) {
    .cards { grid-template-columns: 1fr; }
  }
</style>
