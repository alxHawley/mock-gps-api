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
if curl -s -H "X-API-Key: 5bd5a5838868668c66bc265afb1036064ada1a6e0bb843f8624346cca360c6e3" http://localhost:5001/user_location > /dev/null; then
    echo "✅ API is responding"
    echo "User location: $(curl -s -H "X-API-Key: 5bd5a5838868668c66bc265afb1036064ada1a6e0bb843f8624346cca360c6e3" http://localhost:5001/user_location)"
else
    echo "❌ API is not responding"
fi
echo ""

# Check systemd service status
echo "Systemd Service Status:"
sudo systemctl status mock-gps-api.service --no-pager -l
echo ""

# Show recent logs
echo "Recent Docker Logs:"
docker-compose logs --tail=10 