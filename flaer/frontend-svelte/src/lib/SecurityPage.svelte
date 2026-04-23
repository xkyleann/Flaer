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
    <h1>Security</h1>
    <p class="legal-updated">Last updated: April 20, 2026</p>
    
    <section>
      <h2>1. Security Infrastructure</h2>
      <p>Flaer employs enterprise-grade security measures to protect your data:</p>
      <ul>
        <li><strong>Encryption:</strong> AES-256 encryption for data at rest, TLS 1.3 for data in transit</li>
        <li><strong>Authentication:</strong> Multi-factor authentication (MFA) with TOTP and SMS options</li>
        <li><strong>Access Control:</strong> Role-based access control (RBAC) with principle of least privilege</li>
        <li><strong>Network Security:</strong> Web Application Firewall (WAF), DDoS protection, and intrusion detection</li>
        <li><strong>Infrastructure:</strong> Hosted on AWS with isolated VPCs and private subnets</li>
      </ul>
    </section>

    <section>
      <h2>2. Compliance Certifications</h2>
      <p>Flaer maintains the following security certifications:</p>
      <ul>
        <li><strong>SOC 2 Type II:</strong> Annual audits by independent third parties</li>
        <li><strong>ISO 27001:</strong> Information security management system certification</li>
        <li><strong>GDPR Compliant:</strong> Full compliance with EU data protection regulations</li>
        <li><strong>CCPA Compliant:</strong> California Consumer Privacy Act compliance</li>
        <li><strong>HIPAA Ready:</strong> Healthcare data protection standards (Enterprise tier)</li>
      </ul>
    </section>

    <section>
      <h2>3. Data Protection</h2>
      <p>Your data is protected through multiple layers:</p>
      <ul>
        <li><strong>Encryption Keys:</strong> Customer-managed encryption keys (CMEK) available for Enterprise clients</li>
        <li><strong>Data Residency:</strong> Choose where your data is stored (US, EU, APAC regions)</li>
        <li><strong>Backup & Recovery:</strong> Automated daily backups with 30-day retention, 4-hour RPO</li>
        <li><strong>Data Isolation:</strong> Logical separation between customer environments</li>
        <li><strong>Secure Deletion:</strong> Cryptographic erasure upon account termination</li>
      </ul>
    </section>

    <section>
      <h2>4. Application Security</h2>
      <p>Our platform is built with security-first principles:</p>
      <ul>
        <li><strong>Secure Development:</strong> OWASP Top 10 compliance, secure coding practices</li>
        <li><strong>Code Reviews:</strong> Mandatory peer reviews and automated security scanning</li>
        <li><strong>Dependency Management:</strong> Automated vulnerability scanning of third-party libraries</li>
        <li><strong>API Security:</strong> Rate limiting, OAuth 2.0, API key rotation</li>
        <li><strong>Session Management:</strong> Secure cookies, automatic timeout, token refresh</li>
      </ul>
    </section>

    <section>
      <h2>5. Monitoring & Incident Response</h2>
      <p>24/7 security monitoring and rapid incident response:</p>
      <ul>
        <li><strong>Security Operations Center:</strong> 24/7 monitoring by dedicated security team</li>
        <li><strong>Threat Detection:</strong> Real-time anomaly detection and automated alerts</li>
        <li><strong>Incident Response:</strong> Documented procedures with 1-hour response time for critical issues</li>
        <li><strong>Audit Logging:</strong> Comprehensive logs retained for 1 year, immutable storage</li>
        <li><strong>Penetration Testing:</strong> Quarterly tests by independent security firms</li>
      </ul>
    </section>

    <section>
      <h2>6. Employee Security</h2>
      <p>Our team follows strict security protocols:</p>
      <ul>
        <li><strong>Background Checks:</strong> All employees undergo comprehensive background verification</li>
        <li><strong>Security Training:</strong> Mandatory annual security awareness training</li>
        <li><strong>Access Management:</strong> Just-in-time access with automatic expiration</li>
        <li><strong>Device Security:</strong> Encrypted laptops, MDM, and remote wipe capabilities</li>
        <li><strong>Confidentiality:</strong> All employees sign NDAs and security agreements</li>
      </ul>
    </section>

    <section>
      <h2>7. Vulnerability Management</h2>
      <p>Proactive identification and remediation of security issues:</p>
      <ul>
        <li><strong>Vulnerability Scanning:</strong> Automated daily scans of infrastructure and applications</li>
        <li><strong>Patch Management:</strong> Critical patches applied within 24 hours, regular patches within 7 days</li>
        <li><strong>Bug Bounty Program:</strong> Rewards for responsible disclosure of security vulnerabilities</li>
        <li><strong>Security Updates:</strong> Transparent communication of security incidents and fixes</li>
      </ul>
    </section>

    <section>
      <h2>8. Third-Party Security</h2>
      <p>We carefully vet all service providers:</p>
      <ul>
        <li><strong>Vendor Assessment:</strong> Security questionnaires and compliance verification</li>
        <li><strong>Data Processing Agreements:</strong> Contractual security and privacy obligations</li>
        <li><strong>Limited Access:</strong> Third parties only access data necessary for their service</li>
        <li><strong>Regular Audits:</strong> Periodic reviews of third-party security practices</li>
      </ul>
    </section>

    <section>
      <h2>9. Disaster Recovery</h2>
      <p>Business continuity and disaster recovery planning:</p>
      <ul>
        <li><strong>High Availability:</strong> Multi-region deployment with automatic failover</li>
        <li><strong>Backup Strategy:</strong> Geographically distributed backups with encryption</li>
        <li><strong>Recovery Time:</strong> RTO of 4 hours, RPO of 1 hour for critical data</li>
        <li><strong>Testing:</strong> Quarterly disaster recovery drills and documentation updates</li>
      </ul>
    </section>

    <section>
      <h2>10. Responsible Disclosure</h2>
      <p>We welcome security researchers to report vulnerabilities:</p>
      <ul>
        <li><strong>Report Email:</strong> <a href="mailto:security@flaer.io">security@flaer.io</a></li>
        <li><strong>PGP Key:</strong> Available at <a href="https://flaer.io/.well-known/security.txt">security.txt</a></li>
        <li><strong>Response Time:</strong> Initial response within 24 hours</li>
        <li><strong>Rewards:</strong> Bug bounty rewards up to $10,000 for critical vulnerabilities</li>
        <li><strong>Safe Harbor:</strong> We will not pursue legal action against good-faith security research</li>
      </ul>
    </section>

    <section>
      <h2>11. User Security Best Practices</h2>
      <p>Help us keep your account secure:</p>
      <ul>
        <li>Enable multi-factor authentication (MFA)</li>
        <li>Use strong, unique passwords (minimum 12 characters)</li>
        <li>Regularly review account activity and access logs</li>
        <li>Keep your contact information up to date</li>
        <li>Report suspicious activity immediately</li>
        <li>Don't share credentials or API keys</li>
        <li>Use API keys with minimal required permissions</li>
      </ul>
    </section>

    <section>
      <h2>12. Contact Security Team</h2>
      <p>For security concerns or questions:</p>
      <ul>
        <li>Security Issues: <a href="mailto:security@flaer.io">security@flaer.io</a></li>
        <li>Privacy Questions: <a href="mailto:privacy@flaer.io">privacy@flaer.io</a></li>
        <li>General Support: <a href="mailto:support@flaer.io">support@flaer.io</a></li>
        <li>Emergency Hotline: +1 (800) FLAER-911 (24/7)</li>
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