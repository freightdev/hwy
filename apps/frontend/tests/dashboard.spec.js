import { test, expect } from '@playwright/test';

const SEED_EMAIL = 'jesse@conleylogistics.com';
const SEED_PASS = 'password123';

test.describe('Dashboard Access', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.evaluate(() => localStorage.clear());
  });

  test('redirects to login when not authenticated', async ({ page }) => {
    await page.goto('http://localhost:5173/app/dashboard');
    await page.waitForURL('**/login', { timeout: 10000 });
    await expect(page.locator('.login-card')).toBeVisible();
  });

  test('logs in and views dashboard', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.locator('#email').click();
    await page.keyboard.type(SEED_EMAIL);
    await page.locator('#password').click();
    await page.keyboard.type(SEED_PASS);
    await page.keyboard.press('Enter');
    await page.waitForURL('**/app/dashboard', { timeout: 10000 });
    await expect(page.locator('.page')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('.hwy-logo')).toContainText('HWY');
  });

  test('persists session across page reload', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.locator('#email').click();
    await page.keyboard.type(SEED_EMAIL);
    await page.locator('#password').click();
    await page.keyboard.type(SEED_PASS);
    await page.keyboard.press('Enter');
    await page.waitForURL('**/app/dashboard', { timeout: 10000 });

    await page.reload();
    await page.waitForURL('**/app/dashboard', { timeout: 15000 });
    await expect(page.locator('.page')).toBeVisible({ timeout: 5000 });
  });
});
