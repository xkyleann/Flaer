<script>
  import { onMount } from 'svelte';
  
  let visible = false;
  
  onMount(() => {
    setTimeout(() => visible = true, 100);
  });
  
  const badges = [
    { icon: '🔒', text: 'SOC 2 Type II Certified' },
    { icon: '🇪🇺', text: 'GDPR Compliant' },
    { icon: '✓', text: 'ISO 27001 Certified' },
    { icon: '⚡', text: '99.9% Uptime SLA' }
  ];
  
  const logos = [
    { name: 'Fortune 500', opacity: 0.6 },
    { name: 'Enterprise', opacity: 0.5 },
    { name: 'Global 2000', opacity: 0.55 },
    { name: 'Tech Leaders', opacity: 0.5 }
  ];
</script>

<section class="trust-section" class:visible>
  <div class="container">
    <div class="trust-header">
      <p class="trust-label">Trusted by leading enterprises</p>
    </div>
    
    <div class="badges-grid">
      {#each badges as badge, i}
        <div class="badge-item" style="--delay: {i * 0.1}s">
          <span class="badge-icon">{badge.icon}</span>
          <span class="badge-text">{badge.text}</span>
        </div>
      {/each}
    </div>
    
    <div class="stats-row">
      <div class="stat-item">
        <div class="stat-value">40+</div>
        <div class="stat-label">Enterprise Clients</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-value">11,000+</div>
        <div class="stat-label">Data Centers Tracked</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-value">€2.1M</div>
        <div class="stat-label">Avg. Annual Savings</div>
      </div>
    </div>
  </div>
</section>

<style>
  .trust-section {
    padding: 80px 0;
    background: linear-gradient(180deg, #ffffff 0%, #f5f5f7 100%);
    border-top: 1px solid rgba(0,0,0,0.06);
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  }
  
  .trust-section.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .container {
    width: min(calc(100% - 48px), 1200px);
    margin: 0 auto;
  }
  
  .trust-header {
    text-align: center;
    margin-bottom: 48px;
  }
  
  .trust-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #6e6e73;
  }
  
  .badges-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    margin-bottom: 60px;
  }
  
  .badge-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 24px;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out var(--delay) forwards;
    transition: all 0.3s ease;
  }
  
  @keyframes fadeInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .badge-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    border-color: rgba(44,173,132,0.3);
  }
  
  .badge-icon {
    font-size: 24px;
    flex-shrink: 0;
  }
  
  .badge-text {
    font-size: 14px;
    font-weight: 600;
    color: #1d1d1f;
    letter-spacing: -0.01em;
  }
  
  .stats-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    padding: 40px 0;
    border-top: 1px solid rgba(0,0,0,0.08);
  }
  
  .stat-item {
    flex: 1;
    text-align: center;
    padding: 0 40px;
  }
  
  .stat-value {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #1d1d1f 0%, #2cad84 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }
  
  .stat-label {
    font-size: 13px;
    color: #6e6e73;
    font-weight: 500;
  }
  
  .stat-divider {
    width: 1px;
    height: 60px;
    background: rgba(0,0,0,0.1);
    flex-shrink: 0;
  }
  
  @media (max-width: 768px) {
    .trust-section {
      padding: 60px 0;
    }
    
    .badges-grid {
      grid-template-columns: 1fr;
      gap: 16px;
      margin-bottom: 40px;
    }
    
    .stats-row {
      flex-direction: column;
      gap: 32px;
    }
    
    .stat-divider {
      width: 60px;
      height: 1px;
    }
    
    .stat-item {
      padding: 0;
    }
    
    .stat-value {
      font-size: 36px;
    }
  }
</style>