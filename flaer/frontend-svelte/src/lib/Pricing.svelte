<script>
  import { pricingTiers } from './data.js';
  import Icon from './Icon.svelte';
</script>

<section id="pricing">
  <div class="inner w">
    <div class="section-head">
      <div class="eyebrow-light">Pricing</div>
      <h2>Start free. Scale to enterprise.</h2>
      <p class="head-body">Transparent pricing built for infrastructure teams. No seat fees, no surprise overage charges.</p>
    </div>

    <div class="cards">
      {#each pricingTiers as tier}
        <div class="card" class:featured={tier.featured}>
          {#if tier.badge}
            <div class="badge">{tier.badge}</div>
          {/if}

          <div class="tier-name">{tier.name}</div>

          <div class="price-row">
            <span class="price">{tier.price}</span>
            {#if tier.period}
              <span class="period">{tier.period}</span>
            {/if}
          </div>

          <p class="tier-desc">{tier.description}</p>

          <hr class="divider"/>

          <ul class="features">
            {#each tier.features as f}
              <li>
                <span class="tick"><Icon name="check" size={13} /></span>
                {f}
              </li>
            {/each}
          </ul>

          <button
            class="cta-btn"
            class:cta-primary={tier.featured}
            class:cta-ghost={!tier.featured}
            onclick={() => document.getElementById('cta')?.scrollIntoView({ behavior: 'smooth' })}
          >
            {tier.cta}
          </button>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  section {
    background: var(--paper);
    padding: 100px 0;
    border-top: 1px solid rgba(0,0,0,0.06);
  }

  .section-head {
    text-align: center;
    margin-bottom: 52px;
  }

  .eyebrow-light {
    display: inline-flex;
    align-items: center;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 14px;
  }

  h2 {
    font-size: clamp(26px, 3.2vw, 40px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin-bottom: 14px;
  }

  .head-body {
    font-size: 15px;
    color: var(--ink-soft);
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    align-items: start;
  }

  .card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: var(--radius-xl);
    padding: 30px;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    position: relative;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.10);
  }

  .card.featured {
    border-color: rgba(35,145,108,0.3);
    box-shadow:
      0 0 0 1px rgba(35,145,108,0.15),
      0 20px 50px rgba(35,145,108,0.12);
    transform: translateY(-6px);
  }

  .card.featured:hover {
    transform: translateY(-10px);
    box-shadow:
      0 0 0 1px rgba(35,145,108,0.22),
      0 28px 64px rgba(35,145,108,0.18);
  }

  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    color: var(--green);
    background: rgba(35,145,108,0.09);
    border: 1px solid rgba(35,145,108,0.18);
    padding: 5px 12px;
    border-radius: 99px;
    margin-bottom: 16px;
    width: fit-content;
  }

  .tier-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
  }

  .price-row {
    display: flex;
    align-items: baseline;
    gap: 3px;
    margin-bottom: 10px;
  }

  .price {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: var(--ink);
    line-height: 1;
  }

  .period {
    font-size: 16px;
    color: var(--ink-muted);
    font-weight: 500;
  }

  .tier-desc {
    font-size: 13.5px;
    line-height: 1.55;
    color: var(--ink-soft);
    margin-bottom: 0;
  }

  .divider {
    border: none;
    border-top: 1px solid rgba(0,0,0,0.07);
    margin: 22px 0;
  }

  .features {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 28px;
    flex: 1;
  }

  .features li {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 13.5px;
    color: var(--ink-soft);
    line-height: 1.4;
  }

  .tick {
    color: var(--green);
    flex-shrink: 0;
    margin-top: 2px;
    display: flex;
    align-items: center;
  }

  .cta-btn {
    width: 100%;
    padding: 13px 20px;
    border-radius: 99px;
    font-size: 14px;
    font-weight: 700;
    transition: all 0.18s;
    cursor: pointer;
  }

  .cta-primary {
    background: linear-gradient(135deg, var(--green) 0%, var(--green-2) 100%);
    color: #fff;
    border: none;
    box-shadow: 0 6px 20px rgba(35,145,108,0.3);
  }

  .cta-primary:hover {
    box-shadow: 0 10px 28px rgba(35,145,108,0.4);
    transform: translateY(-1px);
  }

  .cta-ghost {
    background: transparent;
    border: 1px solid rgba(0,0,0,0.12);
    color: var(--ink);
  }

  .cta-ghost:hover {
    border-color: var(--green);
    color: var(--green);
    background: rgba(35,145,108,0.04);
    transform: translateY(-1px);
  }

  @media (max-width: 900px) {
    .cards { grid-template-columns: 1fr; }
    .card.featured { transform: none; }
  }
</style>
