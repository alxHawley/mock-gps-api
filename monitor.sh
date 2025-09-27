#!/bin/bash

# Mock GPS API Monitoring Script

echo "=== Mock GPS API Status ==="
echo ""

# Check Docker container status
echo "Docker Container Status:"
docker-compose ps
echo ""

# Check if API is responding
echo "API Health Check:"
if curl -s -H "X-API-Key: $API_KEY" http://localhost:5001/user_location > /dev/null; then
    echo "✅ API is responding"
    echo "User location: $(curl -s -H "X-API-Key: $API_KEY" http://localhost:5001/user_location)"
else
    echo "❌ API is not responding"
    echo "Note: Set API_KEY environment variable to test API endpoints"
fi
echo ""

# Check systemd service status
echo "Systemd Service Status:"
sudo systemctl status mock-gps-api.service --no-pager -l
echo ""

# Show recent logs
echo "Recent Docker Logs:"
docker-compose logs --tail=10
