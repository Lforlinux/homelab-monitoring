#!/bin/bash

# Install node exporter on macOS using Homebrew
echo "Installing node exporter on macOS..."

# Install Homebrew if not already installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install node exporter
brew install prometheus-node-exporter

# Create launchd plist for auto-start
sudo tee /Library/LaunchDaemons/com.prometheus.node_exporter.plist > /dev/null <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.prometheus.node_exporter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/node_exporter</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load and start the service
sudo launchctl load /Library/LaunchDaemons/com.prometheus.node_exporter.plist
sudo launchctl start com.prometheus.node_exporter

echo "Node exporter installed and started on port 9100"
echo "Test it: curl http://localhost:9100/metrics"
