<script>
  import { page } from '$app/stores';

  $: path = $page.url.pathname;

  const tabs = [
    { href: '/app/dashboard',        label: 'Me',      icon: '👤' },
    { href: '/app/connect',          label: 'Connect',  icon: '🔗' },
    { href: '/app/ai',               label: 'AI',       icon: '✦', center: true },
    { href: '/app/connect/loadboard',label: 'Loads',    icon: '📦' },
    { href: '/app/more',             label: 'More',     icon: '⋯' },
  ];

  // Loads tab is active for loadboard but NOT for the broader connect section
  function isActive(tab) {
    if (tab.href === '/app/connect/loadboard') return path === '/app/connect/loadboard';
    if (tab.href === '/app/connect') return path.startsWith('/app/connect') && path !== '/app/connect/loadboard';
    return path.startsWith(tab.href);
  }
</script>

<nav class="bottom-nav">
  {#each tabs as tab}
    <a
      href={tab.href}
      class="nav-item"
      class:active={isActive(tab)}
      class:center={tab.center}
    >
      <span class="nav-icon">{tab.icon}</span>
      <span class="nav-label">{tab.label}</span>
    </a>
  {/each}
</nav>

<style>
  .bottom-nav {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 64px;
    background: #0d0f14;
    border-top: 1px solid #1e2330;
    display: flex;
    align-items: center;
    z-index: 100;
    padding-bottom: env(safe-area-inset-bottom);
  }

  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    text-decoration: none;
    color: #4a5568;
    transition: color 0.15s;
    height: 100%;
    position: relative;
  }

  .nav-item.active { color: #3b82f6; }
  .nav-item:hover  { color: #6b7280; }

  .nav-icon  { font-size: 18px; line-height: 1; }
  .nav-label { font-size: 10px; font-weight: 500; letter-spacing: 0.02em; }

  .nav-item.center .nav-icon {
    background: #3b82f6;
    color: #fff;
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-top: -16px;
    box-shadow: 0 0 20px rgba(59,130,246,0.4);
  }

  .nav-item.center.active .nav-icon {
    background: #2563eb;
  }
</style>
