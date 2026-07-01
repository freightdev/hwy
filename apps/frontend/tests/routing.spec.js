import { test, expect } from '@playwright/test';

const CADDY = 'http://localhost:8080';

test.describe('Caddy Internal Routing', () => {

  test('frontend serves HTML via Caddy for hwytms.com', async ({ request }) => {
    const resp = await request.get(CADDY, {
      headers: { Host: 'hwytms.com' },
    });
    expect(resp.status()).toBe(200);
    const text = await resp.text();
    expect(text).toContain('<!DOCTYPE html>');
    expect(text).toContain('HWY');
  });

  test('frontend serves HTML via Caddy for www.hwytms.com', async ({ request }) => {
    const resp = await request.get(CADDY, {
      headers: { Host: 'www.hwytms.com' },
    });
    expect(resp.status()).toBe(200);
    const text = await resp.text();
    expect(text).toContain('<!DOCTYPE html>');
  });

  test('backend API health via Caddy for api.hwytms.com', async ({ request }) => {
    const resp = await request.get(`${CADDY}/api/v1/health`, {
      headers: { Host: 'api.hwytms.com' },
    });
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.data.status).toBe('ok');
  });

  test('CoDriver health via Caddy for codriver.hwytms.com', async ({ request }) => {
    const resp = await request.get(`${CADDY}/health`, {
      headers: { Host: 'codriver.hwytms.com' },
    });
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.data.status).toBe('ok');
  });

  test('unmatched hostname returns non-200', async ({ request }) => {
    const resp = await request.get(CADDY, {
      headers: { Host: 'unknown.hwytms.com' },
    });
    expect(resp.status()).toBeGreaterThanOrEqual(400);
  });

});

test.describe('Login Flow via Caddy Proxy', () => {

  test('landing page renders via Caddy at hwytms.com', async ({ page }) => {
    await page.goto(CADDY, { waitUntil: 'networkidle' });
    await expect(page.locator('.landing')).toBeVisible({ timeout: 5000 });
  });

  test('login page renders via Caddy at hwytms.com', async ({ page, request }) => {
    const resp = await request.get(`${CADDY}/login`, {
      headers: { Host: 'hwytms.com' },
    });
    expect(resp.status()).toBe(200);
    const text = await resp.text();
    expect(text).toContain('Welcome back');
  });

});
