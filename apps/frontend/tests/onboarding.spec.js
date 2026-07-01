import { test, expect } from '@playwright/test';

test.describe('Onboarding Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.evaluate(() => localStorage.clear());
  });

  test('shows onboarding page when navigated to directly', async ({ page }) => {
    await page.goto('http://localhost:5173/onboarding');
    await expect(page.locator('.onboarding')).toBeVisible({ timeout: 5000 });
  });

  test('completes step 0 welcome and shows role selection', async ({ page }) => {
    await page.goto('http://localhost:5173/onboarding');
    await page.waitForTimeout(500);
    const btn = page.locator('button', { hasText: 'Get Started' });
    await expect(btn).toBeVisible({ timeout: 5000 });
    await btn.click({ force: true });
    await page.waitForTimeout(500);
    await expect(page.locator('.step-hdr')).toBeVisible({ timeout: 5000 });
    const roleCard = page.locator('.role-card').first();
    await expect(roleCard).toBeVisible({ timeout: 5000 });
  });

  test('shows validation error when password is missing', async ({ page }) => {
    await page.goto('http://localhost:5173/onboarding');
    await page.waitForTimeout(500);
    await page.locator('button', { hasText: 'Get Started' }).click({ force: true });
    await page.waitForTimeout(300);

    // Click the first role card (Dispatching Company)
    await page.locator('.role-card').first().click({ force: true });
    await page.waitForTimeout(300);

    // Fill step 2 but leave password empty
    await page.fill('input[placeholder="Jesse"]', 'Test');
    await page.fill('input[placeholder="jesse@company.com"]', 'test@hwy.com');
    await page.locator('button', { hasText: 'Continue' }).click();
    await expect(page.locator('.toast--error')).toBeVisible({ timeout: 5000 });
  });
});
