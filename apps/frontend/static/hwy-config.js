// Runtime browser config override.
//
// This file is intentionally tiny and safe to edit. It lets an agent or operator
// switch API endpoints without hunting through Svelte route components.
// Values here are only public browser config; never put secrets here.
window.HWY_LOCAL_API_BASE_URL = window.HWY_LOCAL_API_BASE_URL || 'http://localhost:18000/api/v1';
window.HWY_PUBLIC_API_BASE_URL = window.HWY_PUBLIC_API_BASE_URL || 'https://api.hwytms.com/api/v1';
