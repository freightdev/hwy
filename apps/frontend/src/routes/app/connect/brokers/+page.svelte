<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api, success, error as toastError } from '$lib/stores/toast.js';
  import { get, post } from '$lib/api.js';

  let search = '';
  let activeTab = 'all';
  let selectedBroker = null;
  let brokers = [];
  let loading = true;

  onMount(async () => {
    const res = await get('/brokers');
    if (res.error) toastError(res.error);
    else brokers = res.data;
    loading = false;
  });

  $: filtered = brokers.filter(b =>
    b.name.toLowerCase().includes(search.toLowerCase()) &&
    (activeTab === 'all' || (activeTab === 'favorites' && b.favorite) || (activeTab === 'active' && b.status === 'Active'))
  );

  function statusColor(s) {
    if (s === 'Active') return '#22c55e';
    if (s === 'Improving') return '#f59e0b';
    return '#6b7280';
  }

  async function toggleFavorite(b) {
    const res = await post(`/brokers/${b.id}/favorite`);
    if (res.error) { toastError(res.error); return; }
    brokers = brokers.map(bro => bro.id === b.id ? res.data : bro);
    success(res.data.favorite ? `${b.name} added to favorites` : `${b.name} removed from favorites`);
  }

  function callBroker(b) { api(`VoIP call to ${b.name}`); }
  function emailBroker(b) { api(`Email to ${b.name}`); }
  function messageBroker(b) { api(`Message to ${b.name}`); }
  function requestLoad(b) { api(`Load request to ${b.name} requires broker API`); }
  function viewDocs(b) { api(`${b.name} documents require storage API`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => selectedBroker ? selectedBroker = null : goto('/app/connect')}>‹</button>
    <div>
      <div class="page-title">{selectedBroker ? selectedBroker.name : 'Brokers'}</div>
      <div style="font-size:11px;color:#4a5568">{selectedBroker ? (selectedBroker.status === 'Active' ? '● Active' : selectedBroker.status) : `${brokers.length} Connected Brokers`}</div>
    </div>
    {#if !selectedBroker}
      <div style="display:flex;gap:8px">
        <button class="icon-btn-sm" on:click={() => api('Filter brokers')}>⊟</button>
        <button class="btn btn-primary btn-sm" on:click={() => api('Find new brokers')}>+ Find</button>
      </div>
    {:else}
      <button class="fav-btn" on:click={() => toggleFavorite(selectedBroker)}>{selectedBroker.favorite ? '★' : '☆'}</button>
    {/if}
  </div>

  {#if selectedBroker}
    <div class="section">
      <div class="broker-hero card" style="margin-bottom:12px">
        <div class="broker-avatar-lg">{selectedBroker.name.charAt(0)}</div>
        <div style="font-size:18px;font-weight:700;margin-top:12px">{selectedBroker.name}</div>
        <div style="font-size:13px;color:#6b7280">{selectedBroker.mc}</div>
        <div style="margin-top:6px"><span style="font-size:12px;color:#3b82f6">{selectedBroker.website}</span></div>
        <span class="chip" style="margin-top:8px;background:{statusColor(selectedBroker.status)}22;color:{statusColor(selectedBroker.status)}">● {selectedBroker.status}</span>
      </div>

      <div class="broker-actions">
        <button class="action-btn" on:click={() => callBroker(selectedBroker)}>📞<span>Call</span></button>
        <button class="action-btn" on:click={() => emailBroker(selectedBroker)}>📧<span>Email</span></button>
        <button class="action-btn" on:click={() => messageBroker(selectedBroker)}>💬<span>Message</span></button>
        <button class="action-btn" on:click={() => requestLoad(selectedBroker)}>📦<span>Load Board</span></button>
      </div>

      <div class="perf-stats" style="margin-bottom:12px">
        {#each [['Total Loads', selectedBroker.loads],['On-Time Rate', selectedBroker.on_time+'%'],['Total Revenue', selectedBroker.revenue],['Rating', selectedBroker.rating+'★']] as [l,v]}
          <div class="stat-box"><div class="stat-val" style="font-size:16px">{v}</div><div class="stat-lbl">{l}</div></div>
        {/each}
      </div>

      <div class="card" style="margin-bottom:12px">
        <div style="font-size:12px;color:#4a5568;font-weight:700;margin-bottom:10px">CREDIT & DOCS</div>
        {#each [
          ['Credit Limit', selectedBroker.credit],
          ['Available', selectedBroker.available],
          ['Authority', selectedBroker.authority ? '✓ Verified' : '✕ Not Verified'],
          ['Insurance', selectedBroker.insurance ? '✓ Valid' : '✕ Not Verified'],
        ] as [k,v]}
          <div class="detail-row">
            <span style="color:#6b7280;font-size:13px">{k}</span>
            <span style="font-size:13px;font-weight:600;color:{v.startsWith('✓') ? '#22c55e' : v.startsWith('✕') ? '#ef4444' : '#e2e8f0'}">{v}</span>
          </div>
        {/each}
      </div>

      <button class="btn btn-primary btn-full" on:click={() => requestLoad(selectedBroker)}>Request Load</button>
      <button class="btn btn-secondary btn-full" style="margin-top:8px" on:click={() => viewDocs(selectedBroker)}>View Documents</button>
    </div>

  {:else}
    <div class="tabs">
      {#each [['all',`All (${brokers.length})`],['active','Active'],['favorites','Favorites']] as [k,label]}
        <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
      {/each}
    </div>

    <div class="search-bar">
      <span>🔍</span>
      <input bind:value={search} placeholder="Search brokers..." />
    </div>

    <div class="card" style="margin:0 16px;padding:0;overflow:hidden">
      {#if loading}
        <div class="empty-state"><p>Loading brokers...</p></div>
      {:else}
        {#each filtered as b}
          <div class="list-item broker-row" on:click={() => selectedBroker = b} role="button" tabindex="0" style="cursor:pointer">
            <div class="broker-icon">{b.name.charAt(0)}</div>
            <div style="flex:1;min-width:0">
              <div style="display:flex;align-items:center;gap:6px">
                <span style="font-size:13px;font-weight:600">{b.name}</span>
                {#if b.favorite}<span style="color:#f59e0b;font-size:12px">★</span>{/if}
              </div>
              <div style="font-size:11px;color:#6b7280">{b.mc}</div>
              <div style="font-size:11px;margin-top:2px">
                <span style="color:{statusColor(b.status)}">● {b.status}</span>
                <span style="color:#4a5568;margin-left:8px">Loads: {b.loads}</span>
                <span style="color:#4a5568;margin-left:8px">{b.on_time}% OT</span>
              </div>
            </div>
            <div style="text-align:right">
              <div style="font-size:13px;font-weight:700;color:#22c55e">{b.revenue}</div>
              <div style="font-size:11px;color:#f59e0b">{b.rating}★</div>
            </div>
          </div>
        {/each}
        {#if filtered.length === 0}
          <div class="empty-state"><div class="icon">🤝</div><p>No brokers found</p></div>
        {/if}
      {/if}
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .fav-btn { background:none;border:none;color:#f59e0b;font-size:22px;cursor:pointer; }
  .icon-btn-sm { background:#161a23;border:1px solid #1e2330;border-radius:7px;padding:6px 9px;font-size:13px;cursor:pointer; }
  .tabs { display:flex;border-bottom:1px solid #1e2330; }
  .tab { flex:1;padding:11px;border:none;background:none;color:#6b7280;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .broker-icon { width:38px;height:38px;border-radius:10px;background:#1e3a5f;color:#3b82f6;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;flex-shrink:0; }
  .broker-hero { text-align:center;padding:24px 16px; }
  .broker-avatar-lg { width:72px;height:72px;border-radius:20px;background:#1e3a5f;color:#3b82f6;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;margin:0 auto; }
  .broker-actions { display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px; }
  .action-btn { background:#161a23;border:1px solid #1e2330;border-radius:12px;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;font-size:18px;cursor:pointer; }
  .action-btn span { font-size:11px;color:#6b7280; }
  .perf-stats { display:grid;grid-template-columns:repeat(4,1fr);gap:8px; }
  .detail-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2330; }
  .detail-row:last-child { border-bottom:none; }
</style>
