<script>
  import { onMount } from 'svelte';
  import { success, api, info, error as toastError } from '$lib/stores/toast.js';
  import { get, post } from '$lib/api.js';

  let activeTab = 'my';
  let selectedFlow = null;
  let showCreate = false;
  let showCategories = false;
  let showHistory = false;
  let search = '';
  let flows = [];
  let loading = true;

  onMount(async () => {
    const res = await get('/flows');
    if (res.error) toastError(res.error);
    else flows = res.data;
    loading = false;
  });

  const templates = [
    { id: 't1', name: 'Post-Delivery Workflow', category: 'Load Management', steps: 7, type: 'Auto', icon: '📦' },
    { id: 't2', name: 'Driver Check-In Flow', category: 'Driver Communication', steps: 5, type: 'Manual', icon: '🚛' },
    { id: 't3', name: 'Invoice Generation', category: 'Billing & Invoicing', steps: 4, type: 'Auto', icon: '💰' },
    { id: 't4', name: 'IFTA Filing Flow', category: 'Documents & Compliance', steps: 6, type: 'Auto', icon: '📋' },
    { id: 't5', name: 'Broker Setup Flow', category: 'Load Management', steps: 3, type: 'Manual', icon: '🤝' },
  ];

  const categories = [
    { name: 'Load Management', count: 8, icon: '📦' },
    { name: 'Driver Communication', count: 6, icon: '🚛' },
    { name: 'Documents & Compliance', count: 7, icon: '📋' },
    { name: 'Billing & Invoicing', count: 5, icon: '💰' },
    { name: 'Safety & Alerts', count: 4, icon: '⚠️' },
    { name: 'Maintenance', count: 3, icon: '🔧' },
    { name: 'Dispatch Operations', count: 6, icon: '📡' },
    { name: 'Custom Integrations', count: 4, icon: '⚙️' },
  ];

  const history = [
    { name: 'Post-Delivery Workflow', time: '9:15 AM', status: 'Completed', type: 'Auto' },
    { name: 'Driver Check-In Flow', time: '8:47 AM', status: 'Completed', type: 'Manual' },
    { name: 'Invoice & Docs Flow', time: '8:32 AM', status: 'Completed', type: 'Auto' },
    { name: 'POD Upload Flow', time: '7:58 AM', status: 'Completed', type: 'Manual' },
    { name: 'Load Assignment Flow', time: 'Yesterday 6:21 PM', status: 'Completed', type: 'Auto' },
    { name: 'Broker Update Flow', time: 'Yesterday 5:44 PM', status: 'Failed', type: 'Auto' },
    { name: 'Emergency Call Flow', time: 'Yesterday 3:12 PM', status: 'Completed', type: 'Manual' },
  ];

  const flowSteps = {
    1: [
      { icon: '📥', title: 'Receive POD from Driver', sub: 'Trigger: Document Uploaded' },
      { icon: '✅', title: 'Validate POD', sub: 'Check document completeness' },
      { icon: '🔄', title: 'Update Load Status', sub: 'Mark as Delivered' },
      { icon: '📧', title: 'Notify Customer', sub: 'Send delivery notification' },
      { icon: '💰', title: 'Generate Invoice', sub: 'Create & send invoice' },
      { icon: '📁', title: 'Archive Documents', sub: 'Store in load folder' },
    ],
    2: [
      { icon: '👤', title: 'Driver Starts Check-In', sub: 'Manual Trigger' },
      { icon: '📍', title: 'Capture Location', sub: 'Get current GPS location' },
      { icon: '✅', title: 'Confirm Appointment', sub: 'Verify pickup details' },
      { icon: '📡', title: 'Notify Dispatcher', sub: 'Send check-in notification' },
      { icon: '🔄', title: 'Update Load', sub: 'Mark as Checked In' },
    ]
  };

  $: filtered = flows.filter(f => f.name.toLowerCase().includes(search.toLowerCase()));

  async function toggleFlow(id) {
    const res = await post(`/flows/${id}/toggle`);
    if (res.error) { toastError(res.error); return; }
    flows = flows.map(f => f.id === id ? res.data : f);
    success(`${res.data.name} ${res.data.enabled ? 'enabled' : 'disabled'}`);
  }

  async function runFlow(f) {
    const res = await post(`/flows/${f.id}/run`);
    if (res.error) { toastError(res.error); return; }
    success(`Running ${f.name}...`);
  }

  function openFlow(f) { selectedFlow = f; }
  function createFlow(fromTemplate) {
    showCreate = false;
    api(fromTemplate ? 'Flow builder requires API integration for saving' : 'Custom flow builder coming soon');
  }
</script>

<div class="page">
  <div class="page-header">
    {#if selectedFlow}
      <button class="back-btn" on:click={() => selectedFlow = null}>‹</button>
      <div class="page-title">{selectedFlow.name}</div>
      <button class="icon-btn-sm" on:click={() => api('Flow editor')}>✏️</button>
    {:else if showCreate}
      <button class="back-btn" on:click={() => showCreate = false}>‹</button>
      <div class="page-title">Create New Flow</div>
      <button class="close-btn" on:click={() => showCreate = false}>✕</button>
    {:else if showCategories}
      <button class="back-btn" on:click={() => showCategories = false}>‹</button>
      <div class="page-title">Flow Categories</div>
      <button class="close-btn" on:click={() => showCategories = false}>✕</button>
    {:else if showHistory}
      <button class="back-btn" on:click={() => showHistory = false}>‹</button>
      <div class="page-title">Flow History</div>
    {:else}
      <div>
        <div class="page-title">Flows</div>
        <div style="font-size:11px;color:#4a5568">Automate your operations</div>
      </div>
      <div style="display:flex;gap:8px">
        <button class="icon-btn-sm" on:click={() => showCategories = true}>⊞</button>
        <button class="icon-btn-sm" on:click={() => showHistory = true}>📋</button>
        <button class="btn btn-primary btn-sm" on:click={() => showCreate = true}>+ New</button>
      </div>
    {/if}
  </div>

  {#if selectedFlow}
    <div class="section">
      <div class="flow-detail-header">
        <div class="flow-icon-lg">{selectedFlow.icon}</div>
        <div>
          <div style="font-size:16px;font-weight:700">{selectedFlow.name}</div>
          <div style="font-size:12px;color:#6b7280">Automates the {selectedFlow.name.toLowerCase()} process end to end.</div>
        </div>
      </div>

      <div class="flow-stats">
        <div class="stat-box"><div class="stat-val">{(flowSteps[selectedFlow.id] || flowSteps[1]).length}</div><div class="stat-lbl">Steps</div></div>
        <div class="stat-box"><div class="stat-val">3</div><div class="stat-lbl">Integrations</div></div>
        <div class="stat-box"><div class="stat-val">12m</div><div class="stat-lbl">Avg. Time</div></div>
      </div>

      <div class="subsection-label">Flow Steps</div>
      <div class="card" style="padding:0;overflow:hidden;margin-bottom:16px">
        {#each (flowSteps[selectedFlow.id] || flowSteps[1]) as step, i}
          <div class="step-row">
            <div class="step-num-badge">{i + 1}</div>
            <div class="step-icon">{step.icon}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{step.title}</div>
              <div style="font-size:11px;color:#6b7280">{step.sub}</div>
            </div>
          </div>
        {/each}
      </div>

      <button class="btn btn-primary btn-full" on:click={() => runFlow(selectedFlow)}>▶ Run Flow</button>
      <button class="btn btn-secondary btn-full" style="margin-top:8px" on:click={() => api('Flow duplication')}>⎘ Duplicate Flow</button>
    </div>

  {:else if showCreate}
    <div class="section">
      <div class="create-tabs">
        <button class="create-tab active">Start from Template</button>
        <button class="create-tab" on:click={() => createFlow(false)}>Start from Scratch</button>
      </div>

      <div class="create-section-label">Load Management</div>
      {#each categories as cat}
        <div class="template-category" on:click={() => api(`${cat.name} templates`)} role="button" tabindex="0">
          <span class="cat-icon">{cat.icon}</span>
          <div style="flex:1">
            <div style="font-size:14px;font-weight:600">{cat.name}</div>
            <div style="font-size:11px;color:#6b7280">{cat.count} templates</div>
          </div>
          <span style="color:#4a5568">›</span>
        </div>
      {/each}
    </div>

  {:else if showCategories}
    <div class="section">
      <div class="cat-grid">
        {#each categories as cat}
          <button class="cat-card" on:click={() => api(`${cat.name} templates`)}>
            <span class="cat-icon-lg">{cat.icon}</span>
            <div style="font-size:13px;font-weight:600;margin-top:8px">{cat.name}</div>
            <div style="font-size:11px;color:#6b7280">{cat.count} templates</div>
          </button>
        {/each}
      </div>
    </div>

  {:else if showHistory}
    <div class="section">
      <div class="hist-tabs">
        {#each ['All', 'Success', 'Failed', 'Manual', 'Auto'] as t}
          <button class="status-tab" class:active={t === 'All'}>{t}</button>
        {/each}
      </div>
      <div class="subsection-label">Today</div>
      <div class="card" style="padding:0;overflow:hidden">
        {#each history as h}
          <div class="list-item">
            <div class="avatar" style="background:#1e2330;font-size:16px">{flows.find(f=>f.name===h.name)?.icon||'⚡'}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{h.name}</div>
              <div style="font-size:11px;color:#6b7280">{h.type} • {h.time}</div>
            </div>
            <span class={h.status === 'Completed' ? 'chip chip-green' : 'chip chip-red'} style="font-size:11px">
              {h.status === 'Completed' ? '✓' : '✕'} {h.status}
            </span>
          </div>
        {/each}
      </div>
    </div>

  {:else}
    <div class="tabs">
      {#each [['my','My Flows'],['team','Team Flows'],['templates','Templates']] as [k,label]}
        <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
      {/each}
    </div>

    <div class="search-bar">
      <span>🔍</span>
      <input bind:value={search} placeholder="Search flows..." />
    </div>

    {#if activeTab === 'my'}
      <div class="section" style="padding-top:8px">
        <div class="section-top">
          <span class="subsection-label">My Saved Flows — {flows.length} Flows</span>
          <button class="btn btn-secondary btn-sm" on:click={() => showCreate = true}>+ New Flow</button>
        </div>

        <div class="card" style="padding:0;overflow:hidden">
          {#if loading}
            <div class="empty-state"><p>Loading flows...</p></div>
          {:else}
            {#each filtered as f}
              <div class="flow-row">
                <div class="flow-icon-sm">{f.icon}</div>
                <div style="flex:1;cursor:pointer" on:click={() => openFlow(f)} role="button" tabindex="0">
                  <div style="font-size:13px;font-weight:600">{f.name}</div>
                  <div style="font-size:11px;color:#6b7280">{f.steps} steps • {f.type}</div>
                </div>
                <button class="run-btn" on:click={() => runFlow(f)}>▶</button>
                <button
                  class="toggle {f.enabled ? 'on' : ''}"
                  on:click={() => toggleFlow(f.id)}
                  aria-label="Toggle {f.name}"
                ></button>
                <button class="icon-btn-sm" on:click={() => info('Flow options')}>⋯</button>
              </div>
            {/each}
          {/if}
        </div>
      </div>

    {:else if activeTab === 'team'}
      <div class="empty-state">
        <div class="icon">👥</div>
        <p>No team flows yet. Invite teammates to collaborate on flows.</p>
        <button class="btn btn-primary" style="margin-top:16px" on:click={() => api('Team flow sharing')}>Invite Team</button>
      </div>

    {:else if activeTab === 'templates'}
      <div class="section" style="padding-top:8px">
        {#each templates as t}
          <div class="card" style="margin-bottom:10px;display:flex;align-items:center;gap:12px">
            <div class="flow-icon-sm">{t.icon}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{t.name}</div>
              <div style="font-size:11px;color:#6b7280">{t.category} • {t.steps} steps • {t.type}</div>
            </div>
            <button class="btn btn-primary btn-sm" on:click={() => createFlow(true)}>Use</button>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .page-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 16px; border-bottom: 1px solid #1e2330;
    position: sticky; top: 0; background: #0d0f14; z-index: 50;
  }
  .back-btn { background: none; border: none; color: #3b82f6; font-size: 24px; cursor: pointer; }
  .close-btn { background: none; border: none; color: #6b7280; font-size: 18px; cursor: pointer; }
  .icon-btn-sm { background: #161a23; border: 1px solid #1e2330; border-radius: 7px; padding: 6px 9px; font-size: 13px; cursor: pointer; }

  .tabs { display: flex; border-bottom: 1px solid #1e2330; }
  .tab { flex: 1; padding: 12px; border: none; background: none; color: #6b7280; font-size: 13px; font-weight: 600; cursor: pointer; border-bottom: 2px solid transparent; }
  .tab.active { color: #3b82f6; border-bottom-color: #3b82f6; }

  .section-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
  .subsection-label { font-size: 10px; color: #4a5568; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }

  .flow-row { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-bottom: 1px solid #1e2330; }
  .flow-row:last-child { border-bottom: none; }
  .flow-icon-sm { width: 36px; height: 36px; background: #1e2330; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
  .run-btn { background: none; border: none; color: #4a5568; font-size: 16px; cursor: pointer; padding: 4px; }
  .run-btn:hover { color: #3b82f6; }

  .flow-detail-header { display: flex; gap: 14px; margin-bottom: 20px; }
  .flow-icon-lg { width: 56px; height: 56px; background: #1e2330; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; }
  .flow-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
  .step-row { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-bottom: 1px solid #1e2330; }
  .step-row:last-child { border-bottom: none; }
  .step-num-badge { width: 22px; height: 22px; border-radius: 50%; background: #1e2330; border: 1px solid #3b82f6; color: #3b82f6; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .step-icon { font-size: 18px; }

  .create-tabs { display: flex; background: #161a23; border-radius: 10px; padding: 3px; margin-bottom: 20px; }
  .create-tab { flex: 1; padding: 8px; border: none; background: none; color: #6b7280; font-size: 13px; border-radius: 8px; cursor: pointer; }
  .create-tab.active { background: #1e2330; color: #e2e8f0; }
  .create-section-label { font-size: 10px; color: #4a5568; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
  .template-category { display: flex; align-items: center; gap: 12px; padding: 12px; background: #161a23; border: 1px solid #1e2330; border-radius: 10px; margin-bottom: 8px; cursor: pointer; }
  .template-category:hover { background: #1e2330; }
  .cat-icon { font-size: 22px; }

  .cat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .cat-card { background: #161a23; border: 1px solid #1e2330; border-radius: 14px; padding: 20px 14px; text-align: center; cursor: pointer; transition: background 0.15s; }
  .cat-card:hover { background: #1e2330; }
  .cat-icon-lg { font-size: 32px; }

  .hist-tabs { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 12px; margin-bottom: 4px; }
  .status-tab { padding: 5px 12px; border-radius: 20px; border: 1px solid #1e2330; background: #161a23; color: #6b7280; font-size: 11px; white-space: nowrap; cursor: pointer; }
  .status-tab.active { background: #0f1e2b; border-color: #3b82f6; color: #3b82f6; }
</style>
