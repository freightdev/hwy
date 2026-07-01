<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api, success, error as toastError } from '$lib/stores/toast.js';
  import { get, post } from '$lib/api.js';

  let search = '';
  let activeTab = 'all';
  let selectedLoad = null;
  let showFilters = false;
  let loads = [];
  let loading = true;

  onMount(async () => {
    const res = await get('/loads');
    if (res.error) toastError(res.error);
    else loads = res.data;
    loading = false;
  });

  $: filtered = loads.filter(l =>
    (l.route.toLowerCase().includes(search.toLowerCase()) ||
     l.broker_name.toLowerCase().includes(search.toLowerCase())) &&
    (activeTab === 'all' ||
     (activeTab === 'saved' && false) ||
     (activeTab === 'posted' && false))
  );

  async function bookLoad(l) {
    const res = await post(`/loads/${l.id}/book`);
    if (res.error) { api(res.error); return; }
    success(`Load ${l.id} booked`);
  }
  function saveLoad(l) { success(`${l.id} saved to favorites`); }
  function contactBroker(l) { api(`Direct contact with ${l.broker_name} requires messaging API`); }
  function postLoad() { api('Load posting requires carrier/broker API integration'); }
  function rateCheck(l) { api(`Rate check for ${l.route} requires DAT/Truckstop API`); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/connect')}>‹</button>
    <div>
      <div class="page-title">Load Board</div>
      <div style="font-size:11px;color:#4a5568">Connected Board</div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="icon-btn-sm" on:click={() => showFilters = !showFilters}>⊟</button>
      <button class="btn btn-primary btn-sm" on:click={postLoad}>+ Post Load</button>
    </div>
  </div>

  {#if showFilters}
    <div class="filters-bar">
      <button class="filter-chip" on:click={() => api('Equipment filter')}>Equipment ›</button>
      <button class="filter-chip" on:click={() => api('Rate filter')}>Rate ›</button>
      <button class="filter-chip" on:click={() => api('Miles filter')}>Miles ›</button>
      <button class="filter-chip" on:click={() => api('Date filter')}>Date ›</button>
      <button class="filter-chip" on:click={() => api('Broker filter')}>Broker ›</button>
    </div>
  {/if}

  <div class="tabs">
    {#each [['all','All Loads'],['saved','Saved (0)'],['posted','Posted (0)']] as [k,label]}
      <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
    {/each}
  </div>

  <div class="search-bar">
    <span>🔍</span>
    <input bind:value={search} placeholder="Search loads, brokers, routes..." />
  </div>

  {#if selectedLoad}
    <div class="section">
      <div class="load-detail card" style="margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px">
          <div>
            <div style="font-size:16px;font-weight:700">{selectedLoad.route}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:3px">{selectedLoad.date} • {selectedLoad.equipment}</div>
          </div>
          <div style="text-align:right">
            <div style="font-size:20px;font-weight:800;color:#22c55e">{selectedLoad.rate}</div>
            <div style="font-size:11px;color:#6b7280">{selectedLoad.rpm}/mi</div>
          </div>
        </div>

        <div class="load-stats">
          {#each [['Miles', selectedLoad.miles],['Stops', selectedLoad.stops],['Weight', selectedLoad.weight]] as [l,v]}
            <div class="stat-box"><div class="stat-val">{v}</div><div class="stat-lbl">{l}</div></div>
          {/each}
        </div>

        <hr class="divider" />
        {#each [
          ['Pickup', `${selectedLoad.pickup} — ${selectedLoad.pickup_location}`],
          ['Delivery', `${selectedLoad.delivery} — ${selectedLoad.delivery_location}`],
          ['Broker', selectedLoad.broker_name],
          ['MC#', selectedLoad.mc],
          ['Equipment', selectedLoad.equipment],
        ] as [k,v]}
          <div class="detail-row"><span class="detail-key">{k}</span><span class="detail-val">{v}</span></div>
        {/each}
      </div>

      <div style="display:flex;gap:8px;margin-bottom:10px">
        <button class="btn btn-secondary" style="flex:1" on:click={() => rateCheck(selectedLoad)}>📊 Rate Check</button>
        <button class="btn btn-secondary" style="flex:1" on:click={() => saveLoad(selectedLoad)}>★ Save</button>
        <button class="btn btn-secondary" style="flex:1" on:click={() => contactBroker(selectedLoad)}>💬 Contact</button>
      </div>
      <button class="btn btn-primary btn-full" style="margin-bottom:10px" on:click={() => bookLoad(selectedLoad)}>Book This Load</button>
      <button class="btn btn-secondary btn-full" on:click={() => selectedLoad = null}>← Back to Board</button>
    </div>

  {:else}
    <div style="padding:0 16px 16px">
      {#if loading}
        <div class="empty-state"><p>Loading loads...</p></div>
      {:else}
        {#each filtered as l}
          <div class="load-card card" on:click={() => selectedLoad = l} role="button" tabindex="0">
            <div class="load-top">
              <div style="flex:1;min-width:0">
                <div class="load-route">{l.route}</div>
                <div class="load-meta">{l.date} • {l.equipment} • {l.broker_name}</div>
              </div>
              <div style="text-align:right;flex-shrink:0">
                <div class="load-rate">{l.rate}</div>
                <div style="font-size:11px;color:#6b7280">{l.rpm}/mi</div>
              </div>
            </div>
            <div class="load-bottom">
              <span class="load-tag">{l.miles} mi</span>
              <span class="load-tag">{l.weight}</span>
              <span class="load-tag">{l.stops} stop{l.stops > 1 ? 's' : ''}</span>
              <button class="btn btn-primary btn-sm" style="margin-left:auto" on:click|stopPropagation={() => bookLoad(l)}>Book</button>
            </div>
          </div>
        {/each}
        {#if filtered.length === 0}
          <div class="empty-state"><div class="icon">📦</div><p>No loads match your search</p></div>
        {/if}
      {/if}
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .icon-btn-sm { background:#161a23;border:1px solid #1e2330;border-radius:7px;padding:6px 9px;font-size:13px;cursor:pointer; }
  .filters-bar { display:flex;gap:8px;overflow-x:auto;padding:10px 16px;border-bottom:1px solid #1e2330; }
  .filter-chip { padding:5px 12px;border-radius:20px;border:1px solid #2d3548;background:#161a23;color:#9ca3af;font-size:12px;white-space:nowrap;cursor:pointer; }
  .filter-chip:hover { border-color:#3b82f6;color:#3b82f6; }
  .tabs { display:flex;border-bottom:1px solid #1e2330; }
  .tab { flex:1;padding:11px;border:none;background:none;color:#6b7280;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .load-card { margin-bottom:10px;cursor:pointer;transition:border-color 0.15s; }
  .load-card:hover { border-color:#3b82f6; }
  .load-top { display:flex;gap:12px;align-items:flex-start;margin-bottom:10px; }
  .load-route { font-size:14px;font-weight:700; }
  .load-meta { font-size:11px;color:#6b7280;margin-top:3px; }
  .load-rate { font-size:18px;font-weight:800;color:#22c55e; }
  .load-bottom { display:flex;align-items:center;gap:6px;flex-wrap:wrap; }
  .load-tag { padding:3px 9px;border-radius:20px;background:#1e2330;color:#9ca3af;font-size:11px; }
  .load-stats { display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px; }
  .detail-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2330;font-size:13px; }
  .detail-row:last-child { border-bottom:none; }
  .detail-key { color:#6b7280; }
  .detail-val { font-weight:600;text-align:right; }
</style>
