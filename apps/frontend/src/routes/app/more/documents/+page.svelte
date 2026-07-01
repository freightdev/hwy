<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api, error as toastError } from '$lib/stores/toast.js';
  import { get } from '$lib/api.js';

  let activeTab = 'all';
  let search = '';
  let documents = [];
  let loading = true;

  onMount(async () => {
    const res = await get('/documents');
    if (res.error) toastError(res.error);
    else documents = res.data;
    loading = false;
  });

  const categories = [
    { name: 'Authority & Compliance', count: 10, icon: '⚖️', color: '#3b82f6' },
    { name: 'Insurance', count: 8, icon: '🛡️', color: '#22c55e' },
    { name: 'Contracts', count: 15, icon: '📝', color: '#8b5cf6' },
    { name: 'Permits & Licenses', count: 6, icon: '📋', color: '#f59e0b' },
    { name: 'Safety & Policies', count: 9, icon: '⚠️', color: '#ef4444' },
    { name: 'Tax & Finance', count: 12, icon: '💰', color: '#06b6d4' },
    { name: 'Other', count: 4, icon: '📁', color: '#6b7280' },
  ];

  const popular = [
    { name: 'How to Create a Load', sub: 'Step by step guide', icon: '📦' },
    { name: 'Driver Setup Guide', sub: 'Onboard new drivers', icon: '🚛' },
    { name: 'IFTA Filing Guide', sub: 'How to file IFTA taxes', icon: '📋' },
    { name: 'Rate Confirmation Template', sub: 'Standard rate con template', icon: '📄' },
    { name: 'Broker Setup Guide', sub: 'Connect with brokers', icon: '🤝' },
    { name: 'Track & Logbook', sub: 'Logbook requirements and updates', icon: '📒' },
  ];

  $: filtered = documents.filter(d =>
    d.name.toLowerCase().includes(search.toLowerCase()) &&
    (activeTab === 'all' || d.category.toLowerCase().includes(activeTab))
  );

  let showKnowledge = false;

  function uploadDoc() { api('Document upload requires cloud storage API (S3/GCS)'); }
  function openDoc(d) { api(`Document viewer requires file storage API for: ${d.name}`); }
  function downloadDoc(d) { api(`Download requires storage API for: ${d.name}`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/more')}>‹</button>
    <div>
      <div class="page-title">Documents</div>
      <div style="font-size:11px;color:#4a5568">AI-Powered Knowledge</div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="icon-btn-sm" on:click={() => showKnowledge = !showKnowledge}>🔍</button>
      <button class="icon-btn-sm" on:click={() => api('Filter documents')}>⊟</button>
    </div>
  </div>

  {#if showKnowledge}
    <div class="section">
      <div class="search-bar" style="margin:0 0 16px">
        <span>🔍</span>
        <input placeholder="Search docs, guides, templates..." />
      </div>
      <div class="kb-tabs">
        {#each ['All','Company','Trucking','FMCSA','Templates'] as t}
          <button class="kb-tab" class:active={t==='All'}>{t}</button>
        {/each}
      </div>
      <div style="font-size:12px;color:#4a5568;font-weight:700;text-transform:uppercase;margin-bottom:10px">Popular</div>
      <div class="card" style="padding:0;overflow:hidden">
        {#each popular as p}
          <div class="list-item" on:click={() => api(`Knowledge base: ${p.name}`)} role="button" tabindex="0" style="cursor:pointer">
            <div class="doc-icon" style="background:#1e2330">{p.icon}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{p.name}</div>
              <div style="font-size:11px;color:#6b7280">{p.sub}</div>
            </div>
            <span style="color:#4a5568">›</span>
          </div>
        {/each}
      </div>
      <div class="ask-codriver card" style="margin-top:16px">
        <div style="font-size:13px;font-weight:600;margin-bottom:8px">✦ Ask CoDriver</div>
        <input placeholder="Ask anything about trucking, docs, or regulations..." style="margin-bottom:8px" on:keydown={(e)=>e.key==='Enter'&&goto('/app/ai')} />
        <button class="btn btn-primary btn-sm btn-full" on:click={() => goto('/app/ai')}>Ask AI Assistant</button>
      </div>
    </div>
  {:else}
    <div class="tabs">
      {#each [['all','All'],['company','Company'],['driver','Drivers'],['equipment','Equipment'],['expired','Expired']] as [k,label]}
        <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
      {/each}
    </div>

    <div class="search-bar">
      <span>🔍</span>
      <input bind:value={search} placeholder="Search documents..." />
    </div>

    <div class="section" style="padding-top:8px">
      <div style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Categories</div>
      <div class="cat-scroll">
        {#each categories as cat}
          <button class="cat-chip" style="border-color:{cat.color}33;color:{cat.color}" on:click={() => api(`${cat.name} documents`)}>
            {cat.icon} {cat.name} ({cat.count})
          </button>
        {/each}
      </div>
    </div>

    <div class="section" style="padding-top:0">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <span style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em">Documents ({filtered.length})</span>
        <button class="btn btn-primary btn-sm" on:click={uploadDoc}>+ Upload Document</button>
      </div>
      <div class="card" style="padding:0;overflow:hidden">
        {#if loading}
          <div class="empty-state"><p>Loading documents...</p></div>
        {:else}
          {#each filtered as doc}
            <div class="doc-row">
              <div class="doc-icon">{doc.icon}</div>
              <div style="flex:1;min-width:0;cursor:pointer" on:click={() => openDoc(doc)} role="button" tabindex="0">
                <div style="font-size:13px;font-weight:600">{doc.name}</div>
                <div style="font-size:11px;color:#6b7280">{doc.category} • {doc.expiry || 'No expiry'} • {doc.size}</div>
              </div>
              <div style="display:flex;align-items:center;gap:6px">
                <span class="chip chip-green" style="font-size:10px">{doc.status}</span>
                <button class="icon-sm" on:click={() => downloadDoc(doc)}>↓</button>
              </div>
            </div>
          {/each}
          {#if filtered.length === 0}
            <div class="empty-state"><div class="icon">📄</div><p>No documents found</p></div>
          {/if}
        {/if}
      </div>
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
  .cat-scroll { display:flex;gap:8px;overflow-x:auto;padding-bottom:4px; }
  .cat-chip { padding:6px 12px;border-radius:20px;border:1px solid;background:transparent;font-size:12px;white-space:nowrap;cursor:pointer; }
  .doc-row { display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid #1e2330; }
  .doc-row:last-child { border-bottom:none; }
  .doc-icon { width:36px;height:36px;background:#1e2330;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
  .icon-sm { background:#1e2330;border:none;border-radius:6px;padding:5px 8px;font-size:13px;cursor:pointer; }
  .kb-tabs { display:flex;gap:6px;overflow-x:auto;padding-bottom:12px;margin-bottom:8px; }
  .kb-tab { padding:5px 14px;border-radius:20px;border:1px solid #1e2330;background:#161a23;color:#6b7280;font-size:12px;cursor:pointer; }
  .kb-tab.active { background:#0f1e2b;border-color:#3b82f6;color:#3b82f6; }
  .ask-codriver { background:#0f1e2b;border-color:#3b82f640; }
</style>
