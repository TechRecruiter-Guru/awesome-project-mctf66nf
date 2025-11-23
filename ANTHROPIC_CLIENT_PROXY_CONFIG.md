# Anthropic Client Proxy Configuration

## Issue
The error "Client.init() got an unexpected keyword argument 'proxies'" indicates an attempt to pass a `proxies` parameter to the Anthropic client initialization, which is not supported.

## Root Cause
The Anthropic SDK (both TypeScript and Python versions) does **NOT** support a `proxies` parameter in the client constructor.

## Correct Proxy Configuration

### For TypeScript SDK (@anthropic-ai/sdk)

If you need to use a proxy with the Anthropic TypeScript SDK, you should:

1. **Use environment variables** (recommended):
   ```bash
   export HTTP_PROXY=http://proxy.example.com:8080
   export HTTPS_PROXY=http://proxy.example.com:8080
   ```

2. **Or configure httpAgent** (advanced):
   ```typescript
   import Anthropic from '@anthropic-ai/sdk';
   import { HttpsProxyAgent } from 'https-proxy-agent';

   const proxyAgent = new HttpsProxyAgent('http://proxy.example.com:8080');

   const client = new Anthropic({
     apiKey: process.env.ANTHROPIC_API_KEY,
     httpAgent: proxyAgent,
   });
   ```

### For Python SDK (anthropic)

If using the Python version:

1. **Use environment variables** (recommended):
   ```bash
   export HTTP_PROXY=http://proxy.example.com:8080
   export HTTPS_PROXY=http://proxy.example.com:8080
   ```

2. **Or configure custom httpx client** (advanced):
   ```python
   import httpx
   from anthropic import Anthropic

   httpx_client = httpx.Client(proxies={
       "http://": "http://proxy.example.com:8080",
       "https://": "http://proxy.example.com:8080",
   })

   client = Anthropic(
       api_key="your-api-key",
       http_client=httpx_client,
   )
   ```

## What NOT to Do

❌ **NEVER** try to pass `proxies` directly to the constructor:
```typescript
// This will FAIL:
new Anthropic({
  apiKey: apiKey,
  proxies: {...}  // ❌ NOT SUPPORTED
});
```

## Current Implementation

The current implementation in `lib/claude.ts` correctly initializes the client without any proxy parameters. If proxy support is needed, use the methods documented above.

## Fix Applied

- Updated `lib/claude.ts` to explicitly use `Anthropic.ClientOptions` type
- Added documentation comments about proxy configuration
- Ensured no `proxies` parameter is passed to the constructor

## Testing

After this fix, the Anthropic client will initialize correctly. If you need proxy support in your environment, configure it using environment variables as described above.
