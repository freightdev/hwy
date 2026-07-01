<script>
  import { onMount } from 'svelte';
  import { company, user } from '$lib/stores/app.js';
  import { success, api, info, error as toastError } from '$lib/stores/toast.js';
  import { goto } from '$app/navigation';
  import { get } from '$lib/api.js';

  let drivers = [];
  let loads = [];
  let loading = true;

  onMount(async () => {
    const [drvRes, ldRes] = await Promise.all([get('/drivers'), get('/loads')]);
    if (drvRes.error) toastError(drvRes.error);
    else drivers = drvRes.data;
    if (ldRes.error) toastError(ldRes.error);
    else loads = ldRes.data;
    loading = false;
  });

  $: name = $user.name ? $user.name.split(' ')[0] : 'there';
  $: greeting = (() => {
    const h = new Date().getHours();
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
  })();

  const quickActions = [
    { label: 'Add Driver', icon: '👤', action: () => goto('/app/connect/drivers') },
    { label: 'Post Load', icon: '📦', action: () => goto('/app/connect/loadboard') },
    { label: 'CoDriver', icon: '✦', action: () => goto('/app/ai') },
    { label: 'Logbook', icon: '📒', action: () => goto('/app/logbook') },
  ];

  $: activeDrivers = drivers.filter(d => d.status !== 'Off Duty').length;
  $: activeLoads = loads.length;
  $: inTransit = drivers.filter(d => d.status === 'In Transit');
  $: available = drivers.filter(d => d.status === 'Available');
  $: atPickup = drivers.filter(d => d.status === 'At Pickup');

  const allStatuses = ['All', 'In Transit', 'At Pickup', 'At Delivery'];
  let activeStatusFilter = 'All';

  $: filteredDrivers = activeStatusFilter === 'All'
    ? drivers.filter(d => d.status !== 'Off Duty')
    : drivers.filter(d => d.status === activeStatusFilter);

  const topLoads = [
    { route: 'Dallas, TX → Houston, TX', date: 'Today', rate: '$2,100', equipment: '53\' Dry Van', broker: 'Landstar' },
    { route: 'Atlanta, GA → Tampa, FL', date: 'Today', rate: '$2,450', equipment: '48\' Flatbed', broker: 'TQL' },
    { route: 'Chicago, IL → Nashville, TN', date: 'Today', rate: '$1,950', equipment: 'Dry Van', broker: 'DAT' },
  ];

  function viewAll() { goto('/app/connect'); }
  function viewLoadBoard() { goto('/app/connect/loadboard'); }
  function contactDriver(name) { api(`Direct message to ${name}`); }
  function callDriver(name) { api(`VoIP call to ${name}`); }
  function statusColor(s) {
    if (s === 'In Transit') return '#3b82f6';
    if (s === 'Available') return '#22c55e';
    if (s === 'At Pickup') return '#f59e0b';
    if (s === 'At Delivery') return '#8b5cf6';
    if (s === 'Off Duty') return '#6b7280';
    return '#4a5568';
  }
</script>

<div class="page">
  <div class="top-bar">
    <div>
      <div class="hwy-logo">HWY <span>TMS</span></div>
      <div class="company-name">{$company.name || 'Your Company'}</div>
    </div>
    <div class="top-actions">
      <button class="icon-btn" on:click={() => api('Push notifications')}>🔔</button>
      <button class="icon-btn" on:click={() => api('Direct messages')}>💬</button>
    </div>
  </div>

  <div class="section">
    <h2 class="greeting">{greeting}, {name}! 👋</h2>
    <p class="greeting-sub">Here's what's happening with your operation today.</p>
  </div>

  <div class="section" style="padding-top: 0">
    <div class="stats-label">TODAY'S OVERVIEW</div>
    <div class="stats-grid">
      <div class="stat-box">
        <div class="stat-val">{loading ? '...' : activeDrivers || '0'}</div>
        <div class="stat-lbl">Drivers<br>Active</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">{loading ? '...' : activeLoads || '0'}</div>
        <div class="stat-lbl">Loads<br>In System</div>
      </div>
      <div class="stat-box">
        <div class="stat-val revenue">$241,550</div>
        <div class="stat-lbl">Revenue<br><span class="up">↑ 15.8%</span></div>
      </div>
      <div class="stat-box">
        <div class="stat-val danger">8.7%</div>
        <div class="stat-lbl">Deadhead<br><span class="down">↓ 13%</span></div>
      </div>
    </div>
  </div>

  <div class="section" style="padding-top:0">
    <div class="quick-actions">
      {#each quickActions as qa}
        <button class="qa-btn" on:click={qa.action}>
          <span class="qa-icon">{qa.icon}</span>
          <span class="qa-label">{qa.label}</span>
        </button>
      {/each}
    </div>
  </div>

  <div class="section" style="padding-top:0">
    <div class="section-header">
      <span class="section-title">Today's Live Operations</span>
      <button class="link-btn" on:click={viewAll}>View All</button>
    </div>

    <div class="status-tabs">
      {#each allStatuses as tab}
        <button
          class="status-tab"
          class:active={activeStatusFilter === tab}
          on:click={() => activeStatusFilter = tab}
        >{tab} ({tab === 'All' ? activeDrivers : drivers.filter(d => d.status === tab).length})</button>
      {/each}
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      {#if loading}
        <div class="empty-state"><p>Loading operations...</p></div>
      {:else if filteredDrivers.length === 0}
        <div class="empty-state"><div class="icon">🚛</div><p>No active drivers</p></div>
      {:else}
        {#each filteredDrivers as op}
          <div class="list-item">
            <div class="avatar" style="background: {statusColor(op.status)}22; color: {statusColor(op.status)}">
              {op.name.split(' ').map(w=>w[0]).join('')}
            </div>
            <div style="flex:1; min-width:0">
              <div class="op-name">{op.name} <span class="chip chip-sm" style="background:{statusColor(op.status)}22;color:{statusColor(op.status)}">{op.status}</span></div>
              <div class="op-sub">Truck {op.truck} • {op.load_id || 'No load'}</div>
              <div class="op-route">{op.route || 'No route assigned'}</div>
            </div>
            <div style="display:flex;gap:6px">
              <button class="icon-sm" on:click={() => callDriver(op.name)}>📞</button>
              <button class="icon-sm" on:click={() => contactDriver(op.name)}>💬</button>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>

  <div class="section" style="padding-top:0">
    <div class="section-header">
      <span class="section-title">Load Board (Top Matches)</span>
      <button class="link-btn" on:click={viewLoadBoard}>View Full Board</button>
    </div>
    <div class="card" style="padding:0;overflow:hidden">
      {#each topLoads as load}
        <div class="list-item">
          <div style="flex:1;min-width:0">
            <div class="op-name">{load.route}</div>
            <div class="op-sub">{load.date} • {load.equipment} • {load.broker}</div>
          </div>
          <div>
            <div class="rate">{load.rate}</div>
            <button class="btn btn-primary btn-sm" style="margin-top:4px" on:click={() => api('Load booking')}>Book</button>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid #1e2330;
    position: sticky;
    top: 0;
    background: #0d0f14;
    z-index: 50;
  }
  .hwy-logo { font-size: 20px; font-weight: 800; letter-spacing: -0.02em; }
  .hwy-logo span { color: #3b82f6; }
  .company-name { font-size: 11px; color: #4a5568; }
  .top-actions { display: flex; gap: 8px; }
  .icon-btn {
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 16px;
    cursor: pointer;
  }

  .greeting { font-size: 18px; font-weight: 700; margin-bottom: 4px; }
  .greeting-sub { font-size: 13px; color: #6b7280; }

  .stats-label { font-size: 10px; color: #4a5568; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px; }
  .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .stat-box { background: #161a23; border: 1px solid #1e2330; border-radius: 12px; padding: 10px 8px; text-align: center; }
  .stat-val { font-size: 18px; font-weight: 700; }
  .stat-lbl { font-size: 9px; color: #4a5568; margin-top: 2px; line-height: 1.4; text-transform: uppercase; }
  .revenue { color: #22c55e; }
  .danger { color: #ef4444; }
  .up { color: #22c55e; }
  .down { color: #22c55e; }

  .quick-actions { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .qa-btn {
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 12px;
    padding: 14px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: background 0.15s;
  }
  .qa-btn:hover { background: #1e2330; }
  .qa-icon { font-size: 22px; }
  .qa-label { font-size: 10px; color: #6b7280; font-weight: 600; }

  .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
  .section-title { font-size: 13px; font-weight: 700; color: #e2e8f0; }
  .link-btn { background: none; border: none; color: #3b82f6; font-size: 12px; cursor: pointer; }

  .status-tabs { display: flex; gap: 6px; margin-bottom: 10px; overflow-x: auto; padding-bottom: 2px; }
  .status-tab {
    padding: 5px 12px;
    border-radius: 20px;
    border: 1px solid #1e2330;
    background: #161a23;
    color: #6b7280;
    font-size: 11px;
    white-space: nowrap;
    cursor: pointer;
  }
  .status-tab.active { background: #0f1e2b; border-color: #3b82f6; color: #3b82f6; }

  .op-name { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .chip-sm { padding: 2px 7px; border-radius: 20px; font-size: 10px; font-weight: 600; }
  .op-sub { font-size: 11px; color: #6b7280; margin-top: 2px; }
  .op-route { font-size: 11px; color: #4a5568; }
  .icon-sm { background: #1e2330; border: none; border-radius: 6px; padding: 5px 7px; font-size: 13px; cursor: pointer; }
  .rate { font-size: 15px; font-weight: 700; color: #22c55e; text-align: right; }
</style>
