<script>
  import { goto } from '$app/navigation';
  import { user, token as tokenStore, onboarded } from '$lib/stores/app.js';
  import { error as toastError } from '$lib/stores/toast.js';
  import { post, setToken } from '$lib/api.js';

  let email = '';
  let password = '';
  let showPassword = false;
  let loading = false;

  async function handleSubmit() {
    if (!email || !password) { toastError('Email and password required'); return; }
    loading = true;
    const { data, error: err } = await post('/auth/login', { email, password });
    loading = false;
    if (err) { toastError(err); return; }

    setToken(data.access_token);
    tokenStore.set(data.access_token);
    user.set(data.user);
    onboarded.set(true);
    console.log('[login] stored, navigating');
    goto('/app/dashboard');
  }
</script>

<div class="login-wrap">
  <div class="login-card">
    <div class="login-header">
      <div class="login-emblem">
        <div class="le-ring r1"></div>
        <div class="le-ring r2"></div>
        <div class="le-core">🛣️</div>
      </div>
      <div class="login-logo">HWY <span>TMS</span></div>
    </div>

    <h1 class="login-title">Welcome back</h1>
    <p class="login-sub">Sign in to your dispatch command center</p>

    <form id="login-form" on:submit|preventDefault={handleSubmit}>
      <div class="form-group">
        <label class="label" for="email">Email</label>
        <input id="email" type="email" bind:value={email} placeholder="you@company.com" disabled={loading} />
      </div>
      <div class="form-group">
        <label class="label" for="password">Password</label>
        <div class="password-wrap">
          <input id="password" type={showPassword ? 'text' : 'password'} value={password} on:input={e => password = e.target.value} placeholder="Enter your password" disabled={loading} />
          <button class="pw-toggle" type="button" on:click={() => showPassword = !showPassword} tabindex="-1" disabled={loading}>
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>
      </div>
      <button class="btn btn-primary btn-full" type="submit" disabled={loading}>
        {loading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>

    <p class="signup-link">
      Don't have an account? <a href="/signup">Create one</a>
    </p>
  </div>
</div>

<svelte:head>
<script>
  if (typeof window !== 'undefined') {
    const attachHwyLogin = () => {
      const form = document.getElementById('login-form');
      if (!form || form.dataset.vanillaLoginAttached) return;
      form.dataset.vanillaLoginAttached = 'true';
      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const emailValue = emailInput?.value || '';
        const passwordValue = passwordInput?.value || '';
        if (!emailValue || !passwordValue) return;
        const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
          ? (window.HWY_LOCAL_API_BASE_URL || 'http://localhost:18000/api/v1')
          : (window.HWY_PUBLIC_API_BASE_URL || 'https://api.hwytms.com/api/v1');
        const res = await fetch(`${apiBase}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: emailValue, password: passwordValue })
        });
        const json = await res.json();
        if (!res.ok || !json.data?.access_token) {
          let toast = document.querySelector('.toast--error');
          if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast toast--error';
            toast.textContent = json.detail || json.error || 'Invalid email or password';
            document.body.appendChild(toast);
          }
          return;
        }
        localStorage.setItem('hwy_token', json.data.access_token);
        localStorage.setItem('hwy_user', JSON.stringify(json.data.user));
        localStorage.setItem('hwy_onboarded', 'true');
        window.location.href = '/app/dashboard';
      }, { capture: true });
    };
    window.addEventListener('DOMContentLoaded', attachHwyLogin);
    setTimeout(attachHwyLogin, 0);
  }
</script>
</svelte:head>

<style>
  .login-wrap {
    min-height: 100vh;
    background: #0d0f14;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }
  .login-card {
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 16px;
    padding: 40px 28px;
    width: 100%;
    max-width: 400px;
    animation: fadeIn 0.4s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  .login-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 28px;
  }
  .login-emblem {
    position: relative;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
  }
  .le-ring {
    position: absolute;
    border-radius: 50%;
    border: 1.5px solid #3b82f6;
    animation: pulse-ring 2s ease-out infinite;
  }
  .r1 { width: 80px; height: 80px; opacity: 0.15; animation-delay: 0s; }
  .r2 { width: 60px; height: 60px; opacity: 0.3; animation-delay: 0.5s; }
  @keyframes pulse-ring {
    0%   { transform: scale(0.9); opacity: 0; }
    50%  { opacity: 0.4; }
    100% { transform: scale(1.1); opacity: 0; }
  }
  .le-core {
    width: 42px; height: 42px;
    background: radial-gradient(circle at 35% 35%, #2563eb, #0d0f14);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 24px rgba(59,130,246,0.5);
    z-index: 2;
  }
  .login-logo {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.03em;
  }
  .login-logo span { color: #3b82f6; }

  .login-title {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 6px;
  }
  .login-sub {
    font-size: 13px;
    color: #6b7280;
    text-align: center;
    margin-bottom: 28px;
  }

  .password-wrap {
    position: relative;
  }
  .password-wrap input {
    padding-right: 44px;
  }
  .pw-toggle {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    background: none;
    border: none;
    color: #6b7280;
    font-size: 18px;
    padding: 0 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  .pw-toggle:hover { color: #e2e8f0; }

  .signup-link {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: #6b7280;
  }
  .signup-link a {
    color: #3b82f6;
    font-weight: 600;
  }
  .signup-link a:hover { text-decoration: underline; }

  .form-group { margin-bottom: 16px; }
</style>
