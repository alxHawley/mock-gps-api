# User Setup Guide

This guide explains how to set up the Mock GPS API for your own use, including generating API keys and configuring your client applications.

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd mock-gps-api

# Copy the environment template
cp env.example .env

# Edit the .env file with your settings
nano .env
```

### 2. Generate API Key
The API requires authentication via API key. Generate a secure key:

```bash
# Generate a secure 64-character hex key
openssl rand -hex 32

# Or generate a 32-character base64 key
openssl rand -base64 32
```

### 3. Configure Environment
Edit your `.env` file:
```bash
# GPS API Security Configuration
GPS_API_KEY=your-generated-api-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
FLASK_ENV=production
FLASK_DEBUG=0
```

### 4. Add Your GPX Route
Place your GPX file in the project directory:
```bash
# Copy your GPX file (must be named 'route.gpx')
cp /path/to/your/route.gpx ./route.gpx
```

### 5. Start the API
```bash
# Start with Docker (recommended)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Client Application Setup

### Setting Up Your App to Use the API

#### 1. Store Your API Key Securely
```bash
# Option 1: Environment variable
export GPS_API_KEY="your-generated-api-key-here"

# Option 2: In your application config
# config.py
GPS_API_KEY = "your-generated-api-key-here"
```

#### 2. Make API Calls
```python
import requests
import os

# Get API key from environment
api_key = os.environ.get('GPS_API_KEY')

# API base URL
base_url = "http://localhost:5001"

# Headers for all requests
headers = {
    'X-API-Key': api_key,
    'Content-Type': 'application/json'
}

# Get user location
response = requests.get(f"{base_url}/user_location", headers=headers)
user_location = response.json()
print(f"User: {user_location}")

# Get dog location
response = requests.get(f"{base_url}/dog_location", headers=headers)
dog_location = response.json()
print(f"Dog: {dog_location}")

# Start tracking
response = requests.post(f"{base_url}/start_tracking", headers=headers)
print(response.json())
```

#### 3. JavaScript/Node.js Example
```javascript
const axios = require('axios');

const API_KEY = process.env.GPS_API_KEY || 'your-generated-api-key-here';
const BASE_URL = 'http://localhost:5001';

const headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
};

// Get user location
async function getUserLocation() {
    try {
        const response = await axios.get(`${BASE_URL}/user_location`, { headers });
        return response.data;
    } catch (error) {
        console.error('Error getting user location:', error.response?.data);
    }
}

// Get dog location
async function getDogLocation() {
    try {
        const response = await axios.get(`${BASE_URL}/dog_location`, { headers });
        return response.data;
    } catch (error) {
        console.error('Error getting dog location:', error.response?.data);
    }
}

// Start tracking
async function startTracking() {
    try {
        const response = await axios.post(`${BASE_URL}/start_tracking`, {}, { headers });
        return response.data;
    } catch (error) {
        console.error('Error starting tracking:', error.response?.data);
    }
}
```

## API Key Management

### Security Best Practices

1. **Never commit API keys to version control**
   ```bash
   # Add .env to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**
   ```bash
   # Set in your deployment environment
   export GPS_API_KEY="your-production-api-key"
   ```

3. **Rotate keys regularly**
   ```bash
   # Generate new key
   openssl rand -hex 32
   
   # Update .env file
   # Restart API service
   docker-compose restart
   ```

4. **Monitor API usage**
   ```bash
   # Check API logs
   docker-compose logs -f | grep "API"
   ```

### Multiple API Keys

If you need multiple API keys for different clients:

1. **Use a reverse proxy** (nginx/traefik) with API key routing
2. **Implement key management** in your application
3. **Use environment-specific keys** for different deployments

## Testing Your Setup

### 1. Test API Connectivity
```bash
# Test with curl
curl -H "X-API-Key: your-generated-api-key-here" http://localhost:5001/user_location
```

### 2. Test Complete Workflow
```bash
# Set your API key
export API_KEY="your-generated-api-key-here"

# Test user location
curl -H "X-API-Key: $API_KEY" http://localhost:5001/user_location

# Start tracking
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/start_tracking

# Test dog location
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location

# Stop tracking
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/stop_tracking
```

### 3. Monitor API Health
```bash
# Check container health
docker-compose ps

# View real-time logs
docker-compose logs -f

# Test API endpoints
./monitor.sh
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check API key is correct
   - Verify X-API-Key header is being sent
   - Ensure .env file is properly configured

2. **API not responding**
   - Check container status: `docker-compose ps`
   - View logs: `docker-compose logs -f`
   - Restart service: `docker-compose restart`

3. **GPX file not found**
   - Ensure `route.gpx` exists in project directory
   - Check file permissions
   - Verify file is valid GPX format

4. **Port already in use**
   - Change port in `docker-compose.yml`
   - Stop conflicting services
   - Use different port mapping

### Getting Help

- Check the [API Documentation](docs/public/API.md) for endpoint details
- Review [Deployment Guide](docs/internal/DEPLOYMENT.md) for production setup
- Check container logs for error messages
- Verify all environment variables are set correctly

## Production Deployment

For production use, consider:

1. **Use a reverse proxy** (nginx/traefik) for SSL termination
2. **Set up monitoring** (Prometheus/Grafana)
3. **Use container orchestration** (Kubernetes/Docker Swarm)
4. **Implement logging** and log aggregation
5. **Set up backups** for your GPX files
6. **Use secrets management** for API keys

See the [Deployment Guide](docs/internal/DEPLOYMENT.md) for detailed production setup instructions.
