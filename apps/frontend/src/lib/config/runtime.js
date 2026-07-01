export const runtimeConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  localApiBaseUrl: import.meta.env.VITE_LOCAL_API_BASE_URL || 'http://localhost:18000/api/v1',
  publicApiBaseUrl: import.meta.env.VITE_PUBLIC_API_BASE_URL || 'https://api.hwytms.com/api/v1',
};

export function browserApiBase(hostname = globalThis?.location?.hostname || '') {
  if (hostname === 'localhost' || hostname === '127.0.0.1') return runtimeConfig.localApiBaseUrl;
  return runtimeConfig.publicApiBaseUrl;
}
