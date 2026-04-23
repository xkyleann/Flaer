<script>
  function goBack() {
    window.location.hash = '#home';
  }
</script>

<div class="legal-page">
  <div class="legal-header">
    <button class="back-button" on:click={goBack}>
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Back to Home
    </button>
  </div>

  <div class="legal-content">
    <h1>Privacy Policy</h1>
    <p class="legal-updated">Last updated: April 20, 2026</p>
    
    <section>
      <h2>1. Information We Collect</h2>
      <p>Flaer collects information necessary to provide carbon intelligence services to enterprise clients. This includes:</p>
      <ul>
        <li><strong>Account Information:</strong> Name, email, company details, and authentication credentials</li>
        <li><strong>Usage Data:</strong> Dashboard interactions, feature usage, and system performance metrics</li>
        <li><strong>Infrastructure Data:</strong> Data center locations, energy consumption, and carbon emissions data</li>
        <li><strong>Technical Data:</strong> IP addresses, browser type, device information, and access logs</li>
      </ul>
    </section>

    <section>
      <h2>2. How We Use Your Information</h2>
      <p>We use collected information to:</p>
      <ul>
        <li>Provide real-time carbon intelligence and emissions tracking</li>
        <li>Generate compliance reports (CSRD, EED, SFDR)</li>
        <li>Improve platform performance and user experience</li>
        <li>Communicate service updates and security notifications</li>
        <li>Ensure platform security and prevent fraud</li>
      </ul>
    </section>

    <section>
      <h2>3. Data Security</h2>
      <p>Flaer implements enterprise-grade security measures including:</p>
      <ul>
        <li>End-to-end encryption for data in transit and at rest</li>
        <li>Multi-factor authentication (MFA) and role-based access control (RBAC)</li>
        <li>Regular security audits and penetration testing</li>
        <li>SOC 2 Type II and ISO 27001 compliance</li>
        <li>24/7 security monitoring and incident response</li>
      </ul>
    </section>

    <section>
      <h2>4. Data Sharing</h2>
      <p>We do not sell your data. We may share information with:</p>
      <ul>
        <li><strong>Service Providers:</strong> Cloud infrastructure, analytics, and security services</li>
        <li><strong>Regulatory Bodies:</strong> When required by law or compliance obligations</li>
        <li><strong>Business Partners:</strong> With explicit consent for integration purposes</li>
      </ul>
    </section>

    <section>
      <h2>5. Your Rights</h2>
      <p>You have the right to:</p>
      <ul>
        <li>Access, correct, or delete your personal data</li>
        <li>Export your data in machine-readable format</li>
        <li>Opt-out of non-essential communications</li>
        <li>Request data processing restrictions</li>
        <li>Lodge complaints with supervisory authorities</li>
      </ul>
    </section>

    <section>
      <h2>6. Data Retention</h2>
      <p>We retain your data for as long as your account is active or as needed to provide services. After account closure, data is retained for 90 days before permanent deletion, except where longer retention is required by law.</p>
    </section>

    <section>
      <h2>7. International Data Transfers</h2>
      <p>Flaer operates globally. Your data may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place for international transfers, including Standard Contractual Clauses (SCCs) approved by the European Commission.</p>
    </section>

    <section>
      <h2>8. Contact Us</h2>
      <p>For privacy inquiries or to exercise your rights:</p>
      <ul>
        <li>Email: <a href="mailto:privacy@flaer.io">privacy@flaer.io</a></li>
        <li>Data Protection Officer: <a href="mailto:dpo@flaer.io">dpo@flaer.io</a></li>
        <li>Address: Flaer, Inc., 1 Infinite Loop, Cupertino, CA 95014</li>
      </ul>
    </section>
  </div>
</div>

<style>
  .legal-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    padding: 40px 20px 80px;
  }

  .legal-header {
    max-width: 800px;
    margin: 0 auto 40px;
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: white;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #1a1a1a;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .back-button:hover {
    background: #f8f9fa;
    border-color: rgba(0,0,0,0.15);
    transform: translateX(-2px);
  }

  .back-button svg {
    transition: transform 0.2s ease;
  }

  .back-button:hover svg {
    transform: translateX(-2px);
  }

  .legal-content {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    padding: 60px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }

  h1 {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #1a1a1a;
    margin: 0 0 12px 0;
  }

  .legal-updated {
    font-size: 14px;
    color: #666;
    margin: 0 0 48px 0;
  }

  section {
    margin-bottom: 48px;
  }

  section:last-child {
    margin-bottom: 0;
  }

  h2 {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: #1a1a1a;
    margin: 0 0 20px 0;
  }

  p {
    font-size: 16px;
    line-height: 1.7;
    color: #333;
    margin: 0 0 16px 0;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 16px 0;
  }

  li {
    font-size: 16px;
    line-height: 1.7;
    color: #333;
    padding-left: 28px;
    margin-bottom: 12px;
    position: relative;
  }

  li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 10px;
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
  }

  a {
    color: #10b981;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  a:hover {
    color: #059669;
    text-decoration: underline;
  }

  strong {
    font-weight: 600;
    color: #1a1a1a;
  }

  @media (max-width: 768px) {
    .legal-content {
      padding: 40px 24px;
    }

    h1 {
      font-size: 32px;
    }

    h2 {
      font-size: 22px;
    }

    p, li {
      font-size: 15px;
    }
  }
</style>
