<script>
  import { goto } from '$app/navigation';

  import { api, info, success } from '$lib/stores/toast.js';

  let search = '';
  let showMessages = false;
  let showMap = false;
  let showInvite = false;
  let inviteType = 'Driver';
  let inviteCompany = '';
  let inviteEmail = '';

  const sections = [
    { label: 'Drivers', icon: '🚛', count: 32, sub: '32 Active', href: '/app/connect/drivers', color: '#3b82f6' },
    { label: 'Dispatchers', icon: '📡', count: 6, sub: '6 Active', href: null, action: () => info('Dispatcher management'), color: '#8b5cf6' },
    { label: 'Brokers', icon: '🤝', count: 63, sub: '63 Connected', href: '/app/connect/brokers', color: '#f59e0b' },
    { label: 'Carriers', icon: '🚚', count: 45, sub: '45 Connected', href: null, action: () => api('Carrier network'), color: '#22c55e' },
    { label: 'Shippers', icon: '📦', count: 12, sub: '12 Favorites', href: null, action: () => api('Shipper network'), color: '#ec4899' },
    { label: 'Customers', icon: '👥', count: 24, sub: '24 Connected', href: null, action: () => api('Customer management'), color: '#06b6d4' },
    { label: 'Fuel Cards', icon: '⛽', count: 3, sub: '3 Connected', href: null, action: () => api('Fuel card management'), color: '#f97316' },
    { label: 'Service Providers', icon: '🔧', count: 8, sub: '8 Connected', href: null, action: () => api('Service provider network'), color: '#84cc16' },
  ];

  const messages = [
    { name: 'Mike Smith', role: 'Driver', time: '8:30 AM', msg: 'On my way to pickup', unread: 1, color: '#3b82f6' },
    { name: 'Landstar', role: 'Carrier', time: '5:15 AM', msg: 'Load confirmed. Thank you!', unread: 0, color: '#f59e0b' },
    { name: 'Sarah Johnson', role: 'Driver', time: 'Yesterday', msg: 'POD uploaded', unread: 0, color: '#22c55e' },
    { name: 'CH Robinson', role: 'Broker', time: '8:00 AM', msg: 'Update on ETA?', unread: 1, color: '#8b5cf6' },
    { name: 'TQL', role: 'Broker', time: 'Yesterday', msg: 'Load board available', unread: 0, color: '#f97316' },
  ];

  const pendingRequests = [
    { name: 'AKZ Logistics', mc: 'MC-167264', time: '7m ago', type: 'Broker' },
    { name: 'John Doe', email: 'johndoe@email.com', time: '21m ago', type: 'Dispatcher' },
    { name: 'FastFreight Inc.', mc: 'MC-490783', time: '1h ago', type: 'Carrier' },
    { name: 'Reliable Transport', mc: 'MC-490783', time: '2h ago', type: 'Carrier' },
  ];

  function navigate(section) {
    if (section.href) goto(section.href);
    else if (section.action) section.action();
  }

  function sendInvite() {
    if (!inviteEmail) { info('Email or company required'); return; }
    success(`Invitation sent to ${inviteEmail || inviteCompany}`);
    showInvite = false;
    inviteEmail = '';
    inviteCompany = '';
  }

  function acceptRequest(r) { success(`${r.name} connection accepted`); }
  function declineRequest(r) { info(`${r.name} request declined`); }
  function openMessage(m) { api(`Direct message with ${m.name}`); }
</script>

<div class="page">
  <div class="page-header-custom">
    <div>
      <div style="font-size:20px;font-weight:800">HWY <span style="color:#3b82f6">TMS</span></div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="icon-btn" on:click={() => showMessages = !showMessages}>
        💬 {#if messages.filter(m=>m.unread).length > 0}<span class="badge">{messages.filter(m=>m.unread).length}</span>{/if}
      </button>
      <button class="icon-btn" on:click={() => showMap = !showMap}>🗺️</button>
      <button class="icon-btn" on:click={() => showInvite = true}>+ Invite</button>
    </div>
  </div>

  {#if showMap}
    <div class="map-placeholder card section">
      <div style="text-align:center;padding:40px 0">
        <div style="font-size:40px;margin-bottom:12px">🗺️</div>
        <div style="font-size:15px;font-weight:600;margin-bottom:6px">Connections Map</div>
        <div style="font-size:12px;color:#6b7280">View your driver & broker network geographically</div>
        <button class="btn btn-secondary" style="margin-top:16px" on:click={() => api('Interactive connections map')}>Load Map View</button>
      </div>
    </div>
  {/if}

  {#if showInvite}
    <div class="section">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <span style="font-size:15px;font-weight:700">Invite to Connect</span>
          <button style="background:none;border:none;color:#6b7280;cursor:pointer;font-size:18px" on:click={() => showInvite=false}>✕</button>
        </div>
        <div class="form-group">
          <label class="label">Type</label>
          <select bind:value={inviteType}>
            <option>Driver</option><option>Dispatcher</option><option>Carrier</option><option>Broker</option><option>Shipper</option>
          </select>
        </div>
        <div class="form-group">
          <label class="label">Company / Name</label>
          <input bind:value={inviteCompany} placeholder="Company name" />
        </div>
        <div class="form-group">
          <label class="label">Email or Phone</label>
          <input bind:value={inviteEmail} placeholder="email@company.com" />
        </div>
        <button class="btn btn-primary btn-full" on:click={sendInvite}>Send Invitation</button>
      </div>
    </div>
  {/if}

  <!-- Search -->
  <div class="search-bar">
    <span>🔍</span>
    <input bind:value={search} placeholder="Search your network and connections..." />
    <button style="background:none;border:none;color:#6b7280;cursor:pointer" on:click={() => api('Filter connections')}>⊟</button>
  </div>

  <!-- Connection sections grid -->
  {#if !showMessages}
  <div class="section" style="padding-top:8px">
    <div class="connect-grid">
      {#each sections as s}
        <button class="connect-card" on:click={() => navigate(s)}>
          <div class="connect-icon" style="background:{s.color}22;color:{s.color}">{s.icon}</div>
          <div style="font-size:14px;font-weight:700">{s.label}</div>
          <div style="font-size:12px;color:#6b7280">{s.sub}</div>
          <div class="connect-arrow">›</div>
        </button>
      {/each}
    </div>
  </div>

  <!-- Pending requests -->
  {#if pendingRequests.length}
  <div class="section" style="padding-top:0">
    <div class="subsection-label">Connection Requests</div>
    <div class="card" style="padding:0;overflow:hidden">
      {#each pendingRequests as r}
        <div class="list-item">
          <div class="avatar">{r.name.charAt(0)}</div>
          <div style="flex:1;min-width:0">
            <div style="font-size:13px;font-weight:600">{r.name}</div>
            <div style="font-size:11px;color:#6b7280">{r.type} • {r.mc || r.email || ''} • {r.time}</div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="btn btn-primary btn-sm" on:click={() => acceptRequest(r)}>Accept</button>
            <button class="btn btn-secondary btn-sm" on:click={() => declineRequest(r)}>Decline</button>
          </div>
        </div>
      {/each}
    </div>
  </div>
  {/if}
  {/if}

  <!-- Messages panel -->
  {#if showMessages}
  <div class="section" style="padding-top:8px">
    <div class="subsection-label">Messages</div>
    <div class="card" style="padding:0;overflow:hidden">
      {#each messages as m}
        <div class="list-item" on:click={() => openMessage(m)} role="button" tabindex="0" style="cursor:pointer">
          <div class="avatar" style="background:{m.color}22;color:{m.color}">{m.name.charAt(0)}</div>
          <div style="flex:1;min-width:0">
            <div style="display:flex;justify-content:space-between">
              <span style="font-size:13px;font-weight:600">{m.name}</span>
              <span style="font-size:11px;color:#6b7280">{m.time}</span>
            </div>
            <div style="font-size:12px;color:#6b7280;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{m.msg}</div>
          </div>
          {#if m.unread > 0}
            <div class="unread-badge">{m.unread}</div>
          {/if}
        </div>
      {/each}
    </div>
    <button class="btn btn-secondary btn-full" style="margin-top:12px" on:click={() => api('Full messaging system')}>New Message</button>
  </div>
  {/if}
</div>

<style>
  .page-header-custom { display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .icon-btn { background:#161a23;border:1px solid #1e2330;border-radius:8px;padding:7px 10px;font-size:13px;cursor:pointer;position:relative; }
  .badge { position:absolute;top:-4px;right:-4px;background:#ef4444;color:#fff;font-size:9px;font-weight:700;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center; }
  .connect-grid { display:grid;grid-template-columns:repeat(2,1fr);gap:10px; }
  .connect-card { background:#161a23;border:1px solid #1e2330;border-radius:14px;padding:16px;text-align:left;cursor:pointer;transition:background 0.15s;position:relative; }
  .connect-card:hover { background:#1e2330; }
  .connect-icon { width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:8px; }
  .connect-arrow { position:absolute;top:14px;right:14px;color:#4a5568;font-size:18px; }
  .subsection-label { font-size:10px;color:#4a5568;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;display:block; }
  .unread-badge { background:#3b82f6;color:#fff;font-size:10px;font-weight:700;min-width:18px;height:18px;border-radius:9px;display:flex;align-items:center;justify-content:center;padding:0 4px; }
</style>
