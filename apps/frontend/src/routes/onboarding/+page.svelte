<script>
  import { browser } from '$app/environment';
  import { goto } from '$app/navigation';
  import { company as companyStore, user, onboarded, token as tokenStore } from '$lib/stores/app.js';
  import { error as toastError } from '$lib/stores/toast.js';
  import { post, setToken } from '$lib/api.js';

  let step = 0;
  let showPassword = false;

  let deviceId = '';
  let deviceLocation = { lat: null, lng: null };

  if (browser) {
    deviceId = localStorage.getItem('hwy_device_id');
    if (!deviceId) {
      deviceId = crypto.randomUUID();
      localStorage.setItem('hwy_device_id', deviceId);
    }
  }
  // 0 = welcome, 1 = pick role, 2 = your info, 3 = company/dispatcher info, 4 = fleet/authority, 5 = done

  let role = ''; // 'carrier' | 'driver' | 'owner-op'
  let termsAccepted = false;

  let form = {
    // user
    firstName: '', lastName: '', email: '', password: '', phone: '', userRole: 'Owner',
    // company
    companyName: '', mc: '', dot: '', scac: '', companyType: 'For-Hire Carrier',
    founded: '', address: '', city: '', state: '', zip: '',
    companyEmail: '', companyPhone: '', website: '',
    // fleet
    fleetSize: '', trailerTypes: [], operatingStates: '',
    // driver-specific
    cdlNumber: '', cdlClass: 'Class A', cdlExpiry: '', cdlState: '',
    dispatcherName: '', dispatcherCompany: '', dispatcherEmail: '', dispatcherPhone: '',
    truckNumber: '', truckType: 'Dry Van', truckYear: '', truckMake: '', truckPlate: '',
    homeBase: '', ownerOpMc: '',
  };

  const trailerOptions = ['Dry Van', 'Flatbed', 'Reefer', 'Step Deck', 'RGN', 'Tanker', 'Auto Hauler', 'Power Only', 'Other'];
  const states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'];

  const roles = [
    {
      key: 'carrier',
      icon: '🏢',
      title: 'Dispatching Company',
      sub: 'I run a fleet — I have drivers and dispatchers working for me',
      color: '#3b82f6'
    },
    {
      key: 'driver',
      icon: '🚛',
      title: 'Driver with Dispatcher',
      sub: 'I drive for a company or work with a dispatch service',
      color: '#22c55e'
    },
    {
      key: 'owner-op',
      icon: '⭐',
      title: 'Owner-Operator',
      sub: 'I own my truck and run my own loads independently',
      color: '#f59e0b'
    }
  ];

  function toggleTrailer(t) {
    form.trailerTypes = form.trailerTypes.includes(t)
      ? form.trailerTypes.filter(x => x !== t)
      : [...form.trailerTypes, t];
  }

  function selectRole(r) {
    role = r;
    step = 2;
  }

  function next() {
    if (step === 2) {
      if (!form.firstName || !form.email || !form.password) { toastError('Name, email, and password required'); return; }
      if (!termsAccepted) { toastError('You must accept the Terms of Service and Privacy Policy'); return; }
    }
    if (step === 3) {
      if (role === 'carrier' && !form.companyName) { toastError('Company name required'); return; }
      if (role === 'driver' && !form.cdlNumber) { toastError('CDL number required'); return; }
      if (role === 'owner-op' && !form.companyName) { toastError('Company or DBA name required'); return; }
    }
    step++;
  }

  function back() { step = step <= 2 ? (step === 2 ? 1 : 0) : step - 1; }

  function getLocation() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) { resolve({ lat: null, lng: null }); return; }
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => resolve({ lat: null, lng: null }),
        { timeout: 5000, enableHighAccuracy: false }
      );
    });
  }

  async function finish() {
    if (role === 'carrier' && !form.mc && !form.dot) { toastError('MC or DOT number required'); return; }
    if (role === 'owner-op' && !form.ownerOpMc && !form.dot) { toastError('MC or DOT number required'); return; }
    if (!form.password) { toastError('Password required'); return; }

    const userData = {
      name: `${form.firstName} ${form.lastName}`.trim(),
      email: form.email, phone: form.phone,
      role: role === 'driver' ? 'Driver' : role === 'owner-op' ? 'Owner-Operator' : form.userRole,
      avatar: ''
    };

    const companyData = {
      name: form.companyName || `${form.firstName} ${form.lastName} Trucking`,
      mc: form.mc || form.ownerOpMc, dot: form.dot, scac: form.scac,
      type: role === 'driver' ? 'Driver' : role === 'owner-op' ? 'Owner-Operator' : form.companyType,
      founded: form.founded, address: form.address, city: form.city,
      state: form.state, zip: form.zip,
      phone: form.companyPhone || form.phone,
      email: form.companyEmail || form.email,
      website: form.website,
      fleet_size: role === 'owner-op' ? '1' : form.fleetSize,
      trailer_types: form.trailerTypes.length ? form.trailerTypes : [form.truckType],
      operating_states: form.operatingStates.split(',').map(s => s.trim()).filter(Boolean),
      cdl: form.cdlNumber, cdlClass: form.cdlClass, cdlExpiry: form.cdlExpiry,
      dispatcher: form.dispatcherCompany,
      truck: form.truckNumber, role_type: role
    };

    const { data: regData, error: regError } = await post('/auth/register', {
      name: userData.name,
      email: form.email,
      password: form.password
    });
    if (regError) { toastError(regError); return; }

    if (regData?.access_token) {
      setToken(regData.access_token);
      tokenStore.set(regData.access_token);
    }
    if (regData?.user) {
      user.set(regData.user);
    }

    const loc = await getLocation();
    deviceLocation = loc;

    const { error: apiError } = await post('/auth/onboarding', {
      user: userData,
      company: companyData,
      onboarded: true,
      device_id: deviceId,
      location_lat: loc.lat,
      location_lng: loc.lng,
      user_agent: navigator.userAgent,
      terms_accepted: termsAccepted
    });
    if (apiError) { toastError(apiError); return; }

    companyStore.set(companyData);
    onboarded.set(true);
    goto('/app/dashboard');
  }

  $: totalSteps = role === 'driver' ? 4 : 5;
  $: progress = step <= 1 ? 0 : ((step - 1) / (totalSteps - 1)) * 100;
</script>

<div class="onboarding">
  {#if step > 1}
    <div class="progress-bar">
      <div class="progress-fill" style="width:{progress}%"></div>
    </div>
  {/if}

  <!-- STEP 0: WELCOME / SPLASH INTO ONBOARDING -->
  {#if step === 0}
    <div class="step welcome">
      <div class="welcome-emblem">
        <div class="we-ring r1"></div>
        <div class="we-ring r2"></div>
        <div class="we-core">🛣️</div>
      </div>
      <div class="splash-logo">HWY <span>TMS</span></div>
      <h1>Your Dispatch Command Center</h1>
      <p class="sub">Built for everyone in trucking — carriers, drivers, and owner-operators. Setup takes under 3 minutes.</p>

      <div class="feature-cards">
        <div class="feat">✦ AI-powered CoDriver dispatch assistant</div>
        <div class="feat">✦ Automated workflows & smart flows</div>
        <div class="feat">✦ Load board, broker & logbook network</div>
        <div class="feat">✦ Full compliance & document management</div>
      </div>

      <button class="btn btn-primary btn-full" on:click={() => step = 1}>Get Started →</button>
      <p class="terms">By continuing you agree to our Terms & Privacy Policy</p>
    </div>

  <!-- STEP 1: PICK YOUR ROLE -->
  {:else if step === 1}
    <div class="step">
      <div class="step-hdr">
        <div class="step-label">Who are you?</div>
        <h2>Pick your role</h2>
        <p class="sub">This customizes your entire experience</p>
      </div>

      <div class="role-cards">
        {#each roles as r}
          <button class="role-card" on:click={() => selectRole(r.key)} style="--accent:{r.color}">
            <div class="role-icon" style="background:{r.color}22;color:{r.color}">{r.icon}</div>
            <div class="role-text">
              <div class="role-title">{r.title}</div>
              <div class="role-sub">{r.sub}</div>
            </div>
            <div class="role-arrow" style="color:{r.color}">›</div>
          </button>
        {/each}
      </div>

      <button class="btn btn-secondary btn-full" style="margin-top:8px" on:click={() => step = 0}>← Back</button>
    </div>

  <!-- STEP 2: YOUR PERSONAL INFO -->
  {:else if step === 2}
    <div class="step scrollable">
      <div class="step-hdr">
        <div class="step-label">Step 1 — About You</div>
        <h2>{role === 'driver' ? 'Driver Info' : role === 'owner-op' ? 'Your Info' : 'Your Profile'}</h2>
        <p class="sub">Tell us who's at the wheel</p>
      </div>

      <div class="row">
        <div class="col form-group"><label class="label">First Name *</label><input bind:value={form.firstName} placeholder="Jesse" /></div>
        <div class="col form-group"><label class="label">Last Name</label><input bind:value={form.lastName} placeholder="Conley" /></div>
      </div>
      <div class="form-group"><label class="label">Email *</label><input type="email" bind:value={form.email} placeholder="jesse@company.com" /></div>
      <div class="form-group">
        <label class="label" for="password">Password *</label>
        <div class="password-wrap">
          <input id="password" type={showPassword ? 'text' : 'password'} value={form.password} on:input={e => form.password = e.target.value} placeholder="Create a password (min 8 chars)" />
          <button class="pw-toggle" type="button" on:click={() => showPassword = !showPassword} tabindex="-1">
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>
      </div>
      <div class="form-group"><label class="label">Phone</label><input type="tel" bind:value={form.phone} placeholder="(555) 000-0000" /></div>
      {#if role === 'carrier'}
        <div class="form-group">
          <label class="label">Your Role at Company</label>
          <select bind:value={form.userRole}>
            <option>Owner</option><option>Fleet Manager</option><option>Operations Manager</option><option>Dispatcher</option>
          </select>
        </div>
      {/if}

      <label class="terms-row">
        <input type="checkbox" bind:checked={termsAccepted} />
        <span>I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/privacy" target="_blank">Privacy Policy</a></span>
      </label>

      <div class="nav-btns">
        <button class="btn btn-secondary" on:click={back}>Back</button>
        <button class="btn btn-primary" on:click={next}>Continue →</button>
      </div>
    </div>

  <!-- STEP 3: ROLE-SPECIFIC INFO -->
  {:else if step === 3}

    <!-- CARRIER: Company Info -->
    {#if role === 'carrier'}
      <div class="step scrollable">
        <div class="step-hdr">
          <div class="step-label">Step 2 — Your Company</div>
          <h2>Company Details</h2>
          <p class="sub">This builds your logbook & authority profile</p>
        </div>
        <div class="form-group"><label class="label">Company Name *</label><input bind:value={form.companyName} placeholder="Conley Logistics LLC" /></div>
        <div class="row">
          <div class="col form-group"><label class="label">Company Type</label>
            <select bind:value={form.companyType}>
              <option>For-Hire Carrier</option><option>Private Carrier</option><option>Broker</option>
            </select>
          </div>
          <div class="col form-group"><label class="label">Founded</label><input type="date" bind:value={form.founded} /></div>
        </div>
        <div class="form-group"><label class="label">Street Address</label><input bind:value={form.address} placeholder="123 Logistics Way" /></div>
        <div class="row">
          <div class="col form-group"><label class="label">City</label><input bind:value={form.city} placeholder="Dallas" /></div>
          <div class="col form-group" style="flex:0 0 65px"><label class="label">State</label>
            <select bind:value={form.state}><option value="">--</option>{#each states as s}<option>{s}</option>{/each}</select>
          </div>
          <div class="col form-group" style="flex:0 0 85px"><label class="label">ZIP</label><input bind:value={form.zip} placeholder="75001" /></div>
        </div>
        <div class="form-group"><label class="label">Company Email</label><input type="email" bind:value={form.companyEmail} placeholder="info@company.com" /></div>
        <div class="form-group"><label class="label">Company Phone</label><input type="tel" bind:value={form.companyPhone} /></div>
        <div class="nav-btns">
          <button class="btn btn-secondary" on:click={back}>Back</button>
          <button class="btn btn-primary" on:click={next}>Continue →</button>
        </div>
      </div>

    <!-- DRIVER: CDL + Dispatcher Info -->
    {:else if role === 'driver'}
      <div class="step scrollable">
        <div class="step-hdr">
          <div class="step-label">Step 2 — Your License & Dispatcher</div>
          <h2>CDL & Dispatcher</h2>
          <p class="sub">Your credentials and who dispatches you</p>
        </div>

        <div class="section-divider">Your CDL</div>
        <div class="row">
          <div class="col form-group"><label class="label">CDL Number *</label><input bind:value={form.cdlNumber} placeholder="TX1234567" /></div>
          <div class="col form-group"><label class="label">Class</label>
            <select bind:value={form.cdlClass}><option>Class A</option><option>Class B</option><option>Class C</option></select>
          </div>
        </div>
        <div class="row">
          <div class="col form-group"><label class="label">CDL State</label>
            <select bind:value={form.cdlState}><option value="">--</option>{#each states as s}<option>{s}</option>{/each}</select>
          </div>
          <div class="col form-group"><label class="label">Expiration</label><input type="date" bind:value={form.cdlExpiry} /></div>
        </div>

        <div class="section-divider">Your Dispatcher / Company</div>
        <div class="form-group"><label class="label">Dispatcher Name</label><input bind:value={form.dispatcherName} placeholder="Mike Johnson" /></div>
        <div class="form-group"><label class="label">Company / Dispatch Service</label><input bind:value={form.dispatcherCompany} placeholder="Acme Dispatch LLC" /></div>
        <div class="form-group"><label class="label">Dispatcher Email</label><input bind:value={form.dispatcherEmail} placeholder="dispatch@company.com" /></div>
        <div class="form-group"><label class="label">Dispatcher Phone</label><input bind:value={form.dispatcherPhone} placeholder="(555) 000-0000" /></div>

        <div class="section-divider">Your Truck</div>
        <div class="row">
          <div class="col form-group"><label class="label">Truck #</label><input bind:value={form.truckNumber} placeholder="#101" /></div>
          <div class="col form-group"><label class="label">Equipment</label>
            <select bind:value={form.truckType}><option>Dry Van</option><option>Flatbed</option><option>Reefer</option><option>Step Deck</option><option>Tanker</option></select>
          </div>
        </div>
        <div class="row">
          <div class="col form-group"><label class="label">Year</label><input bind:value={form.truckYear} placeholder="2021" /></div>
          <div class="col form-group"><label class="label">Make</label><input bind:value={form.truckMake} placeholder="Freightliner" /></div>
        </div>

        <div class="nav-btns">
          <button class="btn btn-secondary" on:click={back}>Back</button>
          <button class="btn btn-primary" on:click={finish}>Finish Setup ✓</button>
        </div>
      </div>

    <!-- OWNER-OP: Their own company + truck -->
    {:else if role === 'owner-op'}
      <div class="step scrollable">
        <div class="step-hdr">
          <div class="step-label">Step 2 — Your Business</div>
          <h2>Company & Truck</h2>
          <p class="sub">Your DBA, authority, and equipment</p>
        </div>
        <div class="form-group"><label class="label">Company / DBA Name *</label><input bind:value={form.companyName} placeholder="Conley Trucking LLC" /></div>
        <div class="row">
          <div class="col form-group"><label class="label">MC Number</label><input bind:value={form.ownerOpMc} placeholder="MC-1234567" /></div>
          <div class="col form-group"><label class="label">DOT Number</label><input bind:value={form.dot} placeholder="3456789" /></div>
        </div>
        <div class="form-group"><label class="label">Home Base State</label>
          <select bind:value={form.state}><option value="">--</option>{#each states as s}<option>{s}</option>{/each}</select>
        </div>

        <div class="section-divider">Your Truck</div>
        <div class="row">
          <div class="col form-group"><label class="label">Truck #</label><input bind:value={form.truckNumber} placeholder="#1" /></div>
          <div class="col form-group"><label class="label">Equipment</label>
            <select bind:value={form.truckType}><option>Dry Van</option><option>Flatbed</option><option>Reefer</option><option>Step Deck</option><option>Tanker</option></select>
          </div>
        </div>
        <div class="row">
          <div class="col form-group"><label class="label">Year</label><input bind:value={form.truckYear} placeholder="2021" /></div>
          <div class="col form-group"><label class="label">Make</label><input bind:value={form.truckMake} placeholder="Peterbilt" /></div>
        </div>

        <div class="section-divider">Your CDL</div>
        <div class="row">
          <div class="col form-group"><label class="label">CDL Number</label><input bind:value={form.cdlNumber} placeholder="TX1234567" /></div>
          <div class="col form-group"><label class="label">Expiration</label><input type="date" bind:value={form.cdlExpiry} /></div>
        </div>

        <div class="nav-btns">
          <button class="btn btn-secondary" on:click={back}>Back</button>
          <button class="btn btn-primary" on:click={next}>Continue →</button>
        </div>
      </div>
    {/if}

  <!-- STEP 4: CARRIER Fleet + Authority -->
  {:else if step === 4 && role === 'carrier'}
    <div class="step scrollable">
      <div class="step-hdr">
        <div class="step-label">Step 3 — Authority & Fleet</div>
        <h2>FMCSA & Equipment</h2>
        <p class="sub">Your operating authority and fleet details</p>
      </div>

      <div class="row">
        <div class="col form-group"><label class="label">MC Number *</label><input bind:value={form.mc} placeholder="MC-1234567" /></div>
        <div class="col form-group"><label class="label">DOT Number *</label><input bind:value={form.dot} placeholder="3456789" /></div>
      </div>
      <div class="form-group"><label class="label">SCAC Code</label><input bind:value={form.scac} placeholder="ABCD" maxlength="4" /></div>
      <div class="form-group"><label class="label">Total Trucks in Fleet</label><input type="number" bind:value={form.fleetSize} placeholder="12" min="1" /></div>

      <div class="form-group">
        <label class="label">Equipment Types (select all)</label>
        <div class="chip-grid">
          {#each trailerOptions as t}
            <button class="trailer-chip" class:selected={form.trailerTypes.includes(t)} on:click={() => toggleTrailer(t)}>{t}</button>
          {/each}
        </div>
      </div>

      <div class="form-group">
        <label class="label">Operating States</label>
        <input bind:value={form.operatingStates} placeholder="TX, LA, OK or 48 States" />
      </div>

      <div class="nav-btns">
        <button class="btn btn-secondary" on:click={back}>Back</button>
        <button class="btn btn-primary" on:click={finish}>Finish Setup ✓</button>
      </div>
    </div>

  <!-- STEP 4: OWNER-OP operating states + trailers -->
  {:else if step === 4 && role === 'owner-op'}
    <div class="step scrollable">
      <div class="step-hdr">
        <div class="step-label">Step 3 — Operations</div>
        <h2>Your Lanes & Equipment</h2>
        <p class="sub">Where you run and what you haul</p>
      </div>

      <div class="form-group">
        <label class="label">Equipment Types</label>
        <div class="chip-grid">
          {#each trailerOptions as t}
            <button class="trailer-chip" class:selected={form.trailerTypes.includes(t)} on:click={() => toggleTrailer(t)}>{t}</button>
          {/each}
        </div>
      </div>
      <div class="form-group"><label class="label">Preferred Lanes / Operating States</label><input bind:value={form.operatingStates} placeholder="TX, OK, LA or Nationwide" /></div>
      <div class="form-group"><label class="label">Home Base City</label><input bind:value={form.city} placeholder="Dallas, TX" /></div>

      <div class="nav-btns">
        <button class="btn btn-secondary" on:click={back}>Back</button>
        <button class="btn btn-primary" on:click={finish}>Finish Setup ✓</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .onboarding {
    min-height: 100vh;
    background: #0d0f14;
    display: flex;
    flex-direction: column;
  }

  .progress-bar { height: 3px; background: #1e2330; flex-shrink: 0; }
  .progress-fill { height: 100%; background: #3b82f6; transition: width 0.4s ease; }

  .step {
    padding: 32px 24px 40px;
    max-width: 480px;
    width: 100%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    flex: 1;
  }
  .scrollable { overflow-y: auto; }

  /* Welcome */
  .welcome { align-items: center; text-align: center; justify-content: center; }
  .welcome-emblem {
    position: relative; width: 110px; height: 110px;
    display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
  }
  .we-ring { position: absolute; border-radius: 50%; border: 1.5px solid #3b82f6; }
  .r1 { width: 110px; height: 110px; opacity: 0.15; animation: pr 2s ease infinite; }
  .r2 { width: 78px; height: 78px; opacity: 0.3; animation: pr 2s ease infinite 0.5s; }
  @keyframes pr { 0%,100%{opacity:0.1;transform:scale(0.95)} 50%{opacity:0.4;transform:scale(1.05)} }
  .we-core {
    width: 52px; height: 52px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #2563eb, #0d0f14);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; box-shadow: 0 0 28px rgba(59,130,246,0.5); z-index: 2;
  }
  .splash-logo { font-size: 32px; font-weight: 900; letter-spacing: -0.03em; margin-bottom: 16px; }
  .splash-logo span { color: #3b82f6; }
  .welcome h1 { font-size: 22px; font-weight: 700; line-height: 1.2; margin-bottom: 10px; }
  .sub { font-size: 13px; color: #6b7280; line-height: 1.6; margin-bottom: 24px; }
  .feature-cards { width: 100%; display: flex; flex-direction: column; gap: 8px; margin-bottom: 28px; }
  .feat { background: #161a23; border: 1px solid #1e2330; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #cbd5e0; text-align: left; }
  .terms { margin-top: 12px; font-size: 11px; color: #374151; }

  /* Role picker */
  .step-hdr { margin-bottom: 24px; }
  .step-label { font-size: 11px; color: #3b82f6; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }
  .step-hdr h2 { font-size: 22px; font-weight: 700; margin-bottom: 4px; }

  .role-cards { display: flex; flex-direction: column; gap: 12px; }
  .role-card {
    display: flex; align-items: center; gap: 14px;
    background: #161a23; border: 1.5px solid #1e2330;
    border-radius: 14px; padding: 16px; cursor: pointer;
    transition: border-color 0.15s, background 0.15s; text-align: left;
  }
  .role-card:hover { border-color: var(--accent); background: #1a1e28; }
  .role-icon { width: 46px; height: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
  .role-text { flex: 1; }
  .role-title { font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 3px; }
  .role-sub { font-size: 12px; color: #6b7280; line-height: 1.4; }
  .role-arrow { font-size: 22px; font-weight: 300; flex-shrink: 0; }

  /* Form */
  .section-divider {
    font-size: 10px; color: #4a5568; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; margin: 16px 0 12px; padding-bottom: 8px;
    border-bottom: 1px solid #1e2330;
  }
  .form-group { margin-bottom: 14px; }
  .row { display: flex; gap: 10px; }
  .col { flex: 1; min-width: 0; }
  .chip-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
  .trailer-chip {
    padding: 7px 13px; border-radius: 20px; border: 1px solid #2d3548;
    background: #161a23; color: #6b7280; font-size: 13px; cursor: pointer; transition: all 0.15s;
  }
  .trailer-chip.selected { background: #0f1e2b; border-color: #3b82f6; color: #3b82f6; }

  .nav-btns { display: flex; gap: 10px; margin-top: auto; padding-top: 24px; }
  .nav-btns .btn { flex: 1; }

  .password-wrap {
    position: relative;
  }
  .password-wrap input {
    padding-right: 44px;
  }
  .pw-toggle {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    background: none;
    border: none;
    color: #6b7280;
    font-size: 18px;
    padding: 0 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  .pw-toggle:hover { color: #e2e8f0; }

  .terms-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin: 16px 0;
    font-size: 13px;
    color: #6b7280;
    line-height: 1.5;
    cursor: pointer;
  }
  .terms-row input[type="checkbox"] {
    width: 18px;
    height: 18px;
    margin-top: 1px;
    flex-shrink: 0;
    accent-color: #3b82f6;
    cursor: pointer;
  }
  .terms-row a {
    color: #3b82f6;
    text-decoration: underline;
  }
  .terms-row a:hover { color: #60a5fa; }
</style>
