# Deployment Guide

This guide explains how to deploy the Mock GPS API to run 24/7 on your machine.

## Current Status ✅

- ✅ Docker container built and running
- ✅ API responding on http://localhost:5001
- ✅ Systemd service configured for auto-startup
- ✅ Management scripts created

## Quick Commands

### Management Scripts
```bash
# Start the service
./manage.sh start

# Stop the service  
./manage.sh stop

# Restart the service
./manage.sh restart

# View logs
./manage.sh logs

# Check status
./manage.sh status

# Build Docker image
./manage.sh build
```

### Monitoring
```bash
# Check overall health and status
./monitor.sh
```

### Systemd Service
```bash
# Start service manually
sudo systemctl start mock-gps-api.service

# Stop service manually
sudo systemctl stop mock-gps-api.service

# Check service status
sudo systemctl status mock-gps-api.service

# View service logs
sudo journalctl -u mock-gps-api.service -f
```

## API Endpoints & Testing

### Endpoint Overview
- `GET /user_location` - Get current user position
- `GET /dog_location` - Get current dog position (returns null when hidden)
- `GET /user_follow_location` - Same as user_location
- `POST /start_tracking` - Show dog on map
- `POST /stop_tracking` - Hide dog from map

### CURL Commands for Testing

**Note:** All API endpoints now require authentication. Add the `X-API-Key` header to your requests:

```bash
# Set your API key (replace with your actual key)
export API_KEY="your-secret-api-key-change-this"
```

#### Get User Location
```bash
curl -H "X-API-Key: $API_KEY" http://localhost:5001/user_location
```

#### Get Dog Location (when hidden)
```bash
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
```

#### Start Tracking (show dog)
```bash
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/start_tracking
```

#### Get Dog Location (when visible)
```bash
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
```

#### Stop Tracking (hide dog)
```bash
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/stop_tracking
```

#### Get User Follow Location
```bash
curl -H "X-API-Key: $API_KEY" http://localhost:5001/user_follow_location
```

### Quick Test Sequence
```bash
# Test complete workflow
export API_KEY="your-secret-api-key-change-this"
curl -H "X-API-Key: $API_KEY" http://localhost:5001/user_location
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/start_tracking
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:5001/stop_tracking
curl -H "X-API-Key: $API_KEY" http://localhost:5001/dog_location
```

## Auto-Startup

The service is configured to start automatically when the system boots:

1. **Systemd Service**: `mock-gps-api.service` is enabled and will start on boot
2. **Docker Compose**: Uses `restart: unless-stopped` for container resilience
3. **Health Checks**: Built-in health monitoring

## Troubleshooting

### If API is not responding:
1. Check container status: `docker-compose ps`
2. View logs: `docker-compose logs -f`
3. Restart: `./manage.sh restart`

### If service doesn't start on boot:
1. Check systemd: `sudo systemctl status mock-gps-api.service`
2. View logs: `sudo journalctl -u mock-gps-api.service -f`
3. Re-enable: `sudo systemctl enable mock-gps-api.service`

### If Docker issues:
1. Check Docker service: `sudo systemctl status docker`
2. Restart Docker: `sudo systemctl restart docker`
3. Rebuild container: `./manage.sh build`

## Configuration

- **Port**: 5001 (configurable in docker-compose.yml)
- **Update Interval**: 1 second (configurable in app.py)
- **Dog Ahead Delay**: 15 seconds (configurable in app.py)
- **GPX File**: route.gpx (mounted as volume)

## Security Configuration

### Security Features Implemented

1. **API Key Authentication**: All endpoints require a valid API key
2. **Host-based Access Control**: Only allowed IPs can access the API
3. **Non-root Docker Container**: Runs as dedicated `appuser`
4. **Read-only File System**: Container filesystem is read-only
5. **Network Isolation**: Internal Docker network with no external access
6. **Security Headers**: XSS protection, content type options, etc.
7. **UFW Firewall**: Restrictive firewall policies
8. **Localhost Binding**: API only accessible from localhost

### Security Setup

#### 1. Environment Configuration
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and set a strong API key
nano .env
```

#### 2. Firewall Setup
```bash
# Run the security setup script (requires sudo)
sudo chmod +x security-setup.sh
sudo ./security-setup.sh
```

#### 3. Tailscale Security
- **Use Tailscale ACLs**: Restrict access to specific users/devices
- **Enable MagicDNS**: Use hostnames instead of IPs
- **Audit Logs**: Monitor Tailscale access logs
- **Subnet Routes**: Only route necessary subnets

#### 4. Application Security
- **API Key**: Use a strong, unique key for each environment
- **Host Filtering**: Only allow trusted IPs
- **Rate Limiting**: Consider adding rate limiting for production
- **Logging**: Monitor API access logs

### Security Monitoring

#### Check Security Status
```bash
# Check UFW status
sudo ufw status

# Check Docker security
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image mock-gps-api_mock-gps-api:latest

# Check container logs for security events
docker-compose logs | grep -i "error\|denied\|unauthorized"
```

#### Recommended Additional Security
- **Fail2ban**: Install for brute force protection
- **Log Monitoring**: Set up centralized logging
- **Regular Updates**: Keep Docker and system packages updated
- **Backup Strategy**: Regular backups of configuration
- **Network Segmentation**: Isolate API server from other services

### Security Considerations

- **API Key Management**: Store keys securely, rotate regularly
- **Network Access**: Only expose necessary ports
- **Monitoring**: Set up alerts for suspicious activity
- **Updates**: Keep all components updated
- **Auditing**: Regular security audits of the setup
