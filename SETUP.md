# Mock GPS API - Setup Guide

This guide explains how to set up the Mock GPS API for development and production use.

## Prerequisites

- Docker and Docker Compose installed
- `route.gpx` file in the project directory

## Quick Setup

### 1. Clone and Configure
```bash
# Clone the repository
git clone <repository-url>
cd mock-gps-api

# Copy environment template
cp env.example .env

# Edit the .env file with your API key
nano .env
```

### 2. Set API Key
Edit the `.env` file and set a strong API key:
```
GPS_API_KEY=your-super-secret-api-key-change-this-immediately
```

### 3. Start the Service
```bash
# Start the API
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Management

### Basic Commands
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
```

### Monitoring
```bash
# Check API health
./monitor.sh

# Note: Set API_KEY environment variable for full monitoring
export API_KEY="your-api-key"
./monitor.sh
```

## Configuration

### Environment Variables
- `GPS_API_KEY` - API key for authentication
- `ALLOWED_HOSTS` - Comma-separated list of allowed IPs

### Docker Configuration
- **Port**: 5001 (configurable in docker-compose.yml)
- **Update Interval**: 1 second
- **Dog Ahead Delay**: 15 seconds
- **GPX File**: route.gpx (mounted as volume)

## Troubleshooting

### Common Issues

1. **API not responding**
   - Check container status: `docker-compose ps`
   - View logs: `docker-compose logs -f`
   - Restart: `./manage.sh restart`

2. **Authentication errors**
   - Verify API key in `.env` file
   - Check that X-API-Key header is being sent

3. **Docker issues**
   - Check Docker service: `sudo systemctl status docker`
   - Restart Docker: `sudo systemctl restart docker`
   - Rebuild container: `./manage.sh build`

## Security

- Use a strong, unique API key
- Keep the `.env` file secure and never commit it
- Consider using environment variables for production
- Monitor API access logs regularly
