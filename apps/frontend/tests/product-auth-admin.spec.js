import { test, expect } from '@playwright/test';

test.describe('HWY public auth and admin UX', () => {
  test('landing page presents mobile-first command center content', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('http://localhost:5173/');
    await expect(page.getByRole('heading', { name: /Run your trucking company from one mobile command center/i })).toBeVisible();
    await expect(page.getByText(/Dispatch, compliance, payments, profiles, permissions, and CoDriver/i)).toBeVisible();
    await expect(page.getByLabel('Public navigation').getByRole('link', { name: /Create account/i })).toBeVisible();
  });

  test('signup page has accessible account creation fields', async ({ page }) => {
    await page.goto('http://localhost:5173/signup');
    await expect(page.getByRole('heading', { name: /Create your HWY account/i })).toBeVisible();
    await expect(page.getByLabel('Full name')).toBeVisible();
    await expect(page.getByLabel('Work email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByLabel('Role')).toBeVisible();
  });

  test('admin panel shows users and role permissions after login', async ({ page, request }) => {
    const login = await request.post('http://localhost:18000/api/v1/auth/login', {
      data: { email: 'jesse@conleylogistics.com', password: 'password123' }
    });
    expect(login.ok()).toBeTruthy();
    const body = await login.json();
    await page.goto('http://localhost:5173/login');
    await page.evaluate(({ token, user }) => {
      localStorage.setItem('hwy_token', token);
      localStorage.setItem('hwy_user', JSON.stringify(user));
      localStorage.setItem('hwy_onboarded', 'true');
    }, { token: body.data.access_token, user: body.data.user });
    await page.goto('http://localhost:5173/app/admin');
    await expect(page.getByRole('heading', { name: /Admin Command Center/i })).toBeVisible();
    await expect(page.getByText('Role permissions')).toBeVisible();
    await expect(page.getByText('Team access')).toBeVisible();
    await expect(page.getByLabel('Role summary').getByRole('heading', { name: 'Admin' })).toBeVisible();
  });
});
