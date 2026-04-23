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
    <h1>Terms of Service</h1>
    <p class="legal-updated">Last updated: April 20, 2026</p>
    
    <section>
      <h2>1. Agreement to Terms</h2>
      <p>By accessing Flaer's platform, you agree to these Terms of Service and our Privacy Policy. If you disagree with any part, you may not access the service.</p>
    </section>

    <section>
      <h2>2. Service Description</h2>
      <p>Flaer provides:</p>
      <ul>
        <li>Real-time carbon emissions tracking across 11,000+ data centers</li>
        <li>AI-powered compliance forecasting and regulatory alerts</li>
        <li>Automated CSRD, EED, and SFDR reporting</li>
        <li>Carbon intensity analytics and optimization recommendations</li>
        <li>Enterprise-grade dashboard and API access</li>
      </ul>
    </section>

    <section>
      <h2>3. User Responsibilities</h2>
      <p>You agree to:</p>
      <ul>
        <li>Provide accurate account and infrastructure information</li>
        <li>Maintain confidentiality of authentication credentials</li>
        <li>Use the platform in compliance with applicable laws</li>
        <li>Not attempt to breach security or access unauthorized data</li>
        <li>Not reverse engineer or copy platform features</li>
        <li>Not use the service for illegal or harmful purposes</li>
      </ul>
    </section>

    <section>
      <h2>4. Subscription and Billing</h2>
      <ul>
        <li><strong>Free Tier:</strong> Limited to 3 data centers, basic reporting</li>
        <li><strong>Professional:</strong> $2,499/month - Up to 25 data centers, full features</li>
        <li><strong>Enterprise:</strong> Custom pricing - Unlimited scale, dedicated support</li>
        <li>Billing is monthly or annual with automatic renewal</li>
        <li>Cancellation requires 30 days notice</li>
        <li>Refunds are provided on a case-by-case basis</li>
      </ul>
    </section>

    <section>
      <h2>5. Service Level Agreement (SLA)</h2>
      <p>Flaer commits to:</p>
      <ul>
        <li><strong>Uptime:</strong> 99.9% availability (excluding scheduled maintenance)</li>
        <li><strong>Support Response:</strong> Enterprise clients receive 24/7 support with 1-hour response time</li>
        <li><strong>Data Accuracy:</strong> Carbon data updated every 5 minutes from verified sources</li>
        <li><strong>Scheduled Maintenance:</strong> Announced 48 hours in advance, typically during low-traffic periods</li>
      </ul>
    </section>

    <section>
      <h2>6. Intellectual Property</h2>
      <p>All platform content, features, and functionality are owned by Flaer, Inc. and protected by international copyright, trademark, and other intellectual property laws. You may not:</p>
      <ul>
        <li>Copy, modify, or distribute platform content without permission</li>
        <li>Use Flaer's trademarks or branding without authorization</li>
        <li>Create derivative works based on the platform</li>
        <li>Remove or alter copyright notices</li>
      </ul>
    </section>

    <section>
      <h2>7. Data Ownership</h2>
      <p>You retain ownership of all data you input into Flaer. We claim no intellectual property rights over your data. You grant us a license to use your data solely to provide and improve our services.</p>
    </section>

    <section>
      <h2>8. Limitation of Liability</h2>
      <p>To the maximum extent permitted by law, Flaer shall not be liable for:</p>
      <ul>
        <li>Indirect, incidental, or consequential damages</li>
        <li>Loss of profits, data, or business opportunities</li>
        <li>Service interruptions or data inaccuracies</li>
        <li>Third-party actions or content</li>
      </ul>
      <p>Our total liability shall not exceed the amount paid by you in the 12 months preceding the claim.</p>
    </section>

    <section>
      <h2>9. Indemnification</h2>
      <p>You agree to indemnify and hold Flaer harmless from any claims, damages, or expenses arising from your use of the service, violation of these terms, or infringement of third-party rights.</p>
    </section>

    <section>
      <h2>10. Termination</h2>
      <p>We may terminate or suspend your account immediately if you:</p>
      <ul>
        <li>Violate these Terms of Service</li>
        <li>Fail to pay subscription fees</li>
        <li>Engage in fraudulent or illegal activities</li>
        <li>Pose a security risk to the platform</li>
      </ul>
      <p>Upon termination, your right to use the service ceases immediately. You may export your data within 30 days of termination.</p>
    </section>

    <section>
      <h2>11. Changes to Terms</h2>
      <p>We reserve the right to modify these terms at any time. Material changes will be communicated via email 30 days before taking effect. Continued use of the service after changes constitutes acceptance.</p>
    </section>

    <section>
      <h2>12. Governing Law</h2>
      <p>These terms are governed by the laws of the State of California, USA, without regard to conflict of law provisions. Any disputes shall be resolved in the courts of Santa Clara County, California.</p>
    </section>

    <section>
      <h2>13. Contact Information</h2>
      <p>For questions about these terms:</p>
      <ul>
        <li>Email: <a href="mailto:legal@flaer.io">legal@flaer.io</a></li>
        <li>Support: <a href="mailto:support@flaer.io">support@flaer.io</a></li>
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