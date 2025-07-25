# Insomnia Environment Configuration

## Development Environment

```json
{
  "name": "Development",
  "data": {
    "base_url": "http://localhost:8000",
    "api_version": "v1"
  }
}
```

## Staging Environment

```json
{
  "name": "Staging",
  "data": {
    "base_url": "https://staging-api.unboxed.ai",
    "api_version": "v1"
  }
}
```

## Production Environment

```json
{
  "name": "Production",
  "data": {
    "base_url": "https://api.unboxed.ai",
    "api_version": "v1"
  }
}
```

## How to Import:

1. Open Insomnia
2. Go to Settings → Manage Environments
3. Click "Create Environment"
4. Copy and paste the JSON above
5. Save the environment

## Usage in Requests:

- URL: `{{ _.base_url }}/health`
- URL: `{{ _.base_url }}/ask`
- Header: `Content-Type: application/json`
