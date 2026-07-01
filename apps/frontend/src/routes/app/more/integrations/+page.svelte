<script>
  import { goto } from '$app/navigation';
  import { api, success } from '$lib/stores/toast.js';

  let activeTab = 'all';

  const connected = [
    { name: 'FMCSA', sub: 'Authority & Compliance', status: 'Connected', icon: '⚖️', color: '#3b82f6' },
    { name: 'Payments', sub: 'Payments', status: 'Connected', icon: '💳', color: '#22c55e' },
    { name: 'TriumphPay', sub: 'Factoring', status: 'Connected', icon: '💰', color: '#22c55e' },
    { name: 'Fuel Cloud', sub: 'Fuel & Cards', status: 'Connected', icon: '⛽', color: '#22c55e' },
    { name: 'Google Maps', sub: 'Maps & Routing', status: 'Connected', icon: '🗺️', color: '#22c55e' },
  ];

  const available = [
    { name: 'EFS Fuel Card', sub: 'Fuel & Cards', icon: '⛽', category: 'fuel' },
    { name: 'IFTA.org', sub: 'Tax Reporting', icon: '📋', category: 'compliance' },
    { name: 'DAT Power', sub: 'Load Board', icon: '📦', category: 'loads', rating: 4.8 },
    { name: 'Truckstop', sub: 'Load Board', icon: '🚛', category: 'loads', rating: 4.6 },
    { name: 'EFS Fuel Card', sub: 'Fuel & Cards', icon: '⛽', category: 'fuel', rating: 4.6 },
    { name: 'QuickBooks', sub: 'Accounting', icon: '📊', category: 'finance', rating: 4.7 },
    { name: 'Samsara', sub: 'ELD & GPS', icon: '📍', category: 'tracking', rating: 4.5 },
    { name: 'KeepTruckin', sub: 'ELD & Compliance', icon: '📱', category: 'tracking', rating: 4.4 },
    { name: 'Stripe', sub: 'Payment Processing', icon: '💳', category: 'finance', rating: 4.9 },
    { name: 'Amazon Freight', sub: 'Load Board', icon: '📦', category: 'loads', rating: 4.3 },
  ];

  const categories = [
    ['all', 'All'],
    ['loads', 'Load Boards'],
    ['fuel', 'Fuel & Cards'],
    ['compliance', 'Compliance'],
    ['finance', 'Analytics'],
  ];

  $: filtered = available.filter(a => activeTab === 'all' || a.category === activeTab);

  function connect(item) { api(`${item.name} integration requires OAuth setup and API key`); }
  function disconnect(item) { api(`Disconnect ${item.name} requires confirmation via API`); }
  function manage(item) { api(`${item.name} management panel`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/more')}>‹</button>
    <div class="page-title">Integrations</div>
    <button class="icon-btn-sm" on:click={() => api('Browse all integrations')}>⊞</button>
  </div>

  <!-- Connected -->
  <div class="section">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;letter-spacing:0.08em">Connected ({connected.length})</div>
      <button style="background:none;border:none;color:#3b82f6;font-size:12px;cursor:pointer" on:click={() => api('Edit integrations')}>Edit</button>
    </div>
    <div class="card" style="padding:0;overflow:hidden;margin-bottom:20px">
      {#each connected as item}
        <div class="list-item">
          <div class="int-icon" style="background:{item.color}22;color:{item.color}">{item.icon}</div>
          <div style="flex:1">
            <div style="font-size:13px;font-weight:600">{item.name}</div>
            <div style="font-size:11px;color:#6b7280">{item.sub}</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span class="chip chip-green" style="font-size:10px">● {item.status}</span>
            <button class="btn btn-secondary btn-sm" on:click={() => manage(item)}>Manage</button>
          </div>
        </div>
      {/each}
    </div>

    <!-- Marketplace / Available -->
    <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Available Integrations</div>

    <div style="display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;margin-bottom:14px">
      {#each categories as [k, label]}
        <button class="cat-btn" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
      {/each}
    </div>

    <!-- Featured -->
    <div style="font-size:11px;color:#4a5568;font-weight:700;margin-bottom:10px">FEATURED</div>
    <div class="featured-grid">
      {#each filtered.slice(0,3) as item}
        <div class="featured-card card">
          <div class="feat-icon">{item.icon}</div>
          <div style="font-size:13px;font-weight:700;margin-top:8px">{item.name}</div>
          <div style="font-size:11px;color:#6b7280;margin-bottom:8px">{item.sub}</div>
          {#if item.rating}<div style="font-size:11px;color:#f59e0b;margin-bottom:8px">{item.rating}★</div>{/if}
          <button class="btn btn-primary btn-sm btn-full" on:click={() => connect(item)}>Connect</button>
        </div>
      {/each}
    </div>

    <!-- Top Categories -->
    <div style="font-size:11px;color:#4a5568;font-weight:700;margin-top:20px;margin-bottom:10px">ALL AVAILABLE</div>
    <div class="card" style="padding:0;overflow:hidden">
      {#each filtered as item}
        <div class="list-item">
          <div class="int-icon" style="background:#1e2330;color:#6b7280">{item.icon}</div>
          <div style="flex:1">
            <div style="font-size:13px;font-weight:600">{item.name}</div>
            <div style="font-size:11px;color:#6b7280">{item.sub}{item.rating ? ` • ${item.rating}★` : ''}</div>
          </div>
          <button class="btn btn-secondary btn-sm" on:click={() => connect(item)}>Connect</button>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .icon-btn-sm { background:#161a23;border:1px solid #1e2330;border-radius:7px;padding:6px 9px;font-size:13px;cursor:pointer;margin-left:auto; }
  .int-icon { width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
  .cat-btn { padding:5px 14px;border-radius:20px;border:1px solid #1e2330;background:#161a23;color:#6b7280;font-size:12px;cursor:pointer;white-space:nowrap; }
  .cat-btn.active { background:#0f1e2b;border-color:#3b82f6;color:#3b82f6; }
  .featured-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:8px; }
  .featured-card { text-align:center;padding:16px 10px; }
  .feat-icon { font-size:28px; }
</style>
