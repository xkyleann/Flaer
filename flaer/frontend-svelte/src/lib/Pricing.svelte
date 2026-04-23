<script>
  import { pricingTiers } from './data.js';
  import Icon from './Icon.svelte';
  import { onMount } from 'svelte';

  let visible = false;

  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible = true;
        }
      });
    }, { threshold: 0.1 });

    const section = document.getElementById('pricing');
    if (section) observer.observe(section);

    return () => observer.disconnect();
  });
</script>

<section id="pricing">
  <div class="inner w">
    <div class="section-head" class:visible>
      <div class="eyebrow-light">Pricing</div>
      <h2>Simple, transparent pricing.</h2>
      <p class="head-body">Choose the plan that fits your infrastructure. Scale as you grow.</p>
    </div>

    <div class="cards">
      {#each pricingTiers as tier, i}
        <div class="card" class:featured={tier.featured} class:visible style="animation-delay: {i * 0.1}s">
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
                <span class="tick"><Icon name="check" size={14} /></span>
                <span>{f}</span>
              </li>
            {/each}
          </ul>

          <button
            class="cta-btn"
            class:cta-primary={tier.featured}
            class:cta-ghost={!tier.featured}
            on:click={() => document.getElementById('cta')?.scrollIntoView({ behavior: 'smooth' })}
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
    padding: 120px 0;
    border-top: 0.5px solid rgba(0,0,0,0.08);
    position: relative;
  }

  .section-head {
    text-align: center;
    margin-bottom: 64px;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s var(--ease-out);
  }

  .section-head.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .eyebrow-light {
    display: inline-flex;
    align-items: center;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 12px;
  }

  h2 {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -0.025em;
    color: var(--ink);
    margin-bottom: 16px;
  }

  .head-body {
    font-size: 19px;
    line-height: 1.47059;
    color: var(--ink-soft);
    letter-spacing: -0.022em;
    max-width: 600px;
    margin: 0 auto;
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    align-items: start;
  }

  .card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: var(--radius-lg);
    padding: 40px 32px;
    display: flex;
    flex-direction: column;
    transition: all 0.4s var(--ease-out);
    box-shadow: var(--shadow-sm);
    position: relative;
    opacity: 0;
    transform: translateY(30px);
  }

  .card.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(0,0,0,0.15);
  }

  .card.featured {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid var(--blue);
    box-shadow:
      0 0 0 1px rgba(10,132,255,0.1),
      var(--shadow-md);
    transform: translateY(-12px) scale(1.02);
  }

  .card.featured.visible {
    transform: translateY(-12px) scale(1.02);
  }

  .card.featured:hover {
    transform: translateY(-16px) scale(1.02);
    box-shadow:
      0 0 0 1px rgba(10,132,255,0.2),
      var(--shadow-lg);
  }

  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    color: var(--blue);
    background: rgba(10,132,255,0.1);
    border: 1px solid rgba(10,132,255,0.2);
    padding: 6px 14px;
    border-radius: 980px;
    margin-bottom: 20px;
    width: fit-content;
    letter-spacing: 0.02em;
  }

  .tier-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--ink-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
  }

  .price-row {
    display: flex;
    align-items: baseline;
    gap: 4px;
    margin-bottom: 12px;
  }

  .price {
    font-size: 56px;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--ink);
    line-height: 1;
  }

  .period {
    font-size: 17px;
    color: var(--ink-muted);
    font-weight: 400;
    letter-spacing: -0.022em;
  }

  .tier-desc {
    font-size: 15px;
    line-height: 1.47059;
    color: var(--ink-soft);
    margin-bottom: 0;
    letter-spacing: -0.022em;
  }

  .divider {
    border: none;
    border-top: 1px solid rgba(0,0,0,0.08);
    margin: 28px 0;
  }

  .features {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 32px;
    flex: 1;
  }

  .features li {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 15px;
    color: var(--ink-soft);
    line-height: 1.47059;
    letter-spacing: -0.022em;
  }

  .tick {
    color: var(--blue);
    flex-shrink: 0;
    margin-top: 2px;
    display: flex;
    align-items: center;
  }

  .cta-btn {
    width: 100%;
    padding: 14px 24px;
    border-radius: 980px;
    font-size: 17px;
    font-weight: 400;
    letter-spacing: -0.022em;
    transition: all 0.3s var(--ease-out);
    cursor: pointer;
  }

  .cta-primary {
    background: var(--blue);
    color: #fff;
    border: none;
    box-shadow: 0 4px 12px rgba(10,132,255,0.3);
  }

  .cta-primary:hover {
    background: #0077ed;
    box-shadow: 0 6px 20px rgba(10,132,255,0.4);
    transform: scale(1.02);
  }

  .cta-primary:active {
    transform: scale(0.98);
  }

  .cta-ghost {
    background: transparent;
    border: 1.5px solid rgba(0,0,0,0.15);
    color: var(--ink);
  }

  .cta-ghost:hover {
    border-color: var(--blue);
    color: var(--blue);
    background: rgba(10,132,255,0.05);
    transform: scale(1.02);
  }

  .cta-ghost:active {
    transform: scale(0.98);
  }

  @media (max-width: 1024px) {
    .cards {
      grid-template-columns: 1fr;
      max-width: 480px;
      margin: 0 auto;
    }
    .card.featured {
      transform: none;
    }
    .card.featured.visible {
      transform: translateY(0);
    }
  }
</style>
