<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { company, user, onboarded } from '$lib/stores/app.js';
  import { success, error as toastError } from '$lib/stores/toast.js';
  import { get, put, post, clearToken } from '$lib/api.js';

  let activeTab = 'general';
  let companyData = null;
  let loading = true;
  let showMockData = true;
  let savingMock = false;

  let deleteStep = 0;

  onMount(async () => {
    const res = await get('/company');
    if (res.data) {
      companyData = res.data;
      showMockData = res.data.show_mock_data;
      company.set(res.data);
    }
    loading = false;
  });

  let form = {
    name: '', mc: '', dot: '', scac: '', type: 'For-Hire Carrier',
    founded: '', address: '', city: '', state: '', zip: '',
    phone: '', email: '', website: '',
    fleet_size: 0,
  };

  $: if (companyData) {
    form.name = companyData.name;
    form.mc = companyData.mc;
    form.dot = companyData.dot;
    form.scac = companyData.scac;
    form.type = companyData.type;
    form.founded = companyData.founded;
    form.address = companyData.address;
    form.city = companyData.city;
    form.state = companyData.state;
    form.zip = companyData.zip;
    form.phone = companyData.phone;
    form.email = companyData.email;
    form.website = companyData.website;
    form.fleet_size = companyData.fleet_size;
  }

  async function saveCompany() {
    const res = await put('/company', form);
    if (res.error) { toastError(res.error); return; }
    company.set(res.data);
    companyData = res.data;
    success('Company settings saved');
  }

  function signOut() {
    clearToken();
    onboarded.set(false);
    goto('/');
  }

  async function toggleMock() {
    savingMock = true;
    const res = await post('/company/toggle-mock');
    if (res.error) { toastError(res.error); savingMock = false; return; }
    showMockData = res.data.show_mock_data;
    company.set(res.data);
    companyData = res.data;
    success(res.message || (showMockData ? 'Mock data restored' : 'Mock data removed'));
    savingMock = false;
  }

  function startDelete() { deleteStep = 1; }

  function confirmDelete() {
    if (deleteStep === 1) { deleteStep = 2; return; }
    if (deleteStep === 2) {
      const input = document.getElementById('delete-confirm-input');
      if (input && input.value !== 'DELETE ALL DATA') {
        toastError('Type DELETE ALL DATA to confirm');
        return;
      }
      executeDelete();
    }
  }

  function cancelDelete() { deleteStep = 0; }

  async function executeDelete() {
    const res = await post('/company/reset');
    if (res.error) { toastError(res.error); return; }
    clearToken();
    onboarded.set(false);
    goto('/onboarding');
  }

  const states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'];
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/more')}>‹</button>
    <div class="page-title">Settings</div>
    <button class="btn btn-primary btn-sm" on:click={saveCompany}>Save</button>
  </div>

  <div class="tabs">
    {#each [['general','General'],['authority','Authority'],['insurance','Insurance'],['preferences','Preferences']] as [k,label]}
      <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
    {/each}
  </div>

  {#if activeTab === 'general'}
    <div class="section">
      {#if loading}
        <div class="empty-state"><p>Loading settings...</p></div>
      {:else}
        <div class="section-divider">Company Info</div>
        <div class="form-group"><label class="label">Company Name</label><input bind:value={form.name} /></div>
        <div class="row">
          <div class="col form-group"><label class="label">MC Number</label><input bind:value={form.mc} /></div>
          <div class="col form-group"><label class="label">DOT Number</label><input bind:value={form.dot} /></div>
        </div>
        <div class="row">
          <div class="col form-group"><label class="label">SCAC</label><input bind:value={form.scac} maxlength="4" /></div>
          <div class="col form-group"><label class="label">Fleet Size</label><input type="number" bind:value={form.fleet_size} /></div>
        </div>
        <div class="form-group"><label class="label">Company Email</label><input type="email" bind:value={form.email} /></div>
        <div class="form-group"><label class="label">Phone</label><input type="tel" bind:value={form.phone} /></div>
        <div class="form-group"><label class="label">Website</label><input bind:value={form.website} /></div>

        <div class="section-divider">Address</div>
        <div class="form-group"><label class="label">Street Address</label><input bind:value={form.address} /></div>
        <div class="row">
          <div class="col form-group"><label class="label">City</label><input bind:value={form.city} /></div>
          <div class="col form-group" style="flex:0 0 70px"><label class="label">State</label>
            <select bind:value={form.state}><option value="">--</option>{#each states as s}<option>{s}</option>{/each}</select>
          </div>
          <div class="col form-group" style="flex:0 0 80px"><label class="label">ZIP</label><input bind:value={form.zip} /></div>
        </div>

        <div class="section-divider">Mock Data</div>
        <div class="pref-row">
          <div>
            <div style="font-size:13px;font-weight:600">Show Mock Data</div>
            <div style="font-size:11px;color:#6b7280">Toggle seed data on/off for testing</div>
          </div>
          <button class="toggle {showMockData ? 'on' : ''}" on:click={toggleMock} disabled={savingMock}></button>
        </div>

        <div class="section-divider">Account Actions</div>
        <button class="btn btn-danger btn-full" style="margin-bottom:8px" on:click={signOut}>Sign Out</button>

        {#if deleteStep === 0}
          <button class="btn btn-danger btn-full" on:click={startDelete}>Delete All Data</button>
        {:else if deleteStep === 1}
          <div class="delete-warning">
            <p style="color:#ef4444;font-size:13px;font-weight:700;margin-bottom:8px">⚠️ Are you sure?</p>
            <p style="font-size:12px;color:#6b7280;margin-bottom:12px">This will permanently delete all company data including drivers, loads, brokers, invoices, and documents. Your account will be reset to start onboarding again.</p>
            <div class="nav-btns" style="margin-top:0;padding-top:0">
              <button class="btn btn-secondary" style="flex:1" on:click={cancelDelete}>Cancel</button>
              <button class="btn btn-danger" style="flex:1" on:click={confirmDelete}>Yes, Delete Everything</button>
            </div>
          </div>
        {:else if deleteStep === 2}
          <div class="delete-warning">
            <p style="color:#ef4444;font-size:13px;font-weight:700;margin-bottom:8px">⚠️ Final Confirmation</p>
            <p style="font-size:12px;color:#6b7280;margin-bottom:8px">Type <strong>DELETE ALL DATA</strong> below to confirm:</p>
            <input id="delete-confirm-input" type="text" placeholder='Type "DELETE ALL DATA"' style="width:100%;margin-bottom:12px" />
            <div class="nav-btns" style="margin-top:0;padding-top:0">
              <button class="btn btn-secondary" style="flex:1" on:click={cancelDelete}>Cancel</button>
              <button class="btn btn-danger" style="flex:1" on:click={confirmDelete}>Confirm & Delete</button>
            </div>
          </div>
        {/if}
      {/if}
    </div>

  {:else if activeTab === 'authority'}
    <div class="section">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
          <span style="font-size:15px;font-weight:700">FMCSA Authority</span>
          <span class="chip chip-green">Active</span>
        </div>
        {#each [
          ['MC Number', form.mc || 'MC-1234567'],
          ['DOT Number', form.dot || '3456789'],
          ['Authority Type', 'For-Hire Carrier'],
          ['Status', 'Active'],
          ['Insurance Required', 'Yes — BMC-84 Filed'],
        ] as [k, v]}
          <div class="detail-row">
            <span style="color:#6b7280;font-size:13px">{k}</span>
            <span style="font-size:13px;font-weight:600">{v}</span>
          </div>
        {/each}
      </div>
    </div>

  {:else if activeTab === 'insurance'}
    <div class="section">
      <div class="card">
        <div style="font-size:15px;font-weight:700;margin-bottom:12px">Insurance Coverage</div>
        {#each [
          ['Primary Liability', '$1,000,000', 'Active'],
          ['Cargo Insurance', '$100,000', 'Active'],
          ['Physical Damage', 'Agreed Value', 'Active'],
          ['General Liability', '$2,000,000', 'Active'],
        ] as [type, amount, status]}
          <div class="detail-row">
            <div>
              <div style="font-size:13px;font-weight:600">{type}</div>
              <div style="font-size:11px;color:#6b7280">{amount}</div>
            </div>
            <span class="chip chip-green" style="font-size:10px">{status}</span>
          </div>
        {/each}
      </div>
    </div>

  {:else if activeTab === 'preferences'}
    <div class="section">
      <div class="card" style="margin-bottom:12px">
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">App Preferences</div>
        {#each [['Dark Mode', true],['Push Notifications', false],['Email Alerts', true],['SMS Alerts', false]] as [label, val]}
          <div class="pref-row">
            <span style="font-size:13px">{label}</span>
            <button class="toggle {val ? 'on' : ''}" on:click={() => toastError(`${label} not available yet`)}></button>
          </div>
        {/each}
      </div>
      <div class="card">
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">Security</div>
        {#each [['Two-Factor Auth', false],['Biometric Login', true]] as [label, val]}
          <div class="pref-row">
            <span style="font-size:13px">{label}</span>
            <button class="toggle {val ? 'on' : ''}" on:click={() => toastError(`${label} not available yet`)}></button>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .tabs { display:flex;border-bottom:1px solid #1e2330;overflow-x:auto; }
  .tab { flex:1;padding:11px 10px;border:none;background:none;color:#6b7280;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .section-divider { font-size:10px;color:#4a5568;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin:16px 0 12px;padding-bottom:8px;border-bottom:1px solid #1e2330; }
  .detail-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2330; }
  .detail-row:last-child { border-bottom:none; }
  .pref-row { display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #1e2330; }
  .pref-row:last-child { border-bottom:none; }
  .delete-warning { background:#1a1111;border:1px solid #3f1a1a;border-radius:10px;padding:14px;margin-top:8px; }
</style>
