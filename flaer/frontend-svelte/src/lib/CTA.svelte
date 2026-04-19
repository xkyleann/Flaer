<script>
  let email = '';
  let submitted = false;

  function handleSubmit() {
    if (email && email.includes('@')) {
      submitted = true;
      email = '';
      setTimeout(() => {
        submitted = false;
      }, 3000);
    }
  }
</script>

<div id="cta" class="cta-block">
  <div class="cta-inner glass-card-dark">
    <div class="cta-copy">
      <h2>Bring carbon intelligence into infrastructure planning.</h2>
      <p>Request a private demo for your team. Early design partners receive guided onboarding and a structured pilot plan.</p>
    </div>
    <div>
      <form class="cta-form" on:submit|preventDefault={handleSubmit}>
        <input 
          class="cta-input" 
          bind:value={email}
          placeholder="work@company.com" 
          type="email"
          required
        />
        <button class="cta-btn" type="submit">
          {submitted ? 'Request received ✓' : 'Request access'}
        </button>
      </form>
      <p class="cta-note">Enterprise pilots available · No credit card required · Response directed to business email only</p>
    </div>
  </div>
</div>

<style>
  .cta-block {
    padding: 0 24px 72px;
  }

  .cta-inner {
    width: min(1240px, 100%);
    margin: 0 auto;
    border-radius: 36px;
    color: var(--text);
    padding: 38px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 20px;
    align-items: center;
    animation: fadeInUp 0.8s ease-out;
  }

  .glass-card-dark {
    background: linear-gradient(135deg, rgba(14,29,24,0.92), rgba(19,38,31,0.88));
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow:
      0 40px 100px rgba(0,0,0,0.35),
      0 15px 40px rgba(0,0,0,0.25);
    backdrop-filter: blur(50px);
    -webkit-backdrop-filter: blur(50px);
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
  }

  .glass-card-dark::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(44,173,132,0.15), transparent 70%);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% {
      transform: translate(0, 0);
    }
    50% {
      transform: translate(-20px, -20px);
    }
  }

  .glass-card-dark:hover {
    transform: translateY(-4px);
    box-shadow:
      0 50px 120px rgba(0,0,0,0.4),
      0 20px 50px rgba(0,0,0,0.3);
    border-color: rgba(255,255,255,0.22);
  }

  h2 {
    color: var(--text);
    font-size: clamp(2rem, 4vw, 3rem);
    line-height: 1.02;
    margin-bottom: 10px;
    letter-spacing: -0.05em;
  }

  p {
    color: var(--text-soft);
    max-width: 640px;
  }

  .cta-form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .cta-input {
    min-width: 280px;
    border: 1px solid rgba(255,255,255,0.16);
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 999px;
    padding: 14px 18px;
    outline: none;
    transition: all 0.2s ease;
    font-family: inherit;
    font-size: 14px;
  }

  .cta-input:focus {
    border-color: rgba(255,255,255,0.24);
    background: rgba(255,255,255,0.12);
    box-shadow: 0 0 0 4px rgba(44,173,132,0.12);
  }

  .cta-input::placeholder {
    color: rgba(244,247,245,0.50);
  }

  .cta-btn {
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 999px;
    padding: 14px 20px;
    font-weight: 800;
    cursor: pointer;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    box-shadow: 0 8px 24px rgba(183,149,99,0.24);
    transition: all 0.2s ease;
    font-family: inherit;
    font-size: 14px;
  }

  .cta-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(183,149,99,0.32);
  }

  .cta-note {
    color: var(--text-muted);
    font-size: 12px;
    margin-top: 10px;
  }

  @media (max-width: 860px) {
    .cta-inner {
      grid-template-columns: 1fr;
    }

    .cta-block {
      padding-inline: 14px;
    }
  }
</style>