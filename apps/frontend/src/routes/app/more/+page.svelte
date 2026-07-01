<script>
  import { goto } from '$app/navigation';
  import { user, company } from '$lib/stores/app.js';
  import { api, success, info } from '$lib/stores/toast.js';

  const quickActions = [
    { label: 'Add Driver', icon: '👤', action: () => goto('/app/connect/drivers') },
    { label: 'Add Dispatcher', icon: '📡', action: () => api('Add dispatcher requires team API') },
    { label: 'Post Load', icon: '📦', action: () => goto('/app/connect/loadboard') },
    { label: 'Send Message', icon: '💬', action: () => api('Messaging API required') },
  ];

  const menu = [
    { label: 'Logbook', icon: '📒', href: '/app/logbook', sub: 'Company profile, scores & authority' },
    { label: 'Documents', icon: '📄', href: '/app/more/documents', sub: 'Everything in one place' },
    { label: 'Payments & Invoices', icon: '💰', href: '/app/more/payments', sub: 'Billing and finance' },
    { label: 'Users & Team', icon: '👥', href: '/app/more/team', sub: 'Manage your team' },
    { label: 'Loads & Rates', icon: '🚛', href: null, action: () => goto('/app/connect/loadboard'), sub: 'Load management' },
    { label: 'Fuel & Cards', icon: '⛽', href: null, action: () => api('Fuel & card management'), sub: 'Fuel tracking' },
    { label: 'Reports & Analytics', icon: '📊', href: null, action: () => api('Reports require data API'), sub: 'Business insights' },
    { label: 'Compliance & Safety', icon: '⚠️', href: null, action: () => api('Compliance management API'), sub: 'DOT compliance' },
    { label: 'Integrations', icon: '🔌', href: '/app/more/integrations', sub: 'Connected services' },
    { label: 'AI & Agents', icon: '✦', href: '/app/ai', sub: 'Manage agents and automations' },
    { label: 'Company Settings', icon: '⚙️', href: '/app/more/settings', sub: 'Configure your account' },
  ];

  function navigate(item) {
    if (item.href) goto(item.href);
    else if (item.action) item.action();
  }
</script>

<div class="page">
  <div class="page-header">
    <div>
      <div style="font-size:20px;font-weight:800">HWY <span style="color:#3b82f6">TMS</span></div>
      <div style="font-size:11px;color:#4a5568">More</div>
    </div>
  </div>

  <!-- Quick actions -->
  <div class="section">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <span style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;letter-spacing:0.08em">Quick Actions</span>
      <button style="background:none;border:none;color:#3b82f6;font-size:12px;cursor:pointer" on:click={() => info('Customize quick actions')}>Edit</button>
    </div>
    <div class="quick-grid">
      {#each quickActions as qa}
        <button class="qa-btn" on:click={qa.action}>
          <span class="qa-icon">{qa.icon}</span>
          <span class="qa-label">{qa.label}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Menu -->
  <div class="section" style="padding-top:0">
    <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Menu</div>
    <div class="card" style="padding:0;overflow:hidden">
      {#each menu as item}
        <div class="menu-row" on:click={() => navigate(item)} role="button" tabindex="0">
          <div class="menu-icon">{item.icon}</div>
          <div style="flex:1">
            <div style="font-size:14px;font-weight:600">{item.label}</div>
            <div style="font-size:11px;color:#6b7280">{item.sub}</div>
          </div>
          <span style="color:#4a5568;font-size:18px">›</span>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .page-header { padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .quick-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:10px; }
  .qa-btn { background:#161a23;border:1px solid #1e2330;border-radius:12px;padding:14px 8px;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;transition:background 0.15s; }
  .qa-btn:hover { background:#1e2330; }
  .qa-icon { font-size:22px; }
  .qa-label { font-size:10px;color:#6b7280;font-weight:600;text-align:center; }
  .menu-row { display:flex;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid #1e2330;cursor:pointer;transition:background 0.1s; }
  .menu-row:hover { background:#161a23; }
  .menu-row:last-child { border-bottom:none; }
  .menu-icon { width:36px;height:36px;background:#1e2330;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
</style>
