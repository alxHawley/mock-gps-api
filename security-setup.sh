#!/bin/bash

# Mock GPS API Security Setup Script
# This script configures the GPS API machine (k8s-control-plane) for secure API access

echo "🔒 Setting up security for Mock GPS API (k8s-control-plane)..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install UFW if not installed
if ! command -v ufw &> /dev/null; then
    echo "🔧 Installing UFW firewall..."
    apt install -y ufw
fi

# Configure UFW
echo "🔥 Configuring UFW firewall..."

# Reset UFW to default
ufw --force reset

# Set default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (adjust port if needed)
ufw allow ssh

# Allow Tailscale
ufw allow in on tailscale0
ufw allow out on tailscale0

# Allow inbound connections from tracker app machine (portable-dev)
ufw allow from 100.110.187.41 to any port 5001

# Allow inbound connections from admin-workstation for monitoring/management
ufw allow from 100.122.121.32 to any port 5001

# Allow localhost connections (for API)
ufw allow from 127.0.0.1 to any port 5001

# Allow Docker internal network
ufw allow from 172.16.0.0/12
ufw allow from 192.168.0.0/16

# Enable UFW
ufw --force enable

echo "✅ UFW firewall configured and enabled"

# Create dedicated user for Docker (optional)
echo "👤 Creating dedicated user for Docker operations..."
useradd -m -s /bin/bash dockeruser || echo "User dockeruser already exists"
usermod -aG docker dockeruser

# Set up log monitoring
echo "📊 Setting up log monitoring..."
cat > /etc/logrotate.d/mock-gps-api << EOF
/home/alexh/Projects/mock-gps-api/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 alexh alexh
}
EOF

echo "✅ Security setup complete!"
echo ""
echo "🔍 Network Configuration:"
echo "- This machine (k8s-control-plane): GPS API on port 5001"
echo "- Tracker app machine (portable-dev): 100.110.187.41"
echo "- Admin access from (admin-workstation): 100.122.121.32"
echo ""
echo "🔐 Security features enabled:"
echo "- UFW firewall with restrictive policies"
echo "- Inbound access from tracker app machine"
echo "- Inbound access from admin-workstation"
echo "- API key authentication"
echo "- Host-based access control"
echo "- Security headers"
echo "- Non-root Docker container"
echo "- Read-only file system"
echo "- Network isolation"
echo ""
echo "🌐 Access Points:"
echo "- GPS API: http://100.99.249.3:5001 (from tracker app and admin)"
echo "- Health check: http://100.99.249.3:5001/health"
echo ""
echo "🔍 Next steps:"
echo "1. Copy env.example to .env and set a strong API key"
echo "2. Restart the Docker container: ./manage.sh restart"
echo "3. Test the API with authentication"
echo "4. Consider setting up fail2ban for additional protection" 