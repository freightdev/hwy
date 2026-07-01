export const hwyFrontendConfig = {
  devHost: '0.0.0.0',
  devPort: 5173,
  localApiBaseUrl: 'http://localhost:18000/api/v1',
  publicApiBaseUrl: 'https://api.hwytms.com/api/v1',
  viteProxyTarget: 'http://backend:8000',
  allowedHosts: [
    'localhost',
    '127.0.0.1',
    'hwytms.com',
    'www.hwytms.com',
    'api.hwytms.com',
    'codriver.hwytms.com'
  ]
};
