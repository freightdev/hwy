<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/app.js';
  import { api, success, error as toastError } from '$lib/stores/toast.js';
  import { get } from '$lib/api.js';

  let activeTab = 'drivers';
  let showAdd = false;
  let drivers = [];
  let loading = true;
  let newMember = { name: '', email: '', role: 'Driver', phone: '' };

  onMount(async () => {
    const res = await get('/drivers');
    if (res.error) toastError(res.error);
    else drivers = res.data;
    loading = false;
  });

  const dispatchers = [
    { name: 'Mike Johnson', role: 'Dispatcher', status: 'Active', email: 'mike.j@company.com' },
    { name: 'Sarah Williams', role: 'Dispatcher', status: 'Active', email: 'sarah.w@company.com' },
  ];

  const staff = [
    { name: $user.name || 'You', role: $user.role || 'Owner', status: 'Active', email: $user.email || '' },
  ];

  function addMember() {
    success(`Invitation sent to ${newMember.email || newMember.name}`);
    showAdd = false;
    newMember = { name: '', email: '', role: 'Driver', phone: '' };
  }

  function manageUser(m) { api(`User management for ${m.name} requires auth API`); }
  function removeUser(m) { api(`Remove ${m.name} requires team management API`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/more')}>‹</button>
    <div class="page-title">Users & Team</div>
    <button class="btn btn-primary btn-sm" on:click={() => showAdd = true}>+ Add User</button>
  </div>

  <div class="section">
    <div class="team-stats">
      {#each [['Total Users', drivers.length + dispatchers.length + staff.length],['Drivers', drivers.length],['Dispatchers', dispatchers.length],['Staff', staff.length]] as [label, val]}
        <div class="stat-box"><div class="stat-val">{val}</div><div class="stat-lbl">{label}</div></div>
      {/each}
    </div>
  </div>

  <div class="tabs">
    {#each [['drivers','Drivers'],['dispatchers','Dispatchers'],['staff','Staff']] as [k,label]}
      <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
    {/each}
  </div>

  {#if showAdd}
    <div class="section">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <span style="font-size:15px;font-weight:700">Add Team Member</span>
          <button style="background:none;border:none;color:#6b7280;cursor:pointer" on:click={() => showAdd=false}>✕</button>
        </div>
        <div class="form-group"><label class="label">Full Name</label><input bind:value={newMember.name} placeholder="John Smith" /></div>
        <div class="form-group"><label class="label">Email *</label><input bind:value={newMember.email} placeholder="john@company.com" /></div>
        <div class="form-group"><label class="label">Phone</label><input bind:value={newMember.phone} placeholder="(555) 000-0000" /></div>
        <div class="form-group">
          <label class="label">Role</label>
          <select bind:value={newMember.role}>
            <option>Driver</option><option>Dispatcher</option><option>Fleet Manager</option><option>Accountant</option><option>Safety Manager</option>
          </select>
        </div>
        <button class="btn btn-primary btn-full" on:click={addMember}>Send Invitation</button>
      </div>
    </div>
  {:else}
    <div class="section" style="padding-top:8px">
      {#if activeTab === 'drivers'}
        <div class="card" style="padding:0;overflow:hidden">
          {#if loading}
            <div class="empty-state"><p>Loading drivers...</p></div>
          {:else}
            {#each drivers as d}
              <div class="list-item">
                <div class="avatar">{d.name.split(' ').map(w=>w[0]).join('')}</div>
                <div style="flex:1">
                  <div style="font-size:13px;font-weight:600">{d.name}</div>
                  <div style="font-size:11px;color:#6b7280">{d.email}</div>
                </div>
                <div style="display:flex;align-items:center;gap:8px">
                  <span class="chip chip-green" style="font-size:10px">{d.status || 'Active'}</span>
                  <button class="btn btn-secondary btn-sm" on:click={() => manageUser(d)}>Manage</button>
                </div>
              </div>
            {/each}
          {/if}
          <button class="list-item add-row" on:click={() => { showAdd = true; newMember.role = 'Driver'; }}>
            <div class="avatar" style="background:#1e3a5f;color:#3b82f6">+</div>
            <span style="color:#3b82f6;font-size:13px;font-weight:600">Add Driver</span>
          </button>
        </div>

      {:else if activeTab === 'dispatchers'}
        <div class="card" style="padding:0;overflow:hidden">
          {#each dispatchers as m}
            <div class="list-item">
              <div class="avatar" style="background:#2d1b5e;color:#8b5cf6">{m.name.split(' ').map(w=>w[0]).join('')}</div>
              <div style="flex:1">
                <div style="font-size:13px;font-weight:600">{m.name}</div>
                <div style="font-size:11px;color:#6b7280">{m.role} • {m.email}</div>
              </div>
              <div style="display:flex;align-items:center;gap:8px">
                <span class="chip chip-green" style="font-size:10px">{m.status}</span>
                <button class="btn btn-secondary btn-sm" on:click={() => manageUser(m)}>Manage</button>
              </div>
            </div>
          {/each}
          <button class="list-item add-row" on:click={() => { showAdd = true; newMember.role = 'Dispatcher'; }}>
            <div class="avatar" style="background:#2d1b5e;color:#8b5cf6">+</div>
            <span style="color:#8b5cf6;font-size:13px;font-weight:600">Add Dispatcher</span>
          </button>
        </div>

      {:else if activeTab === 'staff'}
        <div class="card" style="padding:0;overflow:hidden">
          {#each staff as m}
            <div class="list-item">
              <div class="avatar" style="background:#1a2b1a;color:#22c55e">{(m.name||'Y').charAt(0)}</div>
              <div style="flex:1">
                <div style="font-size:13px;font-weight:600">{m.name} <span class="chip chip-blue" style="font-size:9px">You</span></div>
                <div style="font-size:11px;color:#6b7280">{m.role} • {m.email}</div>
              </div>
              <span class="chip chip-green" style="font-size:10px">{m.status}</span>
            </div>
          {/each}
          <button class="list-item add-row" on:click={() => { showAdd = true; newMember.role = 'Fleet Manager'; }}>
            <div class="avatar" style="background:#1a2b1a;color:#22c55e">+</div>
            <span style="color:#22c55e;font-size:13px;font-weight:600">Add Staff</span>
          </button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .team-stats { display:grid;grid-template-columns:repeat(4,1fr);gap:8px; }
  .tabs { display:flex;border-bottom:1px solid #1e2330; }
  .tab { flex:1;padding:11px;border:none;background:none;color:#6b7280;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .add-row { cursor:pointer;border-bottom:none !important; }
  .add-row:hover { background:#161a23; }
</style>
