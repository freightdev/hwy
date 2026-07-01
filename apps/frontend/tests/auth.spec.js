import { test, expect } from '@playwright/test';

test.describe('Auth Flow', () => {

  test('landing page renders public mobile-first command center', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page.getByRole('heading', { name: /Run your trucking company from one mobile command center/i })).toBeVisible();
    await expect(page.getByLabel('Public navigation').getByRole('link', { name: /Sign in/i })).toBeVisible();
    await expect(page.getByLabel('Public navigation').getByRole('link', { name: /Create account/i })).toBeVisible();
  });

  test('login page renders correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await expect(page.locator('.login-card')).toBeVisible();
    await expect(page.locator('.login-logo')).toContainText('HWY');
    await expect(page.locator('h1')).toContainText('Welcome back');
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[id="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toContainText('Sign In');
    await expect(page.locator('.signup-link a')).toContainText('Create one');
  });

  test('shows error on invalid login', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.fill('input[type="email"]', 'wrong@email.com');
    await page.fill('input[id="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    await expect(page.locator('.toast--error')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('.login-card')).toBeVisible();
  });

  test('logs in with seeded user credentials', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.locator('#email').click();
    await page.keyboard.type('jesse@conleylogistics.com');
    await page.locator('#password').click();
    await page.keyboard.type('password123');
    await page.keyboard.press('Enter');
    await page.waitForURL('**/app/dashboard', { timeout: 10000 });
    await expect(page.locator('.page')).toBeVisible({ timeout: 5000 });
  });

  test('redirects to login when accessing dashboard without auth', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.evaluate(() => localStorage.clear());
    await page.goto('http://localhost:5173/app/dashboard');
    await page.waitForURL('**/login', { timeout: 10000 });
    await expect(page.locator('.login-card')).toBeVisible();
  });

  test('toggle password visibility', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    const passwordInput = page.locator('input[id="password"]');
    await expect(passwordInput).toHaveAttribute('type', 'password');
    await page.click('.pw-toggle');
    await expect(passwordInput).toHaveAttribute('type', 'text');
    await page.click('.pw-toggle');
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('requires email and password', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.click('button[type="submit"]');
    await expect(page.locator('.toast--error')).toBeVisible({ timeout: 5000 });
  });

  test('create account link opens signup page', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.click('.signup-link a');
    await page.waitForURL('**/signup', { timeout: 5000 });
    await expect(page.getByRole('heading', { name: /Create your HWY account/i })).toBeVisible();
  });

});
