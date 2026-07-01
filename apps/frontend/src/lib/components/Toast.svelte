<script>
  import { toasts, dismiss } from '$lib/stores/toast.js';
</script>

<div class="toast-container">
  {#each $toasts as t (t.id)}
    <div class="toast toast--{t.type}" role="alert">
      <span class="toast-icon">
        {#if t.type === 'success'}✓{:else if t.type === 'error'}✕{:else if t.type === 'warn'}⚠{:else if t.type === 'api'}⚡{:else}ℹ{/if}
      </span>
      <span class="toast-msg">{t.message}</span>
      <button class="toast-close" on:click={() => dismiss(t.id)}>✕</button>
    </div>
  {/each}
</div>

<style>
  .toast-container {
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: min(92vw, 400px);
    pointer-events: none;
  }

  .toast {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    pointer-events: all;
    animation: slideUp 0.2s ease;
    border: 1px solid transparent;
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .toast--success { background: #0f2b1a; border-color: #22c55e; color: #22c55e; }
  .toast--error   { background: #2b0f0f; border-color: #ef4444; color: #ef4444; }
  .toast--warn    { background: #2b1e0f; border-color: #f59e0b; color: #f59e0b; }
  .toast--api     { background: #1a1040; border-color: #818cf8; color: #818cf8; }
  .toast--info    { background: #0f1e2b; border-color: #3b82f6; color: #3b82f6; }

  .toast-icon { font-size: 14px; flex-shrink: 0; }
  .toast-msg  { flex: 1; color: inherit; }
  .toast-close {
    background: none; border: none; cursor: pointer;
    color: inherit; opacity: 0.6; font-size: 11px; padding: 2px;
    flex-shrink: 0;
  }
  .toast-close:hover { opacity: 1; }
</style>
