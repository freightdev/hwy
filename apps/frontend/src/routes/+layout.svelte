<script>
  import Toast from '$lib/components/Toast.svelte';
</script>

<slot />
<Toast />

<style>
  :global(*, *::before, *::after) { box-sizing: border-box; margin: 0; padding: 0; }
  :global(html, body) {
    background: #0d0f14;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
    font-size: 15px;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
  }
  :global(a) { text-decoration: none; color: inherit; }
  :global(button) { cursor: pointer; font-family: inherit; }
  :global(input, select, textarea) {
    font-family: inherit;
    background: #1e2330;
    border: 1px solid #2d3548;
    color: #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    width: 100%;
    outline: none;
    transition: border-color 0.15s;
  }
  :global(input:focus, select:focus, textarea:focus) {
    border-color: #3b82f6;
  }
  :global(input::placeholder, textarea::placeholder) { color: #4a5568; }

  :global(.btn) {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 11px 20px;
    border-radius: 10px;
    border: none;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.15s;
    cursor: pointer;
  }
  :global(.btn-primary) { background: #3b82f6; color: #fff; }
  :global(.btn-primary:hover) { background: #2563eb; }
  :global(.btn-secondary) { background: #1e2330; color: #e2e8f0; border: 1px solid #2d3548; }
  :global(.btn-secondary:hover) { background: #252d3d; }
  :global(.btn-danger) { background: #7f1d1d; color: #fca5a5; }
  :global(.btn-danger:hover) { background: #991b1b; }
  :global(.btn-full) { width: 100%; }
  :global(.btn-sm) { padding: 7px 14px; font-size: 12px; }

  :global(.card) {
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 14px;
    padding: 16px;
  }

  :global(.label) {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 6px;
    display: block;
  }

  :global(.chip) {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
  }
  :global(.chip-green)  { background: #0f2b1a; color: #22c55e; }
  :global(.chip-blue)   { background: #0f1e2b; color: #3b82f6; }
  :global(.chip-orange) { background: #2b1e0f; color: #f59e0b; }
  :global(.chip-red)    { background: #2b0f0f; color: #ef4444; }
  :global(.chip-gray)   { background: #1e2330; color: #6b7280; }

  :global(.divider) { border: none; border-top: 1px solid #1e2330; margin: 12px 0; }

  :global(.page) {
    min-height: 100vh;
    padding-bottom: 80px;
  }

  :global(.page-header) {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    border-bottom: 1px solid #1e2330;
    position: sticky;
    top: 0;
    background: #0d0f14;
    z-index: 50;
  }

  :global(.page-title) {
    font-size: 17px;
    font-weight: 700;
  }

  :global(.back-btn) {
    background: none;
    border: none;
    color: #3b82f6;
    font-size: 22px;
    padding: 0;
    line-height: 1;
  }

  :global(.section) { padding: 16px; }
  :global(.section + .section) { padding-top: 0; }

  :global(.row) { display: flex; gap: 10px; }
  :global(.col) { flex: 1; min-width: 0; }

  :global(.form-group) { margin-bottom: 14px; }

  :global(.stat-box) {
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
  }
  :global(.stat-val) { font-size: 20px; font-weight: 700; color: #e2e8f0; }
  :global(.stat-lbl) { font-size: 10px; color: #4a5568; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }

  :global(.list-item) {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-bottom: 1px solid #1e2330;
    transition: background 0.1s;
  }
  :global(.list-item:hover) { background: #161a23; }
  :global(.list-item:last-child) { border-bottom: none; }

  :global(.avatar) {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: #1e2330;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    font-weight: 600;
    color: #3b82f6;
  }

  :global(.toggle) {
    position: relative;
    width: 44px; height: 24px;
    background: #2d3548;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
    flex-shrink: 0;
  }
  :global(.toggle.on) { background: #3b82f6; }
  :global(.toggle::after) {
    content: '';
    position: absolute;
    top: 2px; left: 2px;
    width: 20px; height: 20px;
    background: #fff;
    border-radius: 50%;
    transition: transform 0.2s;
  }
  :global(.toggle.on::after) { transform: translateX(20px); }

  :global(.hwy-logo) {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
  }
  :global(.hwy-logo span) { color: #3b82f6; }

  :global(.empty-state) {
    text-align: center;
    padding: 48px 24px;
    color: #4a5568;
  }
  :global(.empty-state .icon) { font-size: 40px; margin-bottom: 12px; }
  :global(.empty-state p) { font-size: 13px; }

  :global(.search-bar) {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #161a23;
    border: 1px solid #1e2330;
    border-radius: 10px;
    padding: 8px 12px;
    margin: 12px 16px;
  }
  :global(.search-bar input) {
    background: none; border: none; padding: 0;
    font-size: 14px; flex: 1;
  }
</style>
