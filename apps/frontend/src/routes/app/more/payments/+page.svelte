<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api, error as toastError } from '$lib/stores/toast.js';
  import { get } from '$lib/api.js';

  let activeTab = 'overview';
  let invoices = [];
  let payments = [];
  let stats = null;
  let loading = true;

  onMount(async () => {
    const [invRes, payRes, statRes] = await Promise.all([
      get('/invoices'),
      get('/invoices/payments'),
      get('/invoices/stats'),
    ]);
    if (invRes.data) invoices = invRes.data;
    else if (invRes.error) toastError(invRes.error);
    if (payRes.data) payments = payRes.data;
    if (statRes.data) stats = statRes.data;
    loading = false;
  });

  function statusColor(s) {
    if (s === 'Paid' || s === 'Received') return '#22c55e';
    if (s === 'Sent') return '#3b82f6';
    if (s === 'Overdue') return '#ef4444';
    return '#6b7280';
  }

  function createInvoice() { api('Invoice creation requires accounting API (QuickBooks/Stripe)'); }
  function viewInvoice(inv) { api(`Invoice ${inv.id} viewer requires storage API`); }
  function sendReminder(inv) { api(`Payment reminder for ${inv.id} requires email API`); }
  function exportStatement() { api('Statement export requires accounting API'); }
  function connectPayments() { api('Payment processing requires Stripe/PayPal integration'); }
</script>

<div class="page">
  <div class="page-header">
    <button class="back-btn" on:click={() => goto('/app/more')}>‹</button>
    <div class="page-title">Payments & Invoices</div>
    <button class="btn btn-primary btn-sm" on:click={createInvoice}>+ Invoice</button>
  </div>

  <div class="tabs">
    {#each [['overview','Overview'],['invoices','Invoices'],['payments','Payments'],['statements','Statements']] as [k,label]}
      <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
    {/each}
  </div>

  {#if activeTab === 'overview'}
    <div class="section">
      {#if loading}
        <div class="empty-state"><p>Loading...</p></div>
      {:else}
        <div class="rev-stats">
          <div class="rev-card">
            <div style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;margin-bottom:6px">Total Revenue (MTD)</div>
            <div style="font-size:28px;font-weight:800;color:#22c55e">{stats?.total_revenue_mtd || '$241,550'}</div>
            <div style="font-size:12px;color:#22c55e;margin-top:4px">↑ 15.8% vs last month</div>
          </div>
          <div class="rev-card">
            <div style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;margin-bottom:6px">Outstanding</div>
            <div style="font-size:28px;font-weight:800;color:#ef4444">{stats?.outstanding || '$67,890'}</div>
            <div style="font-size:12px;color:#ef4444;margin-top:4px">↑ 4.8% vs last month</div>
          </div>
        </div>

        <div class="card" style="margin-bottom:16px">
          <div style="font-size:13px;font-weight:700;margin-bottom:4px">Avg Net Rate (MTD)</div>
          <div style="font-size:22px;font-weight:800">$173,660</div>
          <div style="font-size:12px;color:#ef4444">Outstanding: $14,230</div>
        </div>

        <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;margin-bottom:10px">Recent Invoices</div>
        <div class="card" style="padding:0;overflow:hidden;margin-bottom:16px">
          {#each invoices.slice(0,4) as inv}
            <div class="inv-row" on:click={() => viewInvoice(inv)} role="button" tabindex="0">
              <div style="flex:1">
                <div style="font-size:13px;font-weight:600">{inv.id}</div>
                <div style="font-size:11px;color:#6b7280">{inv.broker_name}</div>
              </div>
              <div style="text-align:right">
                <div style="font-size:14px;font-weight:700">{inv.amount}</div>
                <span class="chip" style="font-size:10px;background:{statusColor(inv.status)}22;color:{statusColor(inv.status)}">{inv.status}</span>
              </div>
            </div>
          {/each}
        </div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-primary" style="flex:1" on:click={createInvoice}>+ New Invoice</button>
          <button class="btn btn-secondary" style="flex:1" on:click={() => activeTab='invoices'}>View All Invoices</button>
        </div>
      {/if}
    </div>

  {:else if activeTab === 'invoices'}
    <div class="section">
      {#if loading}
        <div class="empty-state"><p>Loading...</p></div>
      {:else}
        <div class="card" style="padding:0;overflow:hidden">
          {#each invoices as inv}
            <div class="inv-row" on:click={() => viewInvoice(inv)} role="button" tabindex="0">
              <div style="flex:1">
                <div style="font-size:13px;font-weight:600">{inv.id}</div>
                <div style="font-size:11px;color:#6b7280">{inv.broker_name} • {inv.date}</div>
              </div>
              <div style="display:flex;align-items:center;gap:10px">
                <div style="text-align:right">
                  <div style="font-size:14px;font-weight:700">{inv.amount}</div>
                  <span class="chip" style="font-size:10px;background:{statusColor(inv.status)}22;color:{statusColor(inv.status)}">{inv.status}</span>
                </div>
                {#if inv.status === 'Overdue'}
                  <button class="btn btn-danger btn-sm" on:click|stopPropagation={() => sendReminder(inv)}>Remind</button>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

  {:else if activeTab === 'payments'}
    <div class="section">
      <div class="card" style="padding:0;overflow:hidden;margin-bottom:16px">
        {#each payments as p}
          <div class="inv-row">
            <div class="pay-icon">💰</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{p.from_broker}</div>
              <div style="font-size:11px;color:#6b7280">{p.date} • {p.method}</div>
            </div>
            <div style="text-align:right">
              <div style="font-size:15px;font-weight:700;color:#22c55e">{p.amount}</div>
              <span class="chip chip-green" style="font-size:10px">{p.status}</span>
            </div>
          </div>
        {/each}
      </div>
      <button class="btn btn-secondary btn-full" on:click={connectPayments}>Connect Payment Processor</button>
    </div>

  {:else if activeTab === 'statements'}
    <div class="section">
      <div class="empty-state">
        <div class="icon">📊</div>
        <p>Monthly statements are generated automatically</p>
        <button class="btn btn-primary" style="margin-top:16px" on:click={exportStatement}>Export Statement</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .back-btn { background:none;border:none;color:#3b82f6;font-size:24px;cursor:pointer; }
  .tabs { display:flex;border-bottom:1px solid #1e2330; }
  .tab { flex:1;padding:11px;border:none;background:none;color:#6b7280;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .rev-stats { display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:16px; }
  .rev-card { background:#161a23;border:1px solid #1e2330;border-radius:14px;padding:14px; }
  .inv-row { display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid #1e2330;cursor:pointer; }
  .inv-row:hover { background:#161a23; }
  .inv-row:last-child { border-bottom:none; }
  .pay-icon { width:36px;height:36px;background:#1e2330;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
</style>
