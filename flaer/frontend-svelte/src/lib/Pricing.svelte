<script>
  import { onMount } from 'svelte';
  
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
  const plans = [
    {
      name: 'Free',
      price: 0,
      period: 'forever',
      description: 'Perfect for getting started',
      features: [
        'Up to 3 data centers',
        'Up to 2 team members',
        '1,000 API calls/month',
        'Basic monitoring',
        'Carbon calculator',
        'Community support'
      ],
      cta: 'Get Started',
      highlighted: false,
      tier: 'free'
    },
    {
      name: 'Starter',
      price: 49,
      period: 'per month',
      description: 'For growing teams',
      features: [
        'Up to 10 data centers',
        'Up to 5 team members',
        '10,000 API calls/month',
        'All Free features',
        'Emissions forecasting',
        'Email alerts',
        'Priority email support'
      ],
      cta: 'Start Free Trial',
      highlighted: true,
      tier: 'starter'
    },
    {
      name: 'Professional',
      price: 199,
      period: 'per month',
      description: 'For serious operations',
      features: [
        'Up to 50 data centers',
        'Up to 20 team members',
        '100,000 API calls/month',
        'All Starter features',
        'Custom reports',
        'API access',
        'Advanced analytics',
        'Priority support'
      ],
      cta: 'Start Free Trial',
      highlighted: false,
      tier: 'professional'
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'contact us',
      description: 'For large organizations',
      features: [
        'Unlimited data centers',
        'Unlimited team members',
        'Unlimited API calls',
        'All Professional features',
        'White-label options',
        'On-premise deployment',
        'SLA guarantee',
        'Dedicated support',
        'Custom integrations'
      ],
      cta: 'Contact Sales',
      highlighted: false,
      tier: 'enterprise'
    }
  ];
  
  async function handleSelectPlan(tier) {
    if (tier === 'free') {
      // Redirect to signup
      window.location.href = '/register';
    } else if (tier === 'enterprise') {
      // Open contact form or email
      window.location.href = 'mailto:sales@flaer.io?subject=Enterprise Plan Inquiry';
    } else {
      // Redirect to checkout (will be implemented with Stripe)
      try {
        const response = await fetch(`${API_URL}/api/billing/create-checkout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({ plan: tier })
        });
        
        if (response.ok) {
          const data = await response.json();
          window.location.href = data.url;
        } else {
          // Not logged in, redirect to signup
          window.location.href = `/register?plan=${tier}`;
        }
      } catch (error) {
        console.error('Error:', error);
        window.location.href = `/register?plan=${tier}`;
      }
    }
  }
</script>

<section class="pricing-section">
  <div class="container">
    <div class="pricing-header">
      <h2>Simple, Transparent Pricing</h2>
      <p>Choose the plan that fits your needs. All plans include a 14-day free trial.</p>
    </div>
    
    <div class="pricing-grid">
      {#each plans as plan}
        <div class="pricing-card" class:highlighted={plan.highlighted}>
          {#if plan.highlighted}
            <div class="badge">Most Popular</div>
          {/if}
          
          <div class="plan-header">
            <h3>{plan.name}</h3>
            <div class="price">
              {#if typeof plan.price === 'number'}
                <span class="currency">$</span>
                <span class="amount">{plan.price}</span>
                <span class="period">/{plan.period}</span>
              {:else}
                <span class="amount custom">{plan.price}</span>
              {/if}
            </div>
            <p class="description">{plan.description}</p>
          </div>
          
          <ul class="features">
            {#each plan.features as feature}
              <li>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {feature}
              </li>
            {/each}
          </ul>
          
          <button 
            class="cta-button" 
            class:primary={plan.highlighted}
            on:click={() => handleSelectPlan(plan.tier)}
          >
            {plan.cta}
          </button>
        </div>
      {/each}
    </div>
    
    <div class="pricing-footer">
      <p>All plans include:</p>
      <div class="included-features">
        <span>✓ SSL encryption</span>
        <span>✓ 99.9% uptime SLA</span>
        <span>✓ GDPR compliant</span>
        <span>✓ Regular updates</span>
      </div>
    </div>
  </div>
</section>

<style>
  .pricing-section {
    padding: 80px 20px;
    background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .pricing-header {
    text-align: center;
    margin-bottom: 60px;
  }
  
  .pricing-header h2 {
    font-size: 42px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 16px;
  }
  
  .pricing-header p {
    font-size: 18px;
    color: #666;
  }
  
  .pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    margin-bottom: 60px;
  }
  
  .pricing-card {
    background: white;
    border-radius: 16px;
    padding: 40px 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    transition: all 0.3s ease;
    position: relative;
    border: 2px solid transparent;
  }
  
  .pricing-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  }
  
  .pricing-card.highlighted {
    border-color: #2563eb;
    box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
  }
  
  .badge {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    padding: 6px 20px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .plan-header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .plan-header h3 {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 16px;
  }
  
  .price {
    margin-bottom: 12px;
  }
  
  .currency {
    font-size: 24px;
    color: #666;
    vertical-align: top;
  }
  
  .amount {
    font-size: 48px;
    font-weight: 700;
    color: #1a1a1a;
  }
  
  .amount.custom {
    font-size: 36px;
  }
  
  .period {
    font-size: 16px;
    color: #666;
  }
  
  .description {
    font-size: 14px;
    color: #666;
  }
  
  .features {
    list-style: none;
    padding: 0;
    margin: 0 0 30px 0;
  }
  
  .features li {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    font-size: 15px;
    color: #4b5563;
  }
  
  .features svg {
    flex-shrink: 0;
    color: #10b981;
  }
  
  .cta-button {
    width: 100%;
    padding: 14px 24px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid #e5e7eb;
    background: white;
    color: #1a1a1a;
  }
  
  .cta-button:hover {
    border-color: #2563eb;
    color: #2563eb;
    transform: translateY(-2px);
  }
  
  .cta-button.primary {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    border-color: transparent;
  }
  
  .cta-button.primary:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    transform: translateY(-2px);
  }
  
  .pricing-footer {
    text-align: center;
    padding-top: 40px;
    border-top: 1px solid #e5e7eb;
  }
  
  .pricing-footer p {
    font-size: 16px;
    color: #666;
    margin-bottom: 16px;
  }
  
  .included-features {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 24px;
  }
  
  .included-features span {
    font-size: 14px;
    color: #10b981;
    font-weight: 500;
  }
  
  @media (max-width: 768px) {
    .pricing-header h2 {
      font-size: 32px;
    }
    
    .pricing-grid {
      grid-template-columns: 1fr;
    }
    
    .included-features {
      flex-direction: column;
      gap: 12px;
    }
  }
</style>
