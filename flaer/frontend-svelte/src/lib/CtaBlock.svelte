<script>
  import analytics from './utils/analytics.js';
  
  let email = '';
  let submitted = false;
  let error = false;
  let loading = false;

  async function handleSubmit(e) {
    e.preventDefault();
    
    // Track form interaction
    analytics.trackCTA('Demo Request Form', 'submit_attempt');
    
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      error = true;
      analytics.trackFormSubmit('Demo Request', false);
      return;
    }
    
    error = false;
    loading = true;
    
    try {
      // Store email for demo purposes (in production, send to backend)
      console.log('Demo request submitted:', email);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Store in localStorage for demo
      const requests = JSON.parse(localStorage.getItem('demo_requests') || '[]');
      requests.push({ email, timestamp: new Date().toISOString() });
      localStorage.setItem('demo_requests', JSON.stringify(requests));
      
      // Track successful submission
      analytics.trackFormSubmit('Demo Request', true);
      analytics.trackEvent('Lead', 'Demo Request', email.split('@')[1]);
      
      submitted = true;
      email = '';
      
      // Reset after 5 seconds
      setTimeout(() => {
        submitted = false;
      }, 5000);
    } catch (err) {
      console.error('Error submitting request:', err);
      error = true;
      analytics.trackFormSubmit('Demo Request', false);
    } finally {
      loading = false;
    }
  }
</script>

<section id="cta">
  <div class="inner w">
    <div class="copy">
      <div class="eyebrow">Get early access</div>
      <h2>Bring carbon intelligence into your infrastructure planning.</h2>
      <p>Request a private demo for your team. Early design partners receive guided onboarding and a structured pilot plan tailored to your CSRD timeline.</p>
    </div>

    <div class="form-side">
      <form on:submit={handleSubmit}>
        <div class="input-row">
          <input
            type="email"
            bind:value={email}
            placeholder="work@company.com"
            class:has-error={error}
            disabled={submitted || loading}
            required
          />
          <button
            type="submit"
            class:success={submitted}
            class:loading={loading}
            disabled={submitted || loading}
          >
            {#if loading}
              Sending...
            {:else if submitted}
              Request received ✓
            {:else}
              Request access
            {/if}
          </button>
        </div>
        {#if error}
          <p class="error-msg">Please enter a valid work email address.</p>
        {/if}
        {#if submitted}
          <p class="success-msg">✓ Thank you! We'll be in touch within 24 hours.</p>
        {/if}
      </form>
      <p class="note">Enterprise pilots available · No credit card required · EU data residency</p>
    </div>
  </div>
</section>

<style>
  section {
    background: linear-gradient(135deg, #061310 0%, #0a1f18 100%);
    padding: 90px 0;
    position: relative;
    overflow: hidden;
  }

  section::before {
    content: '';
    position: absolute;
    top: -200px;
    right: -200px;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(44,173,132,0.08), transparent 70%);
    pointer-events: none;
  }

  section::after {
    content: '';
    position: absolute;
    bottom: -150px;
    left: -100px;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(183,149,99,0.06), transparent 70%);
    pointer-events: none;
  }

  .inner {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
    position: relative;
    z-index: 1;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green-2);
    margin-bottom: 16px;
  }

  h2 {
    font-size: clamp(26px, 3.2vw, 40px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.025em;
    color: #f4f7f5;
    margin-bottom: 14px;
  }

  p {
    font-size: 15px;
    line-height: 1.65;
    color: rgba(244,247,245,0.6);
  }

  form {
    width: 100%;
  }

  .input-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  input {
    flex: 1;
    min-width: 220px;
    padding: 14px 20px;
    border-radius: 99px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.07);
    color: #f4f7f5;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.18s, background 0.18s, box-shadow 0.18s;
  }

  input::placeholder {
    color: rgba(244,247,245,0.38);
  }

  input:focus {
    border-color: rgba(44,173,132,0.5);
    background: rgba(255,255,255,0.10);
    box-shadow: 0 0 0 4px rgba(44,173,132,0.10);
  }

  input.has-error {
    border-color: rgba(211,93,92,0.5);
    box-shadow: 0 0 0 4px rgba(211,93,92,0.08);
  }

  button[type="submit"] {
    padding: 14px 26px;
    border-radius: 99px;
    font-size: 14px;
    font-weight: 700;
    font-family: inherit;
    background: linear-gradient(135deg, var(--green) 0%, var(--green-2) 100%);
    color: #fff;
    border: none;
    cursor: pointer;
    white-space: nowrap;
    transition: opacity 0.18s, transform 0.15s, background 0.3s;
  }

  button[type="submit"]:hover:not(:disabled) {
    opacity: 0.9;
    transform: translateY(-1px);
  }

  button[type="submit"].success {
    background: linear-gradient(135deg, #1a6247 0%, #23916c 100%);
    cursor: default;
  }

  button[type="submit"]:disabled {
    opacity: 0.85;
  }

  .error-msg {
    font-size: 12px;
    color: var(--red);
    margin-top: 8px;
    padding-left: 4px;
  }
  
  .success-msg {
    font-size: 12px;
    color: var(--green-2);
    margin-top: 8px;
    padding-left: 4px;
    font-weight: 500;
  }

  .note {
    font-size: 11.5px;
    color: rgba(244,247,245,0.35);
    margin-top: 12px;
  }
  
  button.loading {
    opacity: 0.7;
    cursor: wait;
  }

  @media (max-width: 760px) {
    .inner { grid-template-columns: 1fr; }
    .input-row { flex-direction: column; }
    input { min-width: 0; }
    button[type="submit"] { width: 100%; justify-content: center; }
  }
</style>
