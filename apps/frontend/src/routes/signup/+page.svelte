<script>
  import { goto } from '$app/navigation';
  import { setToken } from '$lib/api.js';
  import { user, token as tokenStore, onboarded } from '$lib/stores/app.js';
  import { error as toastError } from '$lib/stores/toast.js';
  import { post } from '$lib/api.js';

  let form = { name: '', email: '', phone: '', password: '', role: 'Owner' };
  let loading = false;
  let showPassword = false;

  const roles = ['Owner', 'Dispatcher', 'Driver', 'Accounting', 'Viewer'];

  async function submit() {
    if (!form.name || !form.email || !form.password) {
      toastError('Name, email, and password required');
      return;
    }
    loading = true;
    const { data, error: err } = await post('/auth/register', form);
    loading = false;
    if (err) {
      toastError(err);
      return;
    }
    setToken(data.access_token);
    tokenStore.set(data.access_token);
    user.set(data.user);
    onboarded.set(Boolean(data.user?.company_id));
    goto(data.user?.company_id ? '/app/dashboard' : '/onboarding');
  }
</script>

<svelte:head><title>Create account | HWY TMS</title></svelte:head>

<div class="auth-shell">
  <section class="panel story-panel">
    <a class="brand" href="/" aria-label="HWY home"><span>HWY</span> TMS</a>
    <div class="eyebrow">Mobile-first trucking OS</div>
    <h1>Create your HWY account</h1>
    <p>Start with a secure user profile, then invite the people who dispatch, drive, bill, manage compliance, and run CoDriver with you.</p>
    <div class="trust-grid">
      <div><strong>Roles</strong><span>Owner, dispatcher, driver, accounting, viewer</span></div>
      <div><strong>Permissions</strong><span>Admin-controlled access from day one</span></div>
      <div><strong>Mobile</strong><span>Designed for the cab first, desktop friendly</span></div>
    </div>
  </section>

  <section class="panel form-panel" aria-label="Signup form">
    <div class="form-head">
      <div class="icon">🛣️</div>
      <div><h2>Set up your login</h2><p>No credit card. No fake data.</p></div>
    </div>

    <form on:submit|preventDefault={submit}>
      <label for="name">Full name</label>
      <input id="name" autocomplete="name" bind:value={form.name} placeholder="Jesse Conley" disabled={loading} />

      <label for="email">Work email</label>
      <input id="email" type="email" autocomplete="email" bind:value={form.email} placeholder="you@company.com" disabled={loading} />

      <label for="phone">Phone</label>
      <input id="phone" type="tel" autocomplete="tel" bind:value={form.phone} placeholder="(555) 000-0000" disabled={loading} />

      <label for="role">Role</label>
      <select id="role" bind:value={form.role} disabled={loading}>
        {#each roles as role}<option>{role}</option>{/each}
      </select>

      <label for="password">Password</label>
      <div class="password-row">
        <input id="password" type={showPassword ? 'text' : 'password'} autocomplete="new-password" value={form.password} on:input={(event) => form.password = event.currentTarget.value} placeholder="At least 8 characters" disabled={loading} />
        <button type="button" on:click={() => showPassword = !showPassword} disabled={loading}>{showPassword ? 'Hide' : 'Show'}</button>
      </div>

      <button class="primary" type="submit" disabled={loading}>{loading ? 'Creating account…' : 'Create account'}</button>
    </form>

    <p class="switch">Already have an account? <a href="/login">Sign in</a></p>
  </section>
</div>

<style>
  .auth-shell{min-height:100vh;background:radial-gradient(circle at 20% 0%,rgba(59,130,246,.22),transparent 32%),#080b12;color:#eef4ff;padding:18px;display:grid;gap:14px;align-items:stretch}
  .panel{border:1px solid rgba(148,163,184,.18);background:rgba(15,23,42,.82);border-radius:28px;box-shadow:0 24px 80px rgba(0,0,0,.35);backdrop-filter:blur(18px)}
  .story-panel{padding:28px;display:flex;flex-direction:column;justify-content:space-between;min-height:330px;overflow:hidden;position:relative}.story-panel:after{content:"";position:absolute;right:-80px;bottom:-80px;width:220px;height:220px;border:1px solid rgba(59,130,246,.25);border-radius:50%;box-shadow:0 0 80px rgba(59,130,246,.18)}
  .brand{color:#eaf2ff;font-weight:900;font-size:22px;letter-spacing:-.04em}.brand span{color:#60a5fa}.eyebrow{color:#93c5fd;font-size:12px;text-transform:uppercase;letter-spacing:.12em;font-weight:800;margin-top:40px}.story-panel h1{font-size:clamp(34px,10vw,62px);line-height:.96;letter-spacing:-.06em;margin:14px 0}.story-panel p{color:#a8b3c7;line-height:1.65;margin:0;max-width:650px}
  .trust-grid{display:grid;gap:10px;margin-top:28px}.trust-grid div{padding:14px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}.trust-grid strong{display:block}.trust-grid span{display:block;color:#94a3b8;font-size:13px;margin-top:4px}
  .form-panel{padding:22px}.form-head{display:flex;gap:14px;align-items:center;margin-bottom:22px}.icon{width:52px;height:52px;border-radius:18px;background:linear-gradient(135deg,#2563eb,#0f172a);display:grid;place-items:center;box-shadow:0 0 35px rgba(37,99,235,.35)}.form-head h2{margin:0;font-size:23px}.form-head p{margin:4px 0 0;color:#94a3b8;font-size:13px}
  form{display:grid;gap:10px}label{font-size:12px;color:#cbd5e1;font-weight:800;margin-top:5px}input,select{width:100%;box-sizing:border-box;background:#0b1220;border:1px solid #243041;color:#f8fafc;border-radius:14px;padding:14px 13px;font-size:16px;outline:none}input:focus,select:focus{border-color:#60a5fa;box-shadow:0 0 0 3px rgba(96,165,250,.14)}.password-row{display:grid;grid-template-columns:1fr auto;gap:8px}.password-row button{border:1px solid #243041;background:#111827;color:#cbd5e1;border-radius:14px;padding:0 14px}.primary{margin-top:12px;border:0;border-radius:16px;padding:15px 18px;background:linear-gradient(135deg,#2563eb,#06b6d4);color:white;font-weight:900;font-size:15px;box-shadow:0 14px 34px rgba(37,99,235,.32)}.primary:disabled{opacity:.55}.switch{text-align:center;color:#94a3b8}.switch a{color:#93c5fd;font-weight:800}
  @media(min-width:860px){.auth-shell{grid-template-columns:minmax(0,1.1fr) 460px;padding:26px}.story-panel{padding:46px}.form-panel{padding:34px;align-self:center}.trust-grid{grid-template-columns:repeat(3,1fr)}}
</style>
