<script>
  import { onMount } from 'svelte';
  
  let visible = false;
  
  onMount(() => {
    setTimeout(() => visible = true, 100);
  });
  
  const features = [
    {
      icon: '🌍',
      title: 'Real-Time Global Monitoring',
      description: 'Track carbon emissions across your entire data center portfolio with live updates every 5 minutes.',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    {
      icon: '🤖',
      title: 'AI-Powered Predictions',
      description: 'Machine learning algorithms forecast emissions trends and suggest optimization strategies.',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    },
    {
      icon: '📊',
      title: 'Advanced Analytics',
      description: 'Deep insights into your carbon footprint with interactive visualizations and custom reports.',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    },
    {
      icon: '⚡',
      title: 'Instant Alerts',
      description: 'Get notified immediately when emissions exceed thresholds or anomalies are detected.',
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    },
    {
      icon: '🎯',
      title: 'Goal Tracking',
      description: 'Set net-zero targets and monitor progress with visual indicators and milestone tracking.',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    },
    {
      icon: '🔒',
      title: 'Enterprise Security',
      description: 'Bank-level encryption, SOC 2 compliance, and role-based access control for your data.',
      gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)'
    }
  ];
</script>

<section class="features-section" class:visible>
  <div class="container">
    <div class="header">
      <h2 class="title">Everything you need.<br/>Nothing you don't.</h2>
      <p class="subtitle">
        Powerful features designed for enterprise-scale carbon management
      </p>
    </div>
    
    <div class="features-grid">
      {#each features as feature, i}
        <div class="feature-card" style="--delay: {i * 0.1}s">
          <div class="feature-icon" style="background: {feature.gradient}">
            <span>{feature.icon}</span>
          </div>
          <h3 class="feature-title">{feature.title}</h3>
          <p class="feature-description">{feature.description}</p>
          <div class="feature-glow" style="background: {feature.gradient}"></div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .features-section {
    position: relative;
    padding: 120px 0;
    background: linear-gradient(180deg, #f5f5f7 0%, #ffffff 50%, #f5f5f7 100%);
    overflow: hidden;
  }
  
  .features-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 1400px;
    height: 100%;
    background: radial-gradient(ellipse at center, rgba(44,173,132,0.03) 0%, transparent 70%);
    pointer-events: none;
  }
  
  .container {
    width: min(calc(100% - 48px), 1200px);
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }
  
  .header {
    text-align: center;
    margin-bottom: 80px;
    opacity: 0;
    transform: translateY(30px);
    animation: fadeInUp 0.8s ease-out 0.2s forwards;
  }
  
  @keyframes fadeInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .title {
    font-size: clamp(36px, 5vw, 56px);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, #1d1d1f 0%, #424245 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
  }
  
  .subtitle {
    font-size: 20px;
    color: #6e6e73;
    font-weight: 400;
    letter-spacing: -0.01em;
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 24px;
  }
  
  .feature-card {
    position: relative;
    padding: 40px 32px;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 0;
    transform: translateY(40px);
    animation: cardFadeIn 0.8s ease-out var(--delay) forwards;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  }
  
  @keyframes cardFadeIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,0,0,0.1);
    box-shadow: 0 12px 32px rgba(0,0,0,0.08);
  }
  
  .feature-card:hover .feature-glow {
    opacity: 0.08;
  }
  
  .feature-card:hover .feature-icon {
    transform: scale(1.05);
  }
  
  .feature-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    opacity: 0;
    transition: opacity 0.5s ease;
    pointer-events: none;
    filter: blur(80px);
  }
  
  .feature-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin-bottom: 20px;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  
  .feature-title {
    font-size: 21px;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #1d1d1f;
    margin-bottom: 10px;
    line-height: 1.3;
  }
  
  .feature-description {
    font-size: 15px;
    line-height: 1.6;
    color: #6e6e73;
    font-weight: 400;
  }
  
  @media (max-width: 768px) {
    .features-section {
      padding: 80px 0;
    }
    
    .header {
      margin-bottom: 60px;
    }
    
    .features-grid {
      grid-template-columns: 1fr;
      gap: 20px;
    }
    
    .feature-card {
      padding: 32px 24px;
    }
  }
</style>
