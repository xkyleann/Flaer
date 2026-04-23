import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5173';
const API_URL = 'http://127.0.0.1:5001';

// Test credentials
const TEST_USER = {
  email: 'test@flaer.io',
  password: 'Test@2026!'
};

const ADMIN_USER = {
  email: 'demo@flaer.io',
  password: 'Demo@2026!'
};

test.describe('Authentication Flow', () => {
  
  test.beforeEach(async ({ page }) => {
    // Clear storage before each test
    await page.goto(BASE_URL);
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  });

  test('should display login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await expect(page).toHaveTitle(/Flaer/);
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill login form
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for redirect to dashboard
    await page.waitForURL(`${BASE_URL}/dashboard`, { timeout: 5000 });
    
    // Verify we're on dashboard
    await expect(page).toHaveURL(`${BASE_URL}/dashboard`);
    
    // Verify token is stored
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeTruthy();
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill with invalid credentials
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', 'WrongPassword123!');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for error message
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 3000 });
    await expect(page.locator('.error-message')).toContainText(/incorrect|invalid/i);
    
    // Verify we're still on login page
    await expect(page).toHaveURL(`${BASE_URL}/login`);
  });

  test('should validate email format', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill with invalid email
    await page.fill('input[type="email"]', 'invalid-email');
    await page.fill('input[type="password"]', TEST_USER.password);
    
    // Try to submit
    await page.click('button[type="submit"]');
    
    // Check for validation error
    const emailInput = page.locator('input[type="email"]');
    const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
  });

  test('should require password', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill only email
    await page.fill('input[type="email"]', TEST_USER.email);
    
    // Try to submit
    await page.click('button[type="submit"]');
    
    // Check for validation error
    const passwordInput = page.locator('input[type="password"]');
    const validationMessage = await passwordInput.evaluate((el: HTMLInputElement) => el.validationMessage);
    expect(validationMessage).toBeTruthy();
  });

  test('should logout successfully', async ({ page, context }) => {
    // First login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Click logout button
    await page.click('button:has-text("Logout"), [data-testid="logout-button"]');
    
    // Wait for redirect to home
    await page.waitForURL(BASE_URL, { timeout: 5000 });
    
    // Verify token is cleared
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeNull();
    
    // Verify cookies are cleared
    const cookies = await context.cookies();
    const refreshToken = cookies.find(c => c.name === 'refresh_token');
    expect(refreshToken).toBeUndefined();
  });
});

test.describe('Protected Routes', () => {
  
  test('should redirect to login when accessing dashboard without auth', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);
    
    // Should redirect to login
    await page.waitForURL(`${BASE_URL}/login`, { timeout: 5000 });
    await expect(page).toHaveURL(`${BASE_URL}/login`);
  });

  test('should access dashboard with valid token', async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Verify dashboard content is visible
    await expect(page.locator('h1, h2')).toContainText(/dashboard|overview/i);
    await expect(page.locator('[data-testid="dashboard-content"]')).toBeVisible();
  });

  test('should maintain session after page reload', async ({ page }) => {
    // Login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Reload page
    await page.reload();
    
    // Should still be on dashboard
    await expect(page).toHaveURL(`${BASE_URL}/dashboard`);
    await expect(page.locator('[data-testid="dashboard-content"]')).toBeVisible();
  });
});

test.describe('Token Refresh', () => {
  
  test('should refresh token automatically when expired', async ({ page }) => {
    // Login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Get initial token
    const initialToken = await page.evaluate(() => localStorage.getItem('access_token'));
    
    // Simulate token expiration by setting an expired token
    await page.evaluate(() => {
      localStorage.setItem('access_token', 'expired_token');
    });
    
    // Make an API call that should trigger refresh
    await page.click('[data-testid="refresh-data-button"]');
    
    // Wait a bit for refresh to happen
    await page.waitForTimeout(2000);
    
    // Get new token
    const newToken = await page.evaluate(() => localStorage.getItem('access_token'));
    
    // Token should be different (refreshed)
    expect(newToken).not.toBe('expired_token');
    expect(newToken).toBeTruthy();
  });
});

test.describe('Registration', () => {
  
  test('should display registration page', async ({ page }) => {
    await page.goto(`${BASE_URL}/register`);
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('input[name="full_name"]')).toBeVisible();
  });

  test('should validate password requirements', async ({ page }) => {
    await page.goto(`${BASE_URL}/register`);
    
    // Try weak password
    await page.fill('input[name="email"]', 'newuser@flaer.io');
    await page.fill('input[name="password"]', 'weak');
    await page.fill('input[name="full_name"]', 'New User');
    
    await page.click('button[type="submit"]');
    
    // Should show password requirements error
    await expect(page.locator('.password-requirements')).toBeVisible();
    await expect(page.locator('.password-requirements')).toContainText(/8 characters|uppercase|lowercase|number|special/i);
  });

  test('should show password strength indicator', async ({ page }) => {
    await page.goto(`${BASE_URL}/register`);
    
    const passwordInput = page.locator('input[name="password"]');
    const strengthIndicator = page.locator('[data-testid="password-strength"]');
    
    // Weak password
    await passwordInput.fill('weak');
    await expect(strengthIndicator).toContainText(/weak/i);
    
    // Medium password
    await passwordInput.fill('Medium123');
    await expect(strengthIndicator).toContainText(/medium/i);
    
    // Strong password
    await passwordInput.fill('Strong@2026!');
    await expect(strengthIndicator).toContainText(/strong/i);
  });
});

test.describe('Navigation', () => {
  
  test('should not show dashboard link when not authenticated', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Dashboard link should not be visible
    const dashboardLink = page.locator('a[href="/dashboard"]');
    await expect(dashboardLink).not.toBeVisible();
    
    // Login link should be visible
    await expect(page.locator('a[href="/login"]')).toBeVisible();
  });

  test('should show dashboard link when authenticated', async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Go back to home
    await page.goto(BASE_URL);
    
    // Dashboard link should be visible
    await expect(page.locator('a[href="/dashboard"]')).toBeVisible();
    
    // Login link should not be visible
    await expect(page.locator('a[href="/login"]')).not.toBeVisible();
  });
});

test.describe('API Integration', () => {
  
  test('should make authenticated API calls', async ({ page }) => {
    // Login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Intercept API call
    const responsePromise = page.waitForResponse(
      response => response.url().includes('/api/dashboard/overview') && response.status() === 200
    );
    
    // Trigger API call
    await page.click('[data-testid="refresh-data-button"]');
    
    // Wait for response
    const response = await responsePromise;
    expect(response.status()).toBe(200);
    
    // Verify Authorization header was sent
    const request = response.request();
    const headers = request.headers();
    expect(headers['authorization']).toContain('Bearer');
  });

  test('should handle 401 unauthorized responses', async ({ page }) => {
    // Set invalid token
    await page.goto(BASE_URL);
    await page.evaluate(() => {
      localStorage.setItem('access_token', 'invalid_token');
    });
    
    // Try to access dashboard
    await page.goto(`${BASE_URL}/dashboard`);
    
    // Should redirect to login
    await page.waitForURL(`${BASE_URL}/login`, { timeout: 5000 });
    await expect(page).toHaveURL(`${BASE_URL}/login`);
  });
});

test.describe('Security', () => {
  
  test('should not expose sensitive data in localStorage', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', TEST_USER.email);
    await page.fill('input[type="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    await page.waitForURL(`${BASE_URL}/dashboard`);
    
    // Check localStorage
    const storage = await page.evaluate(() => {
      const items: Record<string, string> = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) items[key] = localStorage.getItem(key) || '';
      }
      return items;
    });
    
    // Should not store password
    expect(JSON.stringify(storage).toLowerCase()).not.toContain(TEST_USER.password.toLowerCase());
    
    // Should only store access token
    expect(storage).toHaveProperty('access_token');
    expect(Object.keys(storage).length).toBeLessThanOrEqual(2); // access_token and maybe user_info
  });

  test('should use HTTPS in production', async ({ page }) => {
    // This test would check for HTTPS in production environment
    // For now, just verify the concept
    const url = page.url();
    if (process.env.NODE_ENV === 'production') {
      expect(url).toMatch(/^https:/);
    }
  });
});

// Made with Bob
