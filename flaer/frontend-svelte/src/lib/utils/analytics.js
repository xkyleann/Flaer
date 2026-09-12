// Simple analytics tracking utility
// In production, integrate with Google Analytics, Mixpanel, or similar

class Analytics {
  constructor() {
    this.enabled = true;
    this.events = [];
  }

  // Track page views
  trackPageView(page) {
    if (!this.enabled) return;
    
    const event = {
      type: 'pageview',
      page,
      timestamp: new Date().toISOString(),
      url: window.location.href
    };
    
    this.events.push(event);
    console.log('📊 Page View:', page);
    
    // In production, send to analytics service
    // Example: gtag('config', 'GA_MEASUREMENT_ID', { page_path: page });
  }

  // Track custom events
  trackEvent(category, action, label = null, value = null) {
    if (!this.enabled) return;
    
    const event = {
      type: 'event',
      category,
      action,
      label,
      value,
      timestamp: new Date().toISOString()
    };
    
    this.events.push(event);
    console.log('📊 Event:', { category, action, label, value });
    
    // In production, send to analytics service
    // Example: gtag('event', action, { event_category: category, event_label: label, value });
  }

  // Track button clicks
  trackButtonClick(buttonName, location) {
    this.trackEvent('Button', 'Click', `${buttonName} - ${location}`);
  }

  // Track form submissions
  trackFormSubmit(formName, success = true) {
    this.trackEvent('Form', success ? 'Submit Success' : 'Submit Error', formName);
  }

  // Track CTA interactions
  trackCTA(ctaName, action = 'click') {
    this.trackEvent('CTA', action, ctaName);
  }

  // Track user signup
  trackSignup(method = 'email') {
    this.trackEvent('User', 'Signup', method);
  }

  // Track user login
  trackLogin(method = 'email') {
    this.trackEvent('User', 'Login', method);
  }

  // Get all tracked events (for debugging)
  getEvents() {
    return this.events;
  }

  // Clear events
  clearEvents() {
    this.events = [];
  }

  // Enable/disable tracking
  setEnabled(enabled) {
    this.enabled = enabled;
  }
}

// Create singleton instance
const analytics = new Analytics();

export default analytics;

// Made with Bob
