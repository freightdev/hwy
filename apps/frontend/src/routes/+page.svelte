<script>
  const operatingCards = [
    ['Dispatch', 'Plan loads, drivers, brokers, documents, and payments from one mobile surface.'],
    ['CoDriver', 'Ask what needs to happen next and route work through the runtime safely.'],
    ['Profiles', 'Company, driver, team, role, permission, and compliance profiles stay connected.'],
    ['Admin', 'Control users, access, packages, billing readiness, and operational permissions.']
  ];

  const packageCards = [
    ['auth', 'Identity, sessions, roles, permissions'],
    ['profiles', 'Company, people, equipment, authority'],
    ['payments', 'Invoices, payments, settlements'],
    ['ui', 'Mobile-first HWY design system'],
    ['codriver', 'AI runtime contracts and console'],
    ['compliance', 'Documents, insurance, IFTA, audits']
  ];
</script>

<svelte:head><title>HWY TMS — Mobile trucking command center</title></svelte:head>

<main class="landing">
  <nav class="nav" aria-label="Public navigation">
    <a class="brand" href="/"><span>HWY</span> TMS</a>
    <div class="nav-actions">
      <a href="#platform">Platform</a>
      <a href="/login">Sign in</a>
      <a class="nav-cta" href="/signup">Create account</a>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-copy">
      <div class="badge">Built for trucking operators who live on their phone</div>
      <h1>Run your trucking company from one mobile command center</h1>
      <p>Dispatch, compliance, payments, profiles, permissions, and CoDriver in one operating system for carriers, owner-operators, dispatchers, drivers, and back-office teams.</p>
      <div class="hero-actions">
        <a class="primary" href="/signup">Create account</a>
        <a class="secondary" href="/login">Sign in</a>
      </div>
      <div class="proof-row" aria-label="Platform facts">
        <span><strong>Mobile first</strong> desktop friendly</span>
        <span><strong>Role based</strong> permission-ready</span>
        <span><strong>Runtime backed</strong> CoDriver aware</span>
      </div>
    </div>

    <div class="phone-card" aria-label="HWY mobile preview">
      <div class="phone-top"><span></span><strong>Today</strong><em>Live</em></div>
      <div class="metric big"><span>Available drivers</span><strong>14</strong></div>
      <div class="stack">
        <div><b>CoDriver</b><span>2 loads need review before dispatch.</span></div>
        <div><b>Permissions</b><span>Owner approved broker payment access.</span></div>
        <div><b>Compliance</b><span>3 documents expire this week.</span></div>
      </div>
      <div class="bottom-tabs"><span>Home</span><span>Loads</span><span>AI</span><span>Admin</span></div>
    </div>
  </section>

  <section class="section" id="platform">
    <div class="section-head">
      <span>Operating system</span>
      <h2>One place for people, work, money, and authority.</h2>
      <p>HWY separates frontend, backend, CoDriver, Moonrust, and reusable packages so the platform can grow without turning into a pile of screens.</p>
    </div>
    <div class="card-grid">
      {#each operatingCards as card}
        <article><h3>{card[0]}</h3><p>{card[1]}</p></article>
      {/each}
    </div>
  </section>

  <section class="section packages">
    <div class="section-head left">
      <span>Package-first foundation</span>
      <h2>Scaffolded for the whole system.</h2>
      <p>Auth, payments, UI, profiles, permissions, CoDriver contracts, and compliance become reusable packages instead of one-off route code.</p>
    </div>
    <div class="package-grid">
      {#each packageCards as card}
        <div><code>@hwy/{card[0]}</code><span>{card[1]}</span></div>
      {/each}
    </div>
  </section>

  <section class="cta-panel">
    <h2>Start with secure login, then invite the team.</h2>
    <p>Create the company owner account, manage users from Admin, and grow into packages without losing mobile-first speed.</p>
    <a class="primary" href="/signup">Create account</a>
  </section>
</main>

<style>
  .landing{min-height:100vh;background:#070a12;color:#eef4ff;overflow:hidden}.nav{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:14px;padding:14px 16px;background:rgba(7,10,18,.8);backdrop-filter:blur(16px);border-bottom:1px solid rgba(148,163,184,.12)}.brand{font-weight:950;color:white;letter-spacing:-.04em}.brand span{color:#60a5fa}.nav-actions{display:flex;align-items:center;gap:12px;font-size:13px}.nav-actions a{color:#a8b3c7}.nav-actions a:first-child{display:none}.nav-cta{background:#1d4ed8!important;color:white!important;border-radius:999px;padding:9px 12px;font-weight:800}
  .hero{display:grid;gap:30px;padding:46px 18px 64px;background:radial-gradient(circle at 15% 10%,rgba(37,99,235,.35),transparent 28%),radial-gradient(circle at 90% 30%,rgba(6,182,212,.16),transparent 28%)}.hero-copy{max-width:790px}.badge{display:inline-flex;padding:8px 10px;border-radius:999px;background:rgba(96,165,250,.12);border:1px solid rgba(96,165,250,.22);color:#bfdbfe;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.hero h1{font-size:clamp(40px,12vw,86px);line-height:.9;letter-spacing:-.075em;margin:18px 0}.hero p{font-size:17px;line-height:1.7;color:#b6c2d5;margin:0;max-width:720px}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}.primary,.secondary{display:inline-flex;align-items:center;justify-content:center;min-height:48px;border-radius:16px;padding:0 18px;font-weight:900}.primary{background:linear-gradient(135deg,#2563eb,#06b6d4);color:white;box-shadow:0 16px 40px rgba(37,99,235,.32)}.secondary{border:1px solid rgba(148,163,184,.24);color:#dbeafe;background:rgba(15,23,42,.65)}.proof-row{display:grid;gap:9px;color:#94a3b8}.proof-row span{padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06)}.proof-row strong{color:white;display:block}
  .phone-card{max-width:360px;margin:0 auto;width:100%;background:linear-gradient(180deg,#101827,#0a0f1c);border:1px solid rgba(148,163,184,.2);border-radius:34px;padding:16px;box-shadow:0 30px 90px rgba(0,0,0,.45),0 0 80px rgba(37,99,235,.18)}.phone-top{display:flex;align-items:center;justify-content:space-between;color:#cbd5e1}.phone-top span{width:52px;height:7px;background:#020617;border-radius:999px}.phone-top em{font-style:normal;color:#22c55e;font-size:12px}.metric.big{margin:22px 0;padding:20px;border-radius:24px;background:linear-gradient(135deg,#1d4ed8,#0891b2)}.metric span{display:block;color:#dbeafe}.metric strong{font-size:54px;letter-spacing:-.06em}.stack{display:grid;gap:10px}.stack div{padding:14px;border-radius:18px;background:#0f172a;border:1px solid rgba(148,163,184,.13)}.stack b,.stack span{display:block}.stack span{font-size:13px;color:#94a3b8;margin-top:4px}.bottom-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:14px;color:#93c5fd;font-size:11px;text-align:center}
  .section{padding:54px 18px}.section-head{text-align:center;max-width:760px;margin:0 auto 26px}.section-head.left{text-align:left;margin-left:0}.section-head span{color:#60a5fa;text-transform:uppercase;letter-spacing:.12em;font-weight:900;font-size:12px}.section h2,.cta-panel h2{font-size:clamp(28px,8vw,54px);line-height:1;letter-spacing:-.06em;margin:12px 0}.section p,.cta-panel p{color:#a8b3c7;line-height:1.65}.card-grid{display:grid;gap:12px}.card-grid article,.package-grid div{background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.13);border-radius:22px;padding:20px}.card-grid h3{margin:0 0 8px;font-size:20px}.card-grid p{margin:0}.packages{background:#0a0f1c}.package-grid{display:grid;gap:10px}.package-grid code{display:block;color:#93c5fd;font-weight:900;font-size:15px;margin-bottom:7px}.package-grid span{color:#a8b3c7;font-size:13px}.cta-panel{margin:18px;padding:28px;border-radius:30px;background:linear-gradient(135deg,rgba(37,99,235,.22),rgba(6,182,212,.11));border:1px solid rgba(96,165,250,.2);text-align:center}.cta-panel .primary{margin-top:12px}
  @media(min-width:760px){.nav{padding:16px 30px}.nav-actions a:first-child{display:inline}.hero{grid-template-columns:minmax(0,1.35fr) 390px;align-items:center;padding:82px 44px}.proof-row{grid-template-columns:repeat(3,1fr)}.section{padding:82px 44px}.card-grid{grid-template-columns:repeat(4,1fr)}.package-grid{grid-template-columns:repeat(3,1fr)}.cta-panel{margin:44px;padding:52px}}
</style>
