<script>
  import analytics from './utils/analytics.js';
  
  let email = '';
  let submitted = false;
  let error = false;
  let loading = false;
  // Set VITE_BOOKING_URL to a Cal.com or Calendly event URL when deploying.
  const bookingUrl = import.meta.env.VITE_BOOKING_URL;

  async function handleSubmit(e) {
    e.preventDefault();
    
    // Track form interaction
    analytics.trackCTA('Consultation Request Form', 'submit_attempt');
    
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      error = true;
      analytics.trackFormSubmit('Consultation Request', false);
      return;
    }
    
    error = false;
    loading = true;
    
    try {
      // Store the request locally during development. Production should send it to a CRM or booking service.
      console.log('Consultation request submitted:', email);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Store in localStorage for demo
      const requests = JSON.parse(localStorage.getItem('consultation_requests') || '[]');
      requests.push({ email, timestamp: new Date().toISOString() });
      localStorage.setItem('consultation_requests', JSON.stringify(requests));
      
      // Track successful submission
      analytics.trackFormSubmit('Consultation Request', true);
      analytics.trackEvent('Lead', 'Consultation Request', email.split('@')[1]);
      
      submitted = true;
      email = '';
      
      // Reset after 5 seconds
      setTimeout(() => {
        submitted = false;
      }, 5000);
    } catch (err) {
      console.error('Error submitting request:', err);
      error = true;
      analytics.trackFormSubmit('Consultation Request', false);
    } finally {
      loading = false;
    }
  }
</script>

<section id="cta">
  <div class="inner w">
    <div class="copy">
      <div class="eyebrow">Talk to our team</div>
      <h2>Bring carbon intelligence into your infrastructure planning.</h2>
      <p>Request a private consultation for your team. We will shape the session around your portfolio, reporting priorities, and site-selection decisions.</p>

      <ol class="steps" aria-label="What happens after you request a consultation">
        <li><span>01</span><div><strong>Share your context</strong><small>Tell us where your team needs clearer carbon decisions.</small></div></li>
        <li><span>02</span><div><strong>Work through priorities</strong><small>Meet with a Flaer specialist for a focused working session.</small></div></li>
        <li><span>03</span><div><strong>Leave with a next step</strong><small>Get a practical view of the right workflow for your team.</small></div></li>
      </ol>
    </div>

    <div class="form-side">
      {#if bookingUrl}
        <div class="booking-card">
          <span class="booking-kicker">Scheduling</span>
          <h3>Choose a time that works for your team.</h3>
          <p>Reserve a private introduction with a Flaer specialist.</p>
          <a class="book-button" href={bookingUrl} target="_blank" rel="noreferrer">View available times <span>↗</span></a>
        </div>
      {:else}
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
              Request a date
            {/if}
          </button>
        </div>
        {#if error}
          <p class="error-msg">Please enter a valid work email address.</p>
        {/if}
        {#if submitted}
          <p class="success-msg">✓ Request received. We’ll confirm your selected time by email.</p>
        {/if}
        </form>
      {/if}
      <p class="note">Private consultation · Enterprise pilots available · EU data residency</p>
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

  .steps {
    list-style: none;
    margin: 30px 0 0;
    padding: 0;
    display: grid;
    gap: 14px;
  }

  .steps li {
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }

  .steps span {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--green-2);
    padding-top: 2px;
  }

  .steps strong,
  .steps small {
    display: block;
  }

  .steps strong {
    font-size: 13px;
    color: #f4f7f5;
    margin-bottom: 3px;
  }

  .steps small {
    font-size: 12px;
    line-height: 1.45;
    color: rgba(244,247,245,0.48);
  }

  form {
    width: 100%;
  }


  .booking-card {
    padding: 25px;
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 16px;
    background: rgba(255,255,255,.05);
  }

  .booking-kicker { color: var(--green-2); font-size: 11px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; }
  .booking-card h3 { color: #f4f7f5; font-size: 19px; letter-spacing: -.025em; line-height: 1.25; margin: 14px 0 8px; }
  .booking-card p { font-size: 13px; }
  .book-button { align-items: center; background: linear-gradient(135deg, var(--green), var(--green-2)); border-radius: 99px; color: #fff; display: inline-flex; font-size: 14px; font-weight: 700; gap: 12px; margin-top: 22px; padding: 13px 20px; }
  .book-button span { font-size: 17px; line-height: .7; }

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
