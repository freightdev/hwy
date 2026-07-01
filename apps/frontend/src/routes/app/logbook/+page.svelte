<script>
  import { onMount } from 'svelte';
  import { company, user } from '$lib/stores/app.js';
  import { api, info } from '$lib/stores/toast.js';
  import { get } from '$lib/api.js';

  let activeTab = 'overview';
  let companyData = null;
  let drivers = [];
  let loading = true;

  onMount(async () => {
    const [coRes, drRes] = await Promise.all([get('/company'), get('/drivers')]);
    if (coRes.data) companyData = coRes.data;
    if (drRes.data) drivers = drRes.data;
    loading = false;
  });

  const scoreFactors = [
    { label: 'Safety Compliance', score: 9.8 },
    { label: 'On-Time Performance', score: 9.3 },
    { label: 'Driver Satisfaction', score: 9.3 },
    { label: 'Load Completion Rate', score: 9.5 },
    { label: 'Document Accuracy', score: 9.2 },
    { label: 'Claims & Incidents', score: 8.7 },
    { label: 'Communication', score: 9.0 },
  ];

  const safetyItems = [
    { label: 'Preventable Accidents', val: 1 },
    { label: 'Non-Preventable Accidents', val: 1 },
    { label: 'Cargo Claims', val: 0 },
    { label: 'Total Claim Amount', val: '$3,250' },
    { label: 'Injuries', val: 0 },
    { label: 'Vehicle Out of Service', val: 2 },
  ];

  const safetyPrograms = [
    { label: 'Drug & Alcohol Program', status: 'Active' },
    { label: 'Driver Training Program', status: 'Active' },
    { label: 'Vehicle Maintenance Program', status: 'Active' },
    { label: 'Safety Meetings', status: 'Monthly' },
  ];

  const docList = [
    { name: 'Insurance Certificate', exp: 'June 15, 2025', status: 'Valid' },
    { name: 'Cargo Insurance', exp: 'June 15, 2025', status: 'Valid' },
    { name: 'BMC-84 Insurance', exp: 'June 15, 2025', status: 'Valid' },
    { name: 'Authority Letter', exp: 'Updated May 10, 2025', status: 'Valid' },
    { name: 'Safety Policy', exp: 'Updated May 1, 2025', status: 'Valid' },
  ];

  const reviews = [
    { name: 'David Brown', role: 'Driver', stars: 5, date: 'May 20, 2025', text: 'Great company to work with. Dispatch is professional and pays on time.' },
    { name: 'Sarah Johnson', role: 'Driver', stars: 5, date: 'May 16, 2025', text: 'Communication is excellent and loads are always what they say they are.' },
  ];

  $: mc = companyData?.mc || 'MC-1234567';
  $: dot = companyData?.dot || '3456789';
  $: companyName = companyData?.name || $company.name || 'Your Company LLC';
  $: driverCount = drivers.length || 32;

  function shareProfile() { api('Logbook profile sharing link'); }
  function editProfile() { info('Edit profile — go to More → Settings'); }
  function uploadDoc() { api('Document upload requires storage API'); }
  function viewSafetyDocs() { api('Safety document management requires API'); }
  function findConnections() { api('Carrier & broker search requires API'); }
</script>

<div class="page">
  <div class="page-header">
    <div class="hwy-logo" style="font-size:20px;font-weight:800">HWY <span style="color:#3b82f6">TMS</span></div>
    <div style="font-size:11px;color:#4a5568;margin-top:1px">{companyName}</div>
  </div>

  <div class="section">
    <div class="profile-card card">
      <div class="profile-header">
        <div class="company-logo">{companyName.charAt(0)}</div>
        <div style="flex:1">
          <div style="font-size:16px;font-weight:700">{companyName}</div>
          <div style="font-size:12px;color:#6b7280">{mc} • DOT {dot}</div>
          <span class="chip chip-green" style="margin-top:4px;font-size:10px">● Active</span>
        </div>
        <span class="chip chip-blue" style="font-size:10px">Company</span>
      </div>

      <div class="profile-actions">
        <button class="btn btn-secondary btn-sm" on:click={shareProfile}>🔗 Share Logbook</button>
        <button class="btn btn-secondary btn-sm" on:click={editProfile}>✏️ Edit Profile</button>
        <button class="btn btn-secondary btn-sm" on:click={() => info('More options')}>⋯ More</button>
      </div>

      <hr class="divider" />

      <div style="font-size:13px;color:#6b7280;margin-bottom:12px">
        Full service logistics and transportation company specializing in dry van, flatbed, and reefer freight across 48 states.
      </div>

      <div class="detail-grid">
        {#each [
          ['Company Type', companyData?.type || 'Motor Carrier'],
          ['Founded', companyData?.founded || 'May 18, 2018'],
          ['Headquarters', `${companyData?.city || 'Dallas'}, ${companyData?.state || 'TX'}`],
          ['Email', companyData?.email || $user.email || 'info@company.com'],
          ['Phone', companyData?.phone || '(214) 555-0196'],
        ] as [k, v]}
          <div class="detail-row">
            <span class="detail-key">{k}</span>
            <span class="detail-val">{v}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="section" style="padding-top:0">
    <div style="font-size:10px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Company Overview</div>
    <div class="stats-row">
      {#each [['Drivers', driverCount, 'Active'], ['Dispatchers', 6, 'Active'], ['Loads (YTD)', 124, ''], ['Revenue', '$241,550', '']] as [lbl, val, sub]}
        <div class="stat-box">
          <div class="stat-val" style="font-size:18px">{val}</div>
          <div class="stat-lbl">{lbl}{sub ? `\n${sub}` : ''}</div>
        </div>
      {/each}
    </div>
  </div>

  <div class="tabs">
    {#each [['overview','Profile'],['authority','Authority'],['safety','Safety'],['docs','Docs'],['reviews','Reviews']] as [k,label]}
      <button class="tab" class:active={activeTab===k} on:click={() => activeTab=k}>{label}</button>
    {/each}
  </div>

  {#if activeTab === 'overview'}
    <div class="section">
      <div class="score-card card" style="text-align:center;margin-bottom:16px">
        <div class="score-ring">
          <div class="score-num">9.4</div>
          <div class="score-label">Excellent</div>
        </div>
        <div style="font-size:12px;color:#6b7280;margin-top:8px">Top 8% of carriers</div>
        <div style="font-size:12px;color:#22c55e;margin-top:4px">+0.3 this month</div>
      </div>

      <div class="subsection-label" style="margin-bottom:10px">Score Factors</div>
      <div class="card" style="padding:12px">
        {#each scoreFactors as f}
          <div class="score-factor">
            <span style="font-size:13px;flex:1">{f.label}</span>
            <div class="score-bar-wrap">
              <div class="score-bar-fill" style="width:{(f.score/10)*100}%"></div>
            </div>
            <span style="font-size:13px;font-weight:700;color:#22c55e;width:30px;text-align:right">{f.score}</span>
          </div>
        {/each}
      </div>
    </div>

  {:else if activeTab === 'authority'}
    <div class="section">
      <div class="card" style="margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
          <span style="font-size:15px;font-weight:700">Operating Authority</span>
          <span class="chip chip-green">Active</span>
        </div>
        {#each [
          ['DOT Number', dot],
          ['USDOT Number', '11284969'],
          ['MC Number', mc],
          ['SCAC Code', companyData?.scac || 'CONL'],
          ['Operating States', companyData?.operating_states?.join(', ') || '48 States'],
          ['Authority Type', 'For-Hire Carrier'],
          ['Authority Status', 'Active'],
          ['Issued', '05/15/2018'],
        ] as [k, v]}
          <div class="detail-row">
            <span class="detail-key">{k}</span>
            <span class="detail-val">{v}</span>
          </div>
        {/each}
      </div>

      <div class="card">
        <div style="font-size:13px;font-weight:700;margin-bottom:12px">FMCSA Snapshot</div>
        <div class="sms-grid">
          {#each [['BLS Score','0.62','Good'],['OOS Rate','0.45','Good'],['Driver Time','0.14','Good'],['Dang.','0.0%','Good']] as [l,v,s]}
            <div class="sms-box">
              <div style="font-size:14px;font-weight:700">{v}</div>
              <div style="font-size:10px;color:#6b7280">{l}</div>
              <span class="chip chip-green" style="font-size:9px;margin-top:3px">{s}</span>
            </div>
          {/each}
        </div>
      </div>
    </div>

  {:else if activeTab === 'safety'}
    <div class="section">
      <div class="section-title-row">
        <span style="font-size:15px;font-weight:700">Safety Overview</span>
        <button class="btn btn-secondary btn-sm" on:click={viewSafetyDocs}>View Safety Docs</button>
      </div>

      <div class="card" style="margin-bottom:12px">
        <div class="subsection-label">Safety Breakdown (12 Months)</div>
        {#each safetyItems as item}
          <div class="detail-row">
            <span class="detail-key">{item.label}</span>
            <span class="detail-val">{item.val}</span>
          </div>
        {/each}
      </div>

      <div class="card">
        <div class="subsection-label">Safety Programs</div>
        {#each safetyPrograms as prog}
          <div class="detail-row">
            <span style="font-size:13px">✓ {prog.label}</span>
            <span class="chip chip-green" style="font-size:10px">{prog.status}</span>
          </div>
        {/each}
      </div>
    </div>

  {:else if activeTab === 'docs'}
    <div class="section">
      <div class="section-title-row">
        <span style="font-size:15px;font-weight:700">Documents</span>
        <button class="btn btn-primary btn-sm" on:click={uploadDoc}>+ Upload</button>
      </div>
      <div class="tabs-mini" style="margin-bottom:14px">
        {#each ['Company','Drivers','Equipment'] as t}
          <button class="tab-mini" class:active={t==='Company'}>{t}</button>
        {/each}
      </div>
      <div class="card" style="padding:0;overflow:hidden">
        {#each docList as doc}
          <div class="list-item">
            <span style="font-size:20px">📄</span>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{doc.name}</div>
              <div style="font-size:11px;color:#6b7280">{doc.exp}</div>
            </div>
            <span class="chip chip-green" style="font-size:10px">{doc.status}</span>
          </div>
        {/each}
      </div>
      <button class="btn btn-secondary btn-full" style="margin-top:12px" on:click={uploadDoc}>+ Upload Document</button>
    </div>

  {:else if activeTab === 'reviews'}
    <div class="section">
      <div class="review-summary card" style="text-align:center;margin-bottom:16px">
        <div style="font-size:36px;font-weight:800;color:#f59e0b">4.8</div>
        <div class="stars">★★★★★</div>
        <div style="font-size:12px;color:#6b7280;margin-top:4px">Based on 126 reviews</div>
        <div class="star-breakdown">
          {#each [['5 Stars', 104], ['4 Stars', 15], ['3 Stars', 5], ['2 Stars', 1], ['1 Star', 1]] as [l, n]}
            <div class="star-row">
              <span style="font-size:11px;width:50px;color:#6b7280">{l}</span>
              <div class="star-bar"><div class="star-fill" style="width:{(n/126)*100}%"></div></div>
              <span style="font-size:11px;width:20px;text-align:right;color:#6b7280">{n}</span>
            </div>
          {/each}
        </div>
      </div>
      {#each reviews as r}
        <div class="card" style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px">
            <div>
              <div style="font-size:13px;font-weight:600">{r.name}</div>
              <div style="font-size:11px;color:#6b7280">{r.role}</div>
            </div>
            <span style="font-size:11px;color:#6b7280">{r.date}</span>
          </div>
          <div style="color:#f59e0b;font-size:14px;margin-bottom:6px">{'★'.repeat(r.stars)}</div>
          <div style="font-size:13px;color:#9ca3af;line-height:1.5">{r.text}</div>
        </div>
      {/each}
      <button class="btn btn-secondary btn-full" on:click={() => api('View all reviews')}>View All Reviews</button>
    </div>
  {/if}
</div>

<style>
  .page-header { display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid #1e2330;position:sticky;top:0;background:#0d0f14;z-index:50; }
  .profile-header { display:flex;gap:12px;align-items:flex-start;margin-bottom:14px; }
  .company-logo { width:52px;height:52px;background:#1e3a5f;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:#3b82f6;flex-shrink:0; }
  .profile-actions { display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px; }
  .detail-grid { display:flex;flex-direction:column;gap:0; }
  .detail-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2330;font-size:13px; }
  .detail-row:last-child { border-bottom:none; }
  .detail-key { color:#6b7280; }
  .detail-val { font-weight:600;text-align:right;max-width:60%; }
  .stats-row { display:grid;grid-template-columns:repeat(4,1fr);gap:8px; }
  .tabs { display:flex;border-bottom:1px solid #1e2330;overflow-x:auto; }
  .tab { flex:1;padding:11px 4px;border:none;background:none;color:#6b7280;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap; }
  .tab.active { color:#3b82f6;border-bottom-color:#3b82f6; }
  .score-ring { width:100px;height:100px;border-radius:50%;border:4px solid #22c55e;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto; }
  .score-num { font-size:26px;font-weight:800;color:#22c55e; }
  .score-label { font-size:10px;color:#22c55e; }
  .score-factor { display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid #1e2330; }
  .score-factor:last-child { border-bottom:none; }
  .score-bar-wrap { flex:1;height:4px;background:#1e2330;border-radius:2px;overflow:hidden; }
  .score-bar-fill { height:100%;background:#22c55e;border-radius:2px; }
  .sms-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:8px; }
  .sms-box { background:#161a23;border:1px solid #1e2330;border-radius:10px;padding:10px 6px;text-align:center; }
  .section-title-row { display:flex;align-items:center;justify-content:space-between;margin-bottom:14px; }
  .subsection-label { font-size:10px;color:#4a5568;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;display:block; }
  .tabs-mini { display:flex;background:#161a23;border-radius:10px;padding:3px; }
  .tab-mini { flex:1;padding:7px;border:none;background:none;color:#6b7280;font-size:12px;border-radius:8px;cursor:pointer; }
  .tab-mini.active { background:#1e2330;color:#e2e8f0; }
  .review-summary { padding:20px; }
  .stars { color:#f59e0b;font-size:20px; }
  .star-breakdown { margin-top:12px;display:flex;flex-direction:column;gap:5px; }
  .star-row { display:flex;align-items:center;gap:8px; }
  .star-bar { flex:1;height:6px;background:#1e2330;border-radius:3px;overflow:hidden; }
  .star-fill { height:100%;background:#f59e0b;border-radius:3px; }
</style>
