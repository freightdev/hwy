import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function persist(key, initial) {
  const stored = browser ? localStorage.getItem(key) : null;
  let data;
  if (stored !== null) {
    try { data = JSON.parse(stored); } catch { data = stored; }
  } else {
    data = initial;
  }
  const store = writable(data);
  if (browser) {
    store.subscribe(val => {
      if (typeof val === 'string') {
        localStorage.setItem(key, val);
      } else {
        localStorage.setItem(key, JSON.stringify(val));
      }
    });
  }
  return store;
}

export const token = persist('hwy_token', '');

export const onboarded = persist('hwy_onboarded', false);

export const company = persist('hwy_company', {
  name: '',
  mc: '',
  dot: '',
  scac: '',
  type: 'For-Hire Carrier',
  founded: '',
  address: '',
  city: '',
  state: '',
  zip: '',
  phone: '',
  email: '',
  website: '',
  fleet_size: '',
  trailer_types: [],
  operating_states: []
});

export const user = persist('hwy_user', {
  name: '',
  email: '',
  role: 'Owner',
  avatar: '',
  id: null,
  company_id: null
});
