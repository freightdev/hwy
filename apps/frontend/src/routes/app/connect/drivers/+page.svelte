<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { success, api, error as toastError } from '$lib/stores/toast.js';
  import { get, post } from '$lib/api.js';

  let activeTab = 'all';
  let search = '';
  let selectedDriver = null;
  let showAdd = false;
  let drivers = [];
  let loading = true;

  onMount(async () => {
    const res = await get('/drivers');
    if (res.error) toastError(res.error);
    else drivers = res.data;
    loading = false;
  });

  let newDriver = { name: '', truck: '', phone: '', email: '', license: '', doe: '', status: 'Available' };

  $: displayDrivers = drivers.filter(d =>
    d.name.toLowerCase().includes(search.toLowerCase()) &&
    (activeTab === 'all' || d.status.toLowerCase().replace(' ', '-') === activeTab)
  );

  function statusColor(s) {
    if (s === 'In Transit') return '#3b82f6';
    if (s === 'Available') return '#22c55e';
    if (s === 'At Pickup') return '#f59e0b';
    if (s === 'At Delivery') return '#8b5cf6';
    if (s === 'Off Duty') return '#6b7280';
    return '#4a5568';
  }

  async function addDriver() {
    if (!newDriver.name || !newDriver.truck) { toastError('Name and truck # required'); return; }
    const res = await post('/drivers', newDriver);
    if (res.error) { toastError(res.error); return; }
    drivers = [...drivers, res.data];
    success(`${newDriver.name} added as driver`);
    showAdd = false;
    newDriver = { name: '', truck: '', phone: '', email: '', license: '', doe: '', status: 'Available' };
  }

  function callDriver(d) { api(`VoIP call to ${d.name}`); }
  function messageDriver(d) { api(`Message to ${d.name}`); }
  function viewLoad(d) { api(`Load detail for ${d.load_id}`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/connect')}>‹</button>
    <div>
      <div class="page-title">Drivers</div>
      <div style="font-size:11px;color:#4a5568">{displayDrivers.length} Active Drivers</div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="icon-btn-sm" on:click={() => api('Filter drivers')}>⊟</button>
      <button class="icon-btn-sm" on:click={() => api('Export drivers')}>↑</button>
      <button class="btn btn-primary btn-sm" on:click={() => showAdd = true}>+ Add</button>
    </div>
  </div>

  {#if showAdd}
    <div class="section">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <span style="font-size:15px;font-weight:700">Add Driver</span>
          <button style="background:none;border:none;color:#6b7280;cursor:pointer" on:click={() => showAdd=false}>✕</button>
        </div>
        <div class="form-group"><label class="label">Full Name *</label><input bind:value={newDriver.name} placeholder="John Smith" /></div>
        <div class="row">
          <div class="col form-group"><label class="label">Truck # *</label><input bind:value={newDriver.truck} placeholder="#101" /></div>
          <div class="col form-group">
            <label class="label">Status</label>
            <select bind:value={newDriver.status}><option>Available</option><option>In Transit</option><option>Off Duty</option></select>
          </div>
        </div>
        <div class="form-group"><label class="label">Phone</label><input bind:value={newDriver.phone} placeholder="(555) 000-0000" /></div>
        <div class="form-group"><label class="label">Email</label><input bind:value={newDriver.email} placeholder="driver@company.com" /></div>
        <div class="row">
          <div class="col form-group"><label class="label">CDL Number</label><input bind:value={newDriver.license} placeholder="TX1234567" /></div>
          <div class="col form-group"><label class="label">CDL Expiry</label><input type="date" bind:value={newDriver.doe} /></div>
        </div>
        <button class="btn btn-primary btn-full" on:click={addDriver}>Add Driver</button>
      </div>
    </div>
  {:else if selectedDriver}
    <div class="section">
      <div class="driver-profile">
        <div class="driver-avatar-lg" style="background:{statusColor(selectedDriver.status)}22;color:{statusColor(selectedDriver.status)}">
          {selectedDriver.name.split(' ').map(w=>w[0]).join('')}
        </div>
        <div style="flex:1">
          <div style="font-size:18px;font-weight:700">{selectedDriver.name}</div>
          <div style="font-size:13px;color:#6b7280">Truck {selectedDriver.truck}</div>
          <span class="chip" style="background:{statusColor(selectedDriver.status)}22;color:{statusColor(selectedDriver.status)};margin-top:6px">● {selectedDriver.status}</span>
        </div>
      </div>

      <div class="driver-actions">
        <button class="action-btn" on:click={() => callDriver(selectedDriver)}>📞<span>Call</span></button>
        <button class="action-btn" on:click={() => messageDriver(selectedDriver)}>💬<span>Message</span></button>
        <button class="action-btn" on:click={() => api('Driver location tracking')}>📍<span>Track</span></button>
        <button class="action-btn" on:click={() => api('Driver documents')}>📄<span>Docs</span></button>
      </div>

      {#if selectedDriver.load_id}
        <div class="card" style="margin-bottom:12px">
          <div style="font-size:12px;color:#4a5568;font-weight:700;margin-bottom:8px">CURRENT LOAD</div>
          <div style="font-size:14px;font-weight:600">{selectedDriver.load_id}</div>
          <div style="font-size:13px;color:#6b7280;margin-top:2px">{selectedDriver.route}</div>
          <div style="font-size:14px;font-weight:700;color:#22c55e;margin-top:4px">{selectedDriver.rate}</div>
          <button class="btn btn-secondary btn-sm" style="margin-top:10px" on:click={() => viewLoad(selectedDriver)}>View Load Details</button>
        </div>
      {/if}

      <div class="card" style="margin-bottom:12px">
        <div style="font-size:12px;color:#4a5568;font-weight:700;margin-bottom:10px">DRIVER INFO</div>
        {#each [
          ['Phone', selectedDriver.phone],
          ['Email', selectedDriver.email],
          ['License', selectedDriver.license],
          ['CDL Expiry', selectedDriver.doe],
        ] as [k,v]}
          <div class="detail-row"><span style="color:#6b7280;font-size:13px">{k}</span><span style="font-size:13px;font-weight:600">{v}</span></div>
        {/each}
      </div>

      <div class="stats-row">
        <div class="stat-box"><div class="stat-val">{selectedDriver.loads_completed}</div><div class="stat-lbl">Loads</div></div>
        <div class="stat-box"><div class="stat-val" style="color:#22c55e">{selectedDriver.on_time}%</div><div class="stat-lbl">On Time</div></div>
        <div class="stat-box"><div class="stat-val" style="color:#f59e0b">{selectedDriver.rating}★</div><div class="stat-lbl">Rating</div></div>
      </div>

      <button class="btn btn-secondary btn-full" style="margin-top:12px" on:click={() => selectedDriver = null}>← Back to Drivers</button>
    </div>
  {:else}
    <div class="tabs">
      {#each [['all','All'],['in-transit','In Transit'],['available','Available'],['at-pickup','At Pickup'],['off-duty','Off Duty']] as [k,label]}
        <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
      {/each}
    </div>

    <div class="search-bar">
      <span>🔍</span>
      <input bind:value={search} placeholder="Search drivers..." />
    </div>

    <div class="card" style="margin:0 16px;padding:0;overflow:hidden">
      {#if loading}
        <div class="empty-state"><p>Loading drivers...</p></div>
      {:else}
        {#each displayDrivers as d}
          <div class="list-item driver-row">
            <div class="avatar" style="background:{statusColor(d.status)}22;color:{statusColor(d.status)}" on:click={() => selectedDriver = d} role="button" tabindex="0">
              {d.name.split(' ').map(w=>w[0]).join('')}
            </div>
            <div style="flex:1;min-width:0;cursor:pointer" on:click={() => selectedDriver = d} role="button" tabindex="0">
              <div style="display:flex;align-items:center;gap:6px">
                <span style="font-size:13px;font-weight:600">{d.name}</span>
                <span class="chip" style="background:{statusColor(d.status)}22;color:{statusColor(d.status)};font-size:10px">● {d.status}</span>
              </div>
              <div style="font-size:11px;color:#6b7280">Truck {d.truck}</div>
              {#if d.route}<div style="font-size:11px;color:#4a5568">{d.route}</div>{/if}
            </div>
            <div style="display:flex;gap:5px">
              <button class="icon-sm" on:click={() => callDriver(d)}>📞</button>
              <button class="icon-sm" on:click={() => messageDriver(d)}>💬</button>
            </div>
          </div>
        {/each}
        {#if displayDrivers.length === 0}
          <div class="empty-state"><div class="icon">🚛</div><p>No drivers found</p></div>
        {/if}
      {/if}
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .icon-btn-sm { background:#161a23;border:1px solid #1e2330;border-radius:7px;padding:6px 9px;font-size:13px;cursor:pointer; }
  .tabs { display:flex;border-bottom:1px solid #1e2330;overflow-x:auto; }
  .tab { padding:11px 12px;border:none;background:none;color:#6b7280;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .icon-sm { background:#1e2330;border:none;border-radius:6px;padding:5px 7px;font-size:13px;cursor:pointer; }
  .driver-profile { display:flex;gap:16px;align-items:flex-start;margin-bottom:16px; }
  .driver-avatar-lg { width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;flex-shrink:0; }
  .driver-actions { display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px; }
  .action-btn { background:#161a23;border:1px solid #1e2330;border-radius:12px;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;font-size:18px;cursor:pointer; }
  .action-btn span { font-size:11px;color:#6b7280; }
  .detail-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2330; }
  .detail-row:last-child { border-bottom:none; }
  .stats-row { display:grid;grid-template-columns:repeat(3,1fr);gap:8px; }
</style>
