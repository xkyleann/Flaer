<script>
  import { readinessCards } from './data.js';
  import Icon from './Icon.svelte';
</script>

<section id="readiness">
  <div class="inner w">
    <div class="section-head">
      <div class="eyebrow-light">Enterprise Readiness</div>
      <h2>Built for the requirements that matter to enterprise buyers.</h2>
    </div>

    <div class="cards">
      {#each readinessCards as card}
        <div class="card">
          <div class="card-icon">
            <Icon name={card.icon} size={18} />
          </div>
          <h3>{card.title}</h3>
          <p>{card.body}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  section {
    background: var(--paper);
    padding: 80px 0 100px;
    border-top: 1px solid rgba(0,0,0,0.06);
  }

  .section-head {
    margin-bottom: 40px;
  }

  .eyebrow-light {
    display: inline-flex;
    align-items: center;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 12px;
  }

  h2 {
    font-size: clamp(22px, 2.8vw, 32px);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.02em;
    color: var(--ink);
    max-width: 560px;
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: var(--radius-lg);
    padding: 28px 30px;
    transition: transform 0.18s, box-shadow 0.18s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }

  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 36px rgba(0,0,0,0.09);
    border-color: rgba(35,145,108,0.15);
  }

  .card-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(35,145,108,0.08);
    border: 1px solid rgba(35,145,108,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    color: var(--green);
  }

  h3 {
    font-size: 15px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
  }

  p {
    font-size: 13.5px;
    line-height: 1.65;
    color: var(--ink-soft);
  }

  @media (max-width: 600px) {
    .cards { grid-template-columns: 1fr; }
  }
</style>
