<script>
  import BottomNav from '$lib/components/BottomNav.svelte';
  import { token } from '$lib/stores/app.js';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { get, clearToken } from '$lib/api.js';
  import { browser } from '$app/environment';

  onMount(async () => {
    const t = browser ? (localStorage.getItem('hwy_token') || $token) : $token;
    if (!t) {
      goto('/login');
      return;
    }
    const { error: err } = await get('/auth/me');
    if (err) {
      clearToken();
      token.set('');
      goto('/login');
    }
  });
</script>

<slot />
<BottomNav />
