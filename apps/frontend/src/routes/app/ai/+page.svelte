<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { api, info, success } from '$lib/stores/toast.js';
  import { get as apiGet, post as apiPost } from '$lib/api.js';
  import { company, user } from '$lib/stores/app.js';

  let activeView = 'hub'; // hub | chat | agents | models | settings | flows | toolaccess
  let chatTab = 'chats'; // chats | pinned | history
  let chatInput = '';
  let listening = false;
  let listenTimer = null;
  let loading = false;
  let activeExecution = null;
  let activeActor = null;
  let flowStatus = 'idle';
  let timelineEvents = [];
  let recentLogbooks = [];
  let runtimeStatus = null;
  let lastError = '';

  let messages = [
    { role: 'assistant', content: `Hey! I'm CoDriver — your AI dispatch pilot. I can find loads, check drivers, handle paperwork, negotiate rates, and run your whole operation. What do you need?`, pinned: false }
  ];

  let pinnedMessages = [];

  const chatHistory = [
    { id: 1, title: 'Lead Update', sub: 'Find me a load from Dallas to Atlanta.', time: '5:32 AM', unread: false },
    { id: 2, title: 'Driver Check', sub: 'Which driver is closest to delivery...', time: '5:41 AM', unread: false },
    { id: 3, title: 'Rate Negotiation', sub: 'Help me negotiate this rate...', time: 'Yesterday', unread: false },
    { id: 4, title: 'IFTA Question', sub: 'How do I file IFTA in New York?', time: 'Yesterday', unread: false },
    { id: 5, title: 'Broker Setup', sub: 'Onboarding as a new broker...', time: 'May 23', unread: false },
    { id: 6, title: 'Maintenance', sub: 'Remind me about truck #103 PM...', time: 'May 19', unread: false },
    { id: 7, title: 'Fuel Prices', sub: 'Where did fuel sheep diesel in TMP', time: 'May 18', unread: false },
    { id: 8, title: 'Documents', sub: 'Create a contract template...', time: 'May 17', unread: false },
  ];

  const quickActions = [
    { label: 'Find Load', icon: '📦', prompt: 'Find me a good load from Dallas, TX to Atlanta, GA for tomorrow' },
    { label: 'Check Driver', icon: '🚛', prompt: 'Which driver is closest to delivery right now?' },
    { label: 'Send Update', icon: '📡', prompt: 'Send a status update to all drivers in transit' },
    { label: 'Rate Check', icon: '💰', prompt: 'What is a good rate per mile for dry van Dallas to Atlanta?' },
  ];

  let myFlows = [
    { id: 1, name: 'Post-Load Workflow', steps: 7, type: 'Auto', enabled: true, icon: '📦', desc: 'Create load, set rate, send outboard, and notify all drivers, jobs, tasks' },
    { id: 2, name: 'New Driver Onboarding', steps: 8, type: 'Auto', enabled: true, icon: '👤', desc: 'Add driver, doc, setup, verify each' },
    { id: 3, name: 'Invoice & Docs Flow', steps: 5, type: 'Auto', enabled: false, icon: '📄', desc: 'Set rate, confirm, send invoice with payment' },
    { id: 4, name: 'POD Collection Flow', steps: 4, type: 'Auto', enabled: true, icon: '📋', desc: 'Collect POD, verify, update load' },
    { id: 5, name: 'Fuel Receipt Flow', steps: 3, type: 'Auto', enabled: false, icon: '⛽', desc: 'Collect, verify, match to load' },
  ];

  const agents = [
    { name: 'CoDriver', sub: 'Main dispatch assistant', status: 'Online', color: '#22c55e', default: true, icon: '✦' },
    { name: 'Rate Analyst', sub: 'Find and analyze best rates', status: 'Online', color: '#22c55e', icon: '📊' },
    { name: 'Doc Helper', sub: 'Documents and compliance', status: 'Online', color: '#22c55e', icon: '📄' },
    { name: 'Driver Coordinator', sub: 'Driver communication & updates', status: 'Online', color: '#22c55e', icon: '🚛' },
    { name: 'Maintenance Bot', sub: 'Maintenance & inspections', status: 'Away', color: '#f59e0b', icon: '🔧' },
  ];

  const availableAgents = [
    { name: 'Safety Monitor', sub: 'Monitor safety & violations', icon: '⚠️' },
    { name: 'Weather Watcher', sub: 'Weather & route alerts', icon: '🌦️' },
    { name: 'Fuel Finder', sub: 'Find the best fuel prices', icon: '⛽' },
  ];

  let models = [
    { name: 'GPT-4o', sub: 'OpenAI', desc: 'Best for reasoning, complex tasks', active: true },
    { name: 'Claude 3.5 Sonnet', sub: 'Anthropic', desc: 'Excellent for analysis, writing', active: false },
    { name: 'Gemini 1.5 Pro', sub: 'Google', desc: 'Best for long context, multimodal', active: false },
    { name: 'Llama 3 7B', sub: 'Meta', desc: 'Best for threads, self-hosted', active: false },
    { name: 'CoDriver Lite', sub: 'HWY AI', desc: 'Fast and optimized for trucking', active: false },
  ];

  let toolAccess = [
    { name: 'Load Board', sub: 'Search and post loads', enabled: true },
    { name: 'Drivers', sub: 'View and manage drivers', enabled: true },
    { name: 'Documents', sub: 'Create and manage documents', enabled: true },
    { name: 'Messages', sub: 'Send and read messages', enabled: true },
    { name: 'Payments', sub: 'View and manage payments', enabled: false },
    { name: 'Reports', sub: 'Generate runs and reports', enabled: false },
    { name: 'Integrations', sub: 'Access third-party tools', enabled: true },
  ];

  // Hub orbit items
  const hubItems = [
    { label: 'Chat', icon: '💬', sub: 'Talk with AI', view: 'chat', angle: -90 },
    { label: 'Docs', icon: '📄', sub: 'Find answers', view: null, action: () => goto('/app/more/documents'), angle: -30 },
    { label: 'Flows', icon: '⚡', sub: 'Run workflows', view: 'flows', angle: 30 },
    { label: 'Settings', icon: '⚙️', sub: 'AI preferences', view: 'settings', angle: 90 },
    { label: 'Models', icon: '🧠', sub: 'AI models', view: 'models', angle: 150 },
    { label: 'Agents', icon: '👥', sub: 'AI team', view: 'agents', angle: 210 },
  ];

  function hubNav(item) {
    if (item.action) item.action();
    else activeView = item.view;
  }

  function startListening() {
    listening = true;
    listenTimer = setTimeout(() => {
      listening = false;
      api('Voice input requires microphone API');
    }, 3000);
  }
  function stopListening() {
    listening = false;
    clearTimeout(listenTimer);
  }

  function releaseToStop() {
    listening = false;
    api('Voice processed — CoDriver AI voice requires API');
  }

  onMount(async () => {
    const status = await apiGet('/codriver/runtime/status');
    if (status.data) runtimeStatus = status.data;
  });

  async function refreshRuntimePanels(executionId) {
    const [status, logbooks] = await Promise.all([
      apiGet('/codriver/runtime/status'),
      apiGet('/codriver/logbooks/recent'),
    ]);
    if (status.data) runtimeStatus = status.data;
    if (logbooks.data?.entries) recentLogbooks = logbooks.data.entries;
    if (executionId) {
      const timeline = await apiGet(`/codriver/executions/${executionId}/timeline`);
      if (timeline.data?.events) timelineEvents = timeline.data.events;
    }
  }

  async function sendMessage() {
    if (!chatInput.trim() || loading) return;
    const msg = chatInput.trim();
    chatInput = '';
    lastError = '';
    messages = [...messages, { role: 'user', content: msg, pinned: false }];
    loading = true;

    const response = await apiPost('/codriver/chat/send', {
      message: msg,
      session_id: 'hwy-tms-ai-tab',
      user_id: user?.id ? String(user.id) : 'dev-user',
      payload: { source: 'hwy-tms-ai-tab' }
    });

    if (response.error) {
      lastError = response.error;
      messages = [...messages, { role: 'assistant', content: `CoDriver runtime unavailable: ${response.error}`, pinned: false }];
      flowStatus = 'error';
      loading = false;
      return;
    }

    const data = response.data || {};
    activeExecution = data.execution_id || null;
    activeActor = data.actor || null;
    flowStatus = data.flow_status || 'answered';
    timelineEvents = data.timeline || [];
    recentLogbooks = data.logbook_entries || [];
    messages = [...messages, { role: 'assistant', content: data.response || 'CoDriver returned no response text.', pinned: false }];
    await refreshRuntimePanels(activeExecution);
    loading = false;
  }

  function getResponse(msg) {
    const l = msg.toLowerCase();
    if (l.includes('load') && (l.includes('dallas') || l.includes('find') || l.includes('atlanta'))) {
      return `I found 3 great loads for you leaving Dallas, TX tomorrow:\n\n• Dallas, TX → Atlanta, GA — $2,450 — 53' Dry Van — Pickup 7:00 AM — Landstar\n• Dallas, TX → Nashville, TN — $2,100 — Flatbed — Pickup 9:00 AM — TQL\n• Dallas, TX → Memphis, TN — $1,850 — Dry Van — Pickup 6:30 AM — DAT\n\nWant me to book one or get more details?`;
    }
    if (l.includes('rate')) return `Current market rate for Dry Van Dallas → Atlanta is $2.15–$2.45/mile. That lane is hot right now — I'd push for $2.40 minimum. Want me to run a full rate analysis?`;
    if (l.includes('driver') || l.includes('status')) return `Fleet status right now:\n\n🔵 In Transit: 27 drivers\n🟡 At Pickup: 3 drivers\n🟣 At Delivery: 2 drivers\n🟢 Available: 4 drivers\n\nNo critical alerts. Everything looks clean.`;
    if (l.includes('update') || l.includes('send')) return `I'll draft a message to all in-transit drivers. Want me to include ETA reminders and weather alerts for their routes?`;
    return `Got it. To fully execute this with live data, CoDriver needs to be connected to your backend API. I can help with load searches, driver tracking, rate analysis, document generation, invoice creation, and more. What would you like to focus on?`;
  }

  function pinMessage(idx) {
    messages[idx].pinned = !messages[idx].pinned;
    messages = [...messages];
    success(messages[idx].pinned ? 'Message pinned' : 'Message unpinned');
  }

  function usePrompt(p) { chatInput = p.prompt; sendMessage(); }
  function handleKey(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }
  function openHistory(h) { info(`Loading conversation: ${h.title}`); }
  function toggleTool(i) { toolAccess[i].enabled = !toolAccess[i].enabled; toolAccess = [...toolAccess]; success(`${toolAccess[i].name} ${toolAccess[i].enabled ? 'enabled' : 'disabled'}`); }
  function toggleFlow(id) { const f = myFlows.find(f=>f.id===id); if(f){ f.enabled=!f.enabled; success(`${f.name} ${f.enabled?'enabled':'disabled'}`); } myFlows = [...myFlows]; }
  function activateModel(name) { models.forEach(m => m.active = m.name === name); success(`Switched to ${name}`); }
</script>

<div class="page ai-page">

  <!-- TOP BAR -->
  <div class="ai-topbar">
    {#if activeView !== 'hub'}
      <button class="back-btn" on:click={() => activeView = 'hub'}>‹</button>
    {:else}
      <div class="hwy-logo">HWY <span>TMS</span></div>
    {/if}
    <div class="topbar-title">
      {#if activeView === 'hub'}AI Hub{:else if activeView === 'chat'}Chat with CoDriver{:else if activeView === 'agents'}Agents{:else if activeView === 'models'}Models{:else if activeView === 'settings'}AI Settings{:else if activeView === 'flows'}Flows{:else if activeView === 'toolaccess'}Tool Access{/if}
    </div>
    <div style="display:flex;gap:6px">
      {#if activeView === 'chat'}
        <button class="icon-btn" on:click={() => api('Search conversation')}>🔍</button>
        <button class="icon-btn" on:click={() => success('Conversation bookmarked')}>☆</button>
      {:else if activeView === 'hub'}
        <button class="icon-btn" on:click={() => activeView = 'agents'}>👥</button>
      {/if}
    </div>
  </div>

  <!-- ═══ HUB ═══ -->
  {#if activeView === 'hub'}
    <div class="hub-wrap section">
      <div class="hub-label">
        <div style="font-size:18px;font-weight:700">AI Hub</div>
        <div style="font-size:12px;color:#6b7280">Your AI assistant for everything trucking</div>
      </div>

      <!-- Orbit layout -->
      <div class="orbit-container">
        <!-- Center orb -->
        <button class="center-orb" on:click={() => activeView = 'chat'}>
          <div class="orb-pulse p1"></div>
          <div class="orb-pulse p2"></div>
          <div class="orb-pulse p3"></div>
          <div class="orb-inner">
            <div class="orb-name">CoDriver</div>
            <div class="orb-sub">Ready to help</div>
          </div>
        </button>

        <!-- Orbit items around it -->
        {#each hubItems as item, i}
          <button class="orbit-item" style="--angle:{item.angle}deg" on:click={() => hubNav(item)}>
            <div class="oi-icon">{item.icon}</div>
            <div class="oi-label">{item.label}</div>
          </button>
        {/each}
      </div>

      <!-- Bottom actions -->
      <div class="hub-bottom">
        <button class="hub-action-btn voice-btn" on:mousedown={startListening} on:mouseup={stopListening} on:touchstart={startListening} on:touchend={stopListening}>
          <span>🎙</span> Hold to Talk
        </button>
        <button class="hub-action-btn swipe-btn" on:click={() => goto('/app/flows')}>
          <span>⚡</span> Open Flows
        </button>
      </div>

      <!-- CoDriver Pro banner -->
      <div class="codriverpro-banner" on:click={() => api('CoDriver Pro upgrade')} role="button" tabindex="0">
        <div class="pro-left">
          <div class="pro-icon">✦</div>
          <div>
            <div style="font-size:13px;font-weight:700">CoDriver Pro</div>
            <div style="font-size:11px;color:#93c5fd">Your AI Co-Pilot for dispatchers, drivers and operations</div>
          </div>
        </div>
        <button class="pro-chat-btn" on:click|stopPropagation={() => activeView = 'chat'}>Chat Now</button>
      </div>
    </div>

  <!-- ═══ CHAT ═══ -->
  {:else if activeView === 'chat'}
    <div class="chat-wrap">
      <!-- Chat tabs -->
      <div class="chat-tabs">
        {#each [['chats','Chats'],['pinned','Pinned'],['history','History']] as [k,label]}
          <button class="ctab" class:active={chatTab===k} on:click={() => chatTab=k}>{label}</button>
        {/each}
      </div>

      <div class="runtime-console">
        <div class="runtime-row">
          <span>Runtime</span>
          <strong>{runtimeStatus?.status || 'checking'}</strong>
        </div>
        <div class="runtime-grid">
          <div><small>Execution</small><b>{activeExecution || 'none'}</b></div>
          <div><small>Actor</small><b>{activeActor || 'waiting'}</b></div>
          <div><small>Flow</small><b>{flowStatus}</b></div>
          <div><small>Events</small><b>{timelineEvents.length}</b></div>
        </div>
        {#if lastError}<div class="runtime-error">{lastError}</div>{/if}
        {#if timelineEvents.length}
          <div class="runtime-list">
            <div class="runtime-label">Timeline</div>
            {#each timelineEvents.slice(-5) as event}
              <div class="runtime-event"><span>{event.event_type}</span><em>{event.actor || event.source}</em></div>
            {/each}
          </div>
        {/if}
        {#if recentLogbooks.length}
          <div class="runtime-list">
            <div class="runtime-label">Recent Logbooks</div>
            {#each recentLogbooks.slice(-3) as entry}
              <div class="runtime-event"><span>{entry.event_type}</span><em>{entry.actor}</em></div>
            {/each}
          </div>
        {/if}
      </div>

      {#if chatTab === 'history'}
        <div class="hist-list">
          {#each chatHistory as h}
            <div class="hist-item" on:click={() => openHistory(h)} role="button" tabindex="0">
              <div class="hist-icon">💬</div>
              <div style="flex:1;min-width:0">
                <div style="font-size:13px;font-weight:600">{h.title}</div>
                <div style="font-size:11px;color:#6b7280;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{h.sub}</div>
              </div>
              <div style="font-size:11px;color:#4a5568;flex-shrink:0">{h.time}</div>
            </div>
          {/each}
        </div>

      {:else if chatTab === 'pinned'}
        {#if pinnedMessages.length === 0}
          <div class="empty-state"><div class="icon">📌</div><p>No pinned messages yet. Long-press any message to pin it.</p></div>
        {/if}

      {:else}
        <!-- Main chat -->
        <div class="messages" id="messages">
          <!-- Quick prompt chips if fresh -->
          {#if messages.length === 1}
            <div class="quick-chip-wrap">
              {#each quickActions as qa}
                <button class="qchip" on:click={() => usePrompt(qa)}>
                  {qa.icon} {qa.label}
                </button>
              {/each}
            </div>
          {/if}

          {#each messages as msg, i}
            <div class="msg msg--{msg.role}">
              {#if msg.role === 'assistant'}
                <div class="msg-av">✦</div>
              {/if}
              <div class="msg-bubble" on:dblclick={() => pinMessage(i)} role="none">
                {#each msg.content.split('\n') as line}
                  {#if line.trim()}<p>{line}</p>{/if}
                {/each}
                {#if msg.pinned}<div class="pin-badge">📌</div>{/if}
              </div>
            </div>
          {/each}

          {#if loading}
            <div class="msg msg--assistant">
              <div class="msg-av">✦</div>
              <div class="msg-bubble typing"><span></span><span></span><span></span></div>
            </div>
          {/if}
        </div>

        <!-- Input -->
        <div class="chat-input-row">
          <div class="chat-input-wrap">
            <input bind:value={chatInput} on:keydown={handleKey} placeholder="Ask anything about loads, drivers, docs..." />
            <button class="mic-btn" on:click={() => api('Voice input')}>🎙</button>
          </div>
          <button class="send-btn" on:click={sendMessage} disabled={loading || !chatInput.trim()}>→</button>
        </div>
      {/if}
    </div>

  <!-- ═══ FLOWS (AI view) ═══ -->
  {:else if activeView === 'flows'}
    <div class="section">
      <!-- Quick Actions -->
      <div style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">Quick Actions</div>
      <div class="qa-row">
        {#each [
          {label:'Find Load',icon:'📦',action:()=>usePrompt(quickActions[0])},
          {label:'Check Driver',icon:'🚛',action:()=>usePrompt(quickActions[1])},
          {label:'Send Update',icon:'📡',action:()=>usePrompt(quickActions[2])},
          {label:'Rate Check',icon:'💰',action:()=>usePrompt(quickActions[3])},
        ] as qa}
          <button class="qa-box" on:click={()=>{activeView='chat';qa.action()}}>
            <span style="font-size:20px">{qa.icon}</span>
            <span style="font-size:11px;color:#6b7280">{qa.label}</span>
          </button>
        {/each}
      </div>

      <div style="display:flex;justify-content:space-between;align-items:center;margin:16px 0 10px">
        <span style="font-size:11px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em">My Flows</span>
        <button class="btn btn-secondary btn-sm" on:click={() => goto('/app/flows')}>View All</button>
      </div>

      <div class="card" style="padding:0;overflow:hidden">
        {#each myFlows as f}
          <div class="flow-ai-row">
            <div class="flow-ai-icon">{f.icon}</div>
            <div style="flex:1;cursor:pointer" on:click={() => goto('/app/flows')} role="button" tabindex="0">
              <div style="font-size:13px;font-weight:600">{f.name}</div>
              <div style="font-size:11px;color:#6b7280">{f.steps} steps • {f.type}</div>
            </div>
            <button class="toggle {f.enabled ? 'on' : ''}" on:click={() => toggleFlow(f.id)}></button>
          </div>
        {/each}
      </div>
    </div>

  <!-- ═══ AGENTS ═══ -->
  {:else if activeView === 'agents'}
    <div class="section">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <div>
          <div style="font-size:17px;font-weight:700">Agents</div>
          <div style="font-size:12px;color:#6b7280">Your AI team</div>
        </div>
        <button class="btn btn-primary btn-sm" on:click={() => api('Create custom agent')}>+ Add Agent</button>
      </div>
      <button class="btn btn-secondary btn-sm" style="margin-bottom:16px" on:click={() => api('Manage all agents')}>Manage</button>

      <div style="font-size:10px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">Active Agents</div>
      <div class="card" style="padding:0;overflow:hidden;margin-bottom:16px">
        {#each agents as a}
          <div class="list-item">
            <div class="avatar" style="background:#1e2330;color:#3b82f6;font-size:16px">{a.icon}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{a.name} {#if a.default}<span class="chip chip-blue" style="font-size:9px;padding:1px 6px">Default</span>{/if}</div>
              <div style="font-size:11px;color:#6b7280">{a.sub}</div>
            </div>
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:11px;color:{a.color}">● {a.status}</span>
              <button class="btn btn-secondary btn-sm" on:click={() => api(`Manage ${a.name}`)}>Manage</button>
            </div>
          </div>
        {/each}
      </div>

      <div style="font-size:10px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">Available Agents</div>
      <div class="card" style="padding:0;overflow:hidden">
        {#each availableAgents as a}
          <div class="list-item">
            <div class="avatar" style="background:#1e2330;color:#4a5568;font-size:16px">{a.icon}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600;color:#6b7280">{a.name}</div>
              <div style="font-size:11px;color:#4a5568">{a.sub}</div>
            </div>
            <button class="btn btn-secondary btn-sm" on:click={() => success(`${a.name} added`)}>Add</button>
          </div>
        {/each}
      </div>
    </div>

  <!-- ═══ MODELS ═══ -->
  {:else if activeView === 'models'}
    <div class="section">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <div>
          <div style="font-size:17px;font-weight:700">Models</div>
          <div style="font-size:12px;color:#6b7280">AI Providers & Models</div>
        </div>
        <button class="btn btn-secondary btn-sm" on:click={() => api('Model management')}>Manage</button>
      </div>

      <div style="font-size:10px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">Active Model</div>
      <div class="card" style="padding:0;overflow:hidden;margin-bottom:16px">
        {#each models.filter(m=>m.active) as m}
          <div class="list-item">
            <div class="avatar" style="background:#0f1e2b;color:#3b82f6;font-size:12px;font-weight:800">AI</div>
            <div style="flex:1">
              <div style="font-size:14px;font-weight:700">{m.name}</div>
              <div style="font-size:11px;color:#6b7280">{m.sub} — {m.desc}</div>
            </div>
            <span class="chip chip-green" style="font-size:10px">Active</span>
          </div>
        {/each}
      </div>

      <div style="font-size:10px;color:#4a5568;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">Available Models</div>
      <div class="card" style="padding:0;overflow:hidden">
        {#each models.filter(m=>!m.active) as m}
          <div class="list-item">
            <div class="avatar" style="background:#1e2330;color:#6b7280;font-size:12px;font-weight:700">AI</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:600">{m.name}</div>
              <div style="font-size:11px;color:#4a5568">{m.sub} — {m.desc}</div>
            </div>
            <button class="btn btn-secondary btn-sm" on:click={() => activateModel(m.name)}>Activate</button>
          </div>
        {/each}
      </div>
    </div>

  <!-- ═══ SETTINGS ═══ -->
  {:else if activeView === 'settings'}
    <div class="section">
      <div style="font-size:17px;font-weight:700;margin-bottom:4px">AI Settings</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:20px">Customize your AI experience</div>

      <div class="settings-group">
        <div class="group-label">General</div>
        {#each [['Default AI Assistant','CoDriver'],['Default Model','GPT-4o'],['Auto-Suggestions','On'],['Voice Input','AI talk to talk'],['Message Memory','30 Days']] as [label, val]}
          <div class="settings-row" on:click={() => api(`Edit ${label}`)} role="button" tabindex="0">
            <span>{label}</span><span class="sval">{val} ›</span>
          </div>
        {/each}
      </div>

      <div class="settings-group">
        <div class="group-label">Units & Preferences</div>
        {#each [['Units','Miles, USD, 3F'],['Preferences','']] as [label, val]}
          <div class="settings-row" on:click={() => api(`Edit ${label}`)} role="button" tabindex="0">
            <span>{label}</span><span class="sval">{val} ›</span>
          </div>
        {/each}
      </div>

      <div class="settings-group">
        <div class="group-label">Advanced</div>
        {#each [['Tool Access','Manage allowed tools'],['Data & Privacy','Manage all data usage'],['Safety & Content','Configure safety settings']] as [label, sub]}
          <div class="settings-row" on:click={() => label === 'Tool Access' ? activeView = 'toolaccess' : api(`Open ${label}`)} role="button" tabindex="0">
            <div><div>{label}</div><div style="font-size:11px;color:#4a5568">{sub}</div></div>
            <span class="sval">›</span>
          </div>
        {/each}
      </div>
    </div>

  <!-- ═══ TOOL ACCESS ═══ -->
  {:else if activeView === 'toolaccess'}
    <div class="section">
      <div style="font-size:17px;font-weight:700;margin-bottom:4px">Tool Access</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:6px">Manage tools CoDriver can use</div>
      <div style="font-size:12px;color:#4a5568;margin-bottom:20px">Tools give CoDriver the ability to take action on your TMS. You can enable or disable any tool at any time.</div>
      <button class="btn btn-secondary btn-sm" style="margin-bottom:16px" on:click={() => info('Learn more about tool access')}>Learn More</button>

      <div class="card" style="padding:0;overflow:hidden">
        {#each toolAccess as tool, i}
          <div class="list-item">
            <div style="flex:1">
              <div style="font-size:14px;font-weight:600">{tool.name}</div>
              <div style="font-size:11px;color:#6b7280">{tool.sub}</div>
            </div>
            <button class="toggle {tool.enabled ? 'on' : ''}" on:click={() => toggleTool(i)}></button>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- TALK / LISTENING overlay -->
  {#if listening}
    <div class="listen-overlay">
      <div class="listen-circle">
        <div class="lc-ring lr1"></div>
        <div class="lc-ring lr2"></div>
        <div class="lc-ring lr3"></div>
        <div class="lc-core">✦</div>
      </div>
      <div class="listen-label">Listening...</div>
      <button class="release-btn" on:click={releaseToStop}>Release to Stop</button>
    </div>
  {/if}
</div>

<style>
  .ai-page { position: relative; overflow: hidden; }

  .ai-topbar {
    display: flex; align-items: center; gap: 10px;
    padding: 14px 16px; border-bottom: 1px solid #1e2330;
    position: sticky; top: 0; background: #0d0f14; z-index: 50;
  }
  .back-btn { background: none; border: none; color: #3b82f6; font-size: 24px; cursor: pointer; flex-shrink: 0; }
  .hwy-logo { font-size: 20px; font-weight: 800; }
  .hwy-logo span { color: #3b82f6; }
  .topbar-title { flex: 1; font-size: 16px; font-weight: 700; }
  .icon-btn { background: #161a23; border: 1px solid #1e2330; border-radius: 8px; padding: 6px 10px; font-size: 15px; cursor: pointer; }

  /* ── HUB ── */
  .hub-wrap { display: flex; flex-direction: column; align-items: center; gap: 0; }
  .hub-label { text-align: center; margin-bottom: 12px; }

  .orbit-container {
    position: relative;
    width: 280px; height: 280px;
    margin: 0 auto 16px;
  }

  .center-orb {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 110px; height: 110px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #1d4ed8, #0a0d14);
    border: none;
    cursor: pointer;
    z-index: 10;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 40px rgba(59,130,246,0.35);
  }
  .orb-pulse {
    position: absolute; border-radius: 50%;
    border: 1px solid #3b82f6;
    animation: orb-ring 2.5s ease-out infinite;
  }
  .p1 { width: 110px; height: 110px; animation-delay: 0s; opacity: 0.3; }
  .p2 { width: 140px; height: 140px; animation-delay: 0.7s; opacity: 0.2; }
  .p3 { width: 170px; height: 170px; animation-delay: 1.4s; opacity: 0.1; }
  @keyframes orb-ring {
    0% { transform: scale(0.9); opacity: 0; }
    50% { opacity: 0.4; }
    100% { transform: scale(1.2); opacity: 0; }
  }
  .orb-inner { text-align: center; z-index: 2; position: relative; }
  .orb-name { font-size: 13px; font-weight: 700; color: #fff; }
  .orb-sub { font-size: 10px; color: #93c5fd; margin-top: 2px; }

  .orbit-item {
    position: absolute;
    top: 50%; left: 50%;
    width: 60px; height: 60px;
    margin: -30px 0 0 -30px;
    transform: rotate(var(--angle)) translateX(105px) rotate(calc(-1 * var(--angle)));
    background: #161a23; border: 1px solid #1e2330;
    border-radius: 14px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 3px; cursor: pointer; transition: background 0.15s, border-color 0.15s;
  }
  .orbit-item:hover { background: #1e2330; border-color: #3b82f6; }
  .oi-icon { font-size: 20px; line-height: 1; }
  .oi-label { font-size: 9px; color: #6b7280; font-weight: 600; }

  .hub-bottom { display: flex; gap: 10px; width: 100%; margin-bottom: 14px; }
  .hub-action-btn {
    flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px;
    padding: 11px; border-radius: 12px; border: 1px solid #1e2330;
    background: #161a23; color: #e2e8f0; font-size: 13px; font-weight: 600; cursor: pointer;
    transition: background 0.15s;
  }
  .hub-action-btn:hover { background: #1e2330; }
  .voice-btn:active { background: #1e3a5f; border-color: #3b82f6; color: #3b82f6; }

  .codriverpro-banner {
    width: 100%; background: linear-gradient(135deg, #0f1e40, #1a1040);
    border: 1px solid #3b82f640; border-radius: 14px;
    padding: 14px 16px; display: flex; align-items: center; gap: 12px;
    cursor: pointer; transition: border-color 0.15s;
  }
  .codriverpro-banner:hover { border-color: #3b82f6; }
  .pro-left { display: flex; align-items: center; gap: 10px; flex: 1; }
  .pro-icon { font-size: 22px; color: #3b82f6; }
  .pro-chat-btn {
    background: #3b82f6; border: none; color: #fff;
    padding: 8px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer;
    flex-shrink: 0;
  }

  /* ── CHAT ── */
  .chat-wrap { display: flex; flex-direction: column; height: calc(100vh - 113px); }
  .chat-tabs { display: flex; border-bottom: 1px solid #1e2330; }
  .ctab { flex: 1; padding: 11px; border: none; background: none; color: #6b7280; font-size: 13px; font-weight: 600; cursor: pointer; border-bottom: 2px solid transparent; }
  .ctab.active { color: #3b82f6; border-bottom-color: #3b82f6; }
  .runtime-console { margin: 10px 14px; padding: 12px; background: #111827; border: 1px solid #1e3a5f; border-radius: 14px; font-size: 12px; }
  .runtime-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; color: #93c5fd; }
  .runtime-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
  .runtime-grid div { background: #0d0f14; border: 1px solid #1e2330; border-radius: 10px; padding: 8px; min-width: 0; }
  .runtime-grid small { display: block; color: #6b7280; font-size: 10px; margin-bottom: 3px; }
  .runtime-grid b { display: block; color: #e2e8f0; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .runtime-list { margin-top: 9px; border-top: 1px solid #1e2330; padding-top: 8px; }
  .runtime-label { font-size: 10px; color: #6b7280; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 5px; }
  .runtime-event { display: flex; justify-content: space-between; gap: 8px; padding: 3px 0; color: #cbd5e1; }
  .runtime-event em { color: #64748b; font-style: normal; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .runtime-error { margin-top: 8px; color: #fca5a5; }

  .hist-list { overflow-y: auto; flex: 1; }
  .hist-item { display: flex; align-items: center; gap: 12px; padding: 13px 16px; border-bottom: 1px solid #1e2330; cursor: pointer; }
  .hist-item:hover { background: #161a23; }
  .hist-icon { width: 36px; height: 36px; background: #1e2330; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }

  .messages { flex: 1; overflow-y: auto; padding: 14px 16px; display: flex; flex-direction: column; gap: 12px; }
  .quick-chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }
  .qchip {
    background: #161a23; border: 1px solid #2d3548; border-radius: 20px;
    padding: 7px 13px; font-size: 12px; color: #3b82f6; cursor: pointer; transition: background 0.15s;
  }
  .qchip:hover { background: #1e2330; }

  .msg { display: flex; gap: 8px; }
  .msg--user { flex-direction: row-reverse; }
  .msg-av { width: 28px; height: 28px; border-radius: 50%; background: #1e2330; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #3b82f6; flex-shrink: 0; }
  .msg-bubble { max-width: 82%; background: #161a23; border: 1px solid #1e2330; border-radius: 14px; padding: 10px 13px; font-size: 13px; line-height: 1.55; position: relative; }
  .msg--user .msg-bubble { background: #1e3a5f; border-color: #3b82f660; }
  .msg-bubble p { margin: 0; }
  .msg-bubble p + p { margin-top: 5px; }
  .pin-badge { position: absolute; top: -6px; right: -6px; font-size: 11px; }
  .typing { display: flex; gap: 4px; align-items: center; padding: 12px 16px; }
  .typing span { width: 6px; height: 6px; background: #3b82f6; border-radius: 50%; animation: bounce 1.2s infinite; }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

  .chat-input-row { display: flex; gap: 8px; padding: 10px 14px; border-top: 1px solid #1e2330; background: #0d0f14; }
  .chat-input-wrap { flex: 1; display: flex; background: #161a23; border: 1px solid #2d3548; border-radius: 22px; overflow: hidden; align-items: center; padding: 0 12px; }
  .chat-input-wrap input { background: none; border: none; flex: 1; padding: 10px 0; font-size: 14px; color: #e2e8f0; }
  .chat-input-wrap input::placeholder { color: #4a5568; }
  .mic-btn { background: none; border: none; font-size: 16px; cursor: pointer; padding: 4px; }
  .send-btn { background: #3b82f6; border: none; border-radius: 50%; width: 42px; height: 42px; color: #fff; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .send-btn:disabled { opacity: 0.4; }

  /* ── FLOWS AI VIEW ── */
  .qa-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; }
  .qa-box { background: #161a23; border: 1px solid #1e2330; border-radius: 12px; padding: 12px 6px; display: flex; flex-direction: column; align-items: center; gap: 5px; cursor: pointer; transition: background 0.15s; }
  .qa-box:hover { background: #1e2330; }
  .flow-ai-row { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-bottom: 1px solid #1e2330; }
  .flow-ai-row:last-child { border-bottom: none; }
  .flow-ai-icon { width: 34px; height: 34px; background: #1e2330; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 17px; flex-shrink: 0; }

  /* ── SETTINGS ── */
  .settings-group { margin-bottom: 22px; }
  .group-label { font-size: 10px; color: #4a5568; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
  .settings-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #1e2330; font-size: 14px; cursor: pointer; }
  .settings-row:hover { color: #3b82f6; }
  .settings-row:last-child { border-bottom: none; }
  .sval { color: #6b7280; font-size: 13px; }

  /* ── LISTENING OVERLAY ── */
  .listen-overlay {
    position: fixed; inset: 0; background: rgba(13,15,20,0.95);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    z-index: 999; gap: 16px;
  }
  .listen-circle { position: relative; width: 160px; height: 160px; display: flex; align-items: center; justify-content: center; }
  .lc-ring { position: absolute; border-radius: 50%; border: 2px solid #3b82f6; animation: lring 1.5s ease-out infinite; }
  .lr1 { width: 80px; height: 80px; animation-delay: 0s; }
  .lr2 { width: 120px; height: 120px; animation-delay: 0.4s; opacity: 0.6; }
  .lr3 { width: 160px; height: 160px; animation-delay: 0.8s; opacity: 0.3; }
  @keyframes lring { 0%{opacity:0.8;transform:scale(0.9)} 100%{opacity:0;transform:scale(1.1)} }
  .lc-core { width: 64px; height: 64px; border-radius: 50%; background: #3b82f6; display: flex; align-items: center; justify-content: center; font-size: 28px; color: #fff; z-index: 2; box-shadow: 0 0 30px rgba(59,130,246,0.6); }
  .listen-label { font-size: 18px; font-weight: 700; color: #e2e8f0; }
  .release-btn { background: #1e2330; border: 1px solid #3b82f6; color: #3b82f6; padding: 12px 28px; border-radius: 24px; font-size: 14px; font-weight: 600; cursor: pointer; }
</style>
