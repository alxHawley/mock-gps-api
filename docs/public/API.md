# API Documentation

This document describes the API endpoints and usage for the Mock GPS API.

## Overview

The Mock GPS API provides simulated GPS location data for testing and demonstration purposes. All endpoints require API key authentication.

## Authentication

All API endpoints require the `X-API-Key` header for authentication:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:5001/endpoint
```

## Endpoints

### Get User Location
```http
GET /user_location
Headers: X-API-Key: <api_key>
```

**Response:**
```json
{
  "lat": 47.654277328401804,
  "lon": -122.40892767906189
}
```

### Get Dog Location
```http
GET /dog_location
Headers: X-API-Key: <api_key>
```

**Response (when tracking):**
```json
{
  "lat": 47.65465979464352,
  "lon": -122.40788178518414
}
```

**Response (when not tracking):**
```json
{
  "lat": null,
  "lon": null
}
```

### Start Tracking
```http
POST /start_tracking
Headers: X-API-Key: <api_key>
```

**Response:**
```json
{
  "status": "tracking started"
}
```

### Stop Tracking
```http
POST /stop_tracking
Headers: X-API-Key: <api_key>
```

**Response:**
```json
{
  "status": "tracking stopped"
}
```

### Get User Follow Location
```http
GET /user_follow_location
Headers: X-API-Key: <api_key>
```

**Response:**
```json
{
  "lat": 47.654277328401804,
  "lon": -122.40892767906189
}
```

## Testing Examples

### Complete Workflow Test
```bash
# Set your API key
export API_KEY="your-secret-api-key-change-this"

# Test user location
curl -H "X-API-Key: $API_KEY" http://localhost:5001/user_location

# Test dog location (should be null initially)
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location

# Start tracking
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/start_tracking

# Test dog location (should now have coordinates)
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location

# Stop tracking
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/stop_tracking

# Test dog location (should be null again)
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "API key required"
}
```

### 403 Forbidden
```json
{
  "error": "Invalid API key"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. See the [Security Guide](../internal/SECURITY.md) for details.

## Configuration

See the [Deployment Guide](../internal/DEPLOYMENT.md) for configuration options and environment variables.
