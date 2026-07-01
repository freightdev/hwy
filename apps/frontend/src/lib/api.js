import { browser } from '$app/environment';
import { runtimeConfig } from '$lib/config/runtime.js';

const BASE = runtimeConfig.apiBaseUrl;

let _token = '';

export function setToken(t) {
  _token = t;
  if (browser) localStorage.setItem('hwy_token', t);
}

export function clearToken() {
  _token = '';
  if (browser) localStorage.removeItem('hwy_token');
}

function getToken() {
  if (browser) {
    _token = localStorage.getItem('hwy_token') || '';
  }
  return _token;
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  try {
    const res = await fetch(`${BASE}${path}`, {
      ...options,
      headers,
    });
    if (res.status === 401) {
      clearToken();
      return { data: null, error: 'Session expired — please sign in again' };
    }
    const json = await res.json();
    if (!res.ok) {
      return { data: null, error: json.error || `Request failed (${res.status})` };
    }
    return { data: json.data, error: null };
  } catch (err) {
    return { data: null, error: 'Network error — check your connection' };
  }
}

export function get(path) {
  return request(path);
}

export function post(path, body) {
  return request(path, { method: 'POST', body: JSON.stringify(body) });
}

export function put(path, body) {
  return request(path, { method: 'PUT', body: JSON.stringify(body) });
}

export function patch(path, body) {
  return request(path, { method: 'PATCH', body: JSON.stringify(body) });
}

export function del(path) {
  return request(path, { method: 'DELETE' });
}
