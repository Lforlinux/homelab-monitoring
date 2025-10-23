# Mac Mini Monitoring Setup

This directory contains files to set up monitoring for your Mac Mini (192.168.1.147) in your homelab monitoring stack.

## 🚀 Quick Setup Options

### Option 1: Docker (Recommended)
If you have Docker installed on your Mac Mini:

```bash
# Navigate to the mac-mini-monitoring directory
cd mac-mini-monitoring

# Start the node exporter
docker-compose up -d

# Verify it's working
curl http://localhost:9100/metrics
```

### Option 2: Native Installation
Install node exporter directly on macOS:

```bash
# Run the installation script
./install-native.sh

# Verify it's working
curl http://localhost:9100/metrics
```

## 🔧 Configuration

The Mac Mini will be automatically added to your Prometheus configuration with:
- **Target**: `192.168.1.147:9100`
- **Job Name**: `mac-mini`
- **Scrape Interval**: 15 seconds
- **Labels**: `instance: mac-mini`, `service: workstation`

## 📊 What Gets Monitored

- **CPU Usage**: Processor utilization and load averages
- **Memory Usage**: RAM consumption and swap usage
- **Disk I/O**: Read/write operations and space usage
- **Network Traffic**: Inbound/outbound network statistics
- **System Load**: 1m, 5m, 15m load averages
- **Temperature**: CPU and system temperatures (if available)
- **Processes**: Running process count and system uptime

## 🎯 Next Steps

1. **Choose your setup method** (Docker or native)
2. **Run the setup** on your Mac Mini
3. **Update your .env file** on the Synology NAS with `MAC_MINI_IP=192.168.1.147`
4. **Redeploy the monitoring stack** on your Synology NAS
5. **Check Prometheus targets** at `http://192.168.1.131:9090/targets`

## 🔍 Verification

After setup, you should see:
- **Prometheus**: `mac-mini` target showing as "UP"
- **Grafana**: Mac Mini metrics available in dashboards
- **Metrics**: CPU, memory, disk, and network data flowing

## 🛠️ Troubleshooting

- **Port 9100 in use**: Change the port in docker-compose.yml or stop conflicting services
- **Firewall issues**: Ensure port 9100 is accessible from your Synology NAS
- **Permission issues**: For native install, you may need to run with sudo
- **Docker not starting**: Check Docker Desktop is running and has proper permissions
