import { writable } from 'svelte/store';

export const toasts = writable([]);

let id = 0;

export function toast(message, type = 'info', duration = 3500) {
  const t = { id: id++, message, type };
  toasts.update(all => [...all, t]);
  setTimeout(() => dismiss(t.id), duration);
}

export function dismiss(id) {
  toasts.update(all => all.filter(t => t.id !== id));
}

export const success = (msg) => toast(msg, 'success');
export const error = (msg) => toast(msg, 'error');
export const info = (msg) => toast(msg, 'info');
export const warn = (msg) => toast(msg, 'warn');
export const api = (feature) => toast(`${feature} requires API integration`, 'api');
