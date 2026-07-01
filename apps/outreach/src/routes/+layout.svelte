<slot />

<style>
  :global(*) { box-sizing: border-box; }
  :global(html) { scroll-behavior: smooth; }
  :global(body) {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #111827;
    background: #f8fafc;
  }
  :global(a) { color: inherit; }
  :global(.shell) { min-height: 100vh; }
  :global(.hero) {
    background:
      radial-gradient(circle at top left, rgba(249, 115, 22, 0.22), transparent 34rem),
      linear-gradient(135deg, #0f172a 0%, #111827 55%, #1e293b 100%);
    color: white;
    padding: 1.2rem clamp(1rem, 4vw, 4rem) 5rem;
  }
  :global(.nav) {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    max-width: 1160px;
    margin: 0 auto 4rem;
  }
  :global(.nav strong) { font-size: 1.35rem; letter-spacing: -0.04em; }
  :global(.nav a) { color: #fed7aa; text-decoration: none; font-weight: 700; }
  :global(.hero-grid) {
    display: grid;
    grid-template-columns: minmax(0, 1.25fr) minmax(18rem, 0.75fr);
    gap: 2rem;
    align-items: stretch;
    max-width: 1160px;
    margin: 0 auto;
  }
  :global(.eyebrow) {
    color: #f97316;
    font-size: .78rem;
    font-weight: 900;
    letter-spacing: .16em;
    text-transform: uppercase;
  }
  :global(h1), :global(h2), :global(h3), :global(p) { margin-top: 0; }
  :global(h1) { max-width: 760px; font-size: clamp(2.6rem, 7vw, 5.8rem); line-height: .9; letter-spacing: -0.075em; margin-bottom: 1.3rem; }
  :global(h2) { font-size: clamp(2rem, 4vw, 3.4rem); line-height: 1; letter-spacing: -0.06em; margin-bottom: 1rem; }
  :global(h3) { font-size: 1.35rem; letter-spacing: -0.04em; }
  :global(.lead) { max-width: 680px; color: #dbeafe; font-size: clamp(1.08rem, 2vw, 1.35rem); line-height: 1.65; }
  :global(.actions) { display: flex; gap: .8rem; flex-wrap: wrap; margin-top: 2rem; }
  :global(.button) {
    border: 0;
    border-radius: 999px;
    padding: .9rem 1.25rem;
    font-weight: 900;
    text-decoration: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  :global(.button.primary) { background: #f97316; color: white; box-shadow: 0 18px 35px rgba(249, 115, 22, .32); }
  :global(.button.secondary) { background: rgba(255,255,255,.12); color: white; border: 1px solid rgba(255,255,255,.22); }
  :global(.proof-card) {
    background: rgba(15, 23, 42, .72);
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 2rem;
    padding: 2rem;
    box-shadow: 0 24px 60px rgba(0,0,0,.28);
    backdrop-filter: blur(14px);
  }
  :global(.proof-card span) { color: #fdba74; font-weight: 900; text-transform: uppercase; letter-spacing: .14em; font-size: .75rem; }
  :global(.proof-card p), :global(.proof-card li) { color: #cbd5e1; line-height: 1.6; }
  :global(.proof-card ul) { padding-left: 1.15rem; margin-bottom: 0; }
  :global(.section) { max-width: 1160px; margin: 0 auto; padding: clamp(3rem, 7vw, 6rem) clamp(1rem, 4vw, 2rem); }
  :global(.cards) { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-top: 2rem; }
  :global(.card), :global(form), :global(.success), :global(.steps) {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 1.4rem;
    padding: 1.35rem;
    box-shadow: 0 16px 38px rgba(15, 23, 42, .07);
  }
  :global(.card p), :global(.section p) { color: #475569; line-height: 1.7; }
  :global(.split), :global(.contact) { display: grid; grid-template-columns: .9fr 1.1fr; gap: 2rem; align-items: start; }
  :global(.steps) { margin: 0; list-style: none; display: grid; gap: .75rem; }
  :global(.steps li) { display: flex; gap: .8rem; align-items: center; font-weight: 800; }
  :global(.steps span) { width: 2rem; height: 2rem; border-radius: 999px; background: #111827; color: white; display: inline-grid; place-items: center; flex: 0 0 auto; }
  :global(form) { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
  :global(label) { display: grid; gap: .4rem; font-weight: 800; color: #1f2937; }
  :global(label.full) { grid-column: 1 / -1; }
  :global(input), :global(select), :global(textarea) {
    width: 100%;
    border: 1px solid #cbd5e1;
    border-radius: .85rem;
    padding: .85rem .95rem;
    font: inherit;
    background: #f8fafc;
  }
  :global(textarea) { resize: vertical; }
  :global(small), :global(.error) { color: #dc2626; font-weight: 800; }
  :global(form button) { justify-self: start; }
  :global(.success) { border-color: #86efac; background: #f0fdf4; }
  @media (max-width: 800px) {
    :global(.nav) { align-items: flex-start; flex-direction: column; margin-bottom: 2.5rem; }
    :global(.hero-grid), :global(.split), :global(.contact), :global(.cards), :global(form) { grid-template-columns: 1fr; }
    :global(.hero) { padding-bottom: 3rem; }
    :global(h1) { font-size: 3rem; }
  }
</style>
