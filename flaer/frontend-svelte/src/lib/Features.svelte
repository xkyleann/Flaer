<script>
  const features = [
    {
      step: '01',
      title: 'Map owned, leased, and colocated infrastructure',
      description: 'Consolidate facilities into one portfolio view, benchmark against regional grid conditions, and understand where operational carbon risk is concentrated.'
    },
    {
      step: '02',
      title: 'Forecast carbon trajectory before exposure becomes visible',
      description: 'Model energy demand and emissions over a ten-year horizon using scenario-based assumptions, infrastructure context, and regional carbon trends.'
    },
    {
      step: '03',
      title: 'Prioritize actions by operating impact and compliance value',
      description: 'Surface the highest-confidence interventions with cost, carbon, and reporting implications for infrastructure teams and executives.'
    }
  ];
</script>

<section id="capabilities" class="section">
  <div class="shell">
    <div class="section-head">
      <div>
        <div class="eyebrow">Capabilities</div>
        <h2>From infrastructure visibility to action-ready decarbonization strategy.</h2>
      </div>
      <p class="section-copy">The product combines portfolio mapping, long-range forecasting, and ranked operational interventions in one system designed for enterprise buyers.</p>
    </div>

    <div class="feature-grid">
      {#each features as feature, i}
        <div class="feature-card glass-card-light" style="animation-delay: {i * 0.15}s">
          <div class="feature-step">Step {feature.step}</div>
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .section {
    padding: 44px 0;
  }

  .shell {
    width: min(calc(100% - 48px), var(--max));
    margin: 0 auto;
    position: relative;
  }

  .section-head {
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 24px;
    margin-bottom: 24px;
  }

  .eyebrow {
    color: var(--green);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .10em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  h2 {
    font-size: clamp(2rem, 4vw, 3rem);
    line-height: 1.02;
    letter-spacing: -0.05em;
    color: var(--ink);
    max-width: 720px;
  }

  .section-copy {
    max-width: 520px;
    color: var(--ink-soft);
    font-size: 15px;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
  }

  .glass-card-light {
    border-radius: 28px;
    padding: 30px;
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(10,20,15,0.06);
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease-out both;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .glass-card-light:hover {
    transform: translateY(-8px);
    box-shadow: 0 32px 80px rgba(8,18,15,0.24);
    border-color: rgba(35,145,108,0.18);
    background: rgba(255,255,255,0.92);
  }

  .glass-card-light::before {
    content: "";
    position: absolute;
    inset: auto -30px -40px auto;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(44,173,132,0.08), transparent 68%);
    transition: all 0.4s ease;
  }

  .glass-card-light:hover::before {
    background: radial-gradient(circle, rgba(44,173,132,0.15), transparent 68%);
    transform: scale(1.2);
  }

  .feature-step {
    display: inline-flex;
    align-items: center;
    padding: 7px 11px;
    border-radius: 999px;
    background: #f3f5f4;
    border: 1px solid rgba(10,20,15,0.06);
    color: var(--green);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 16px;
  }

  h3 {
    color: var(--ink);
    margin-bottom: 10px;
    letter-spacing: -0.04em;
    font-size: 18px;
  }

  p {
    color: var(--ink-soft);
    font-size: 14px;
    line-height: 1.6;
  }

  @media (max-width: 1100px) {
    .feature-grid {
      grid-template-columns: 1fr;
    }

    .section-head {
      flex-direction: column;
      align-items: start;
    }
  }
</style>