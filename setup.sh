#!/bin/bash

# Automated setup script for homelab monitoring stack
# This script configures Prometheus and Grafana automatically after deployment

echo "🚀 Setting up homelab monitoring stack..."

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Get the NAS IP (you can modify this)
NAS_IP=${SYNOLOGY_IP:-192.168.1.131}

# Configure Prometheus targets
echo "📊 Configuring Prometheus targets..."

# Create Prometheus config
cat > /tmp/prometheus-config.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'homelab'
    replica: 'prometheus-01'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 5s
    metrics_path: /metrics

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    scrape_interval: 15s
    metrics_path: /metrics

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
    scrape_interval: 15s
    metrics_path: /metrics

  - job_name: 'grafana'
    static_configs:
      - targets: ['grafana:3000']
    scrape_interval: 30s
    metrics_path: /metrics

  - job_name: 'synology-nas'
    metrics_path: /metrics
    static_configs:
      - targets: ['${NAS_IP}:3001']
        labels:
          instance: 'synology-nas'
          service: 'nas'
    scrape_interval: 30s
EOF

# Copy config to Prometheus container
docker cp /tmp/prometheus-config.yml homelab-prometheus:/etc/prometheus/prometheus.yml

# Reload Prometheus configuration
echo "🔄 Reloading Prometheus configuration..."
curl -X POST http://localhost:9090/-/reload

# Wait for Grafana to be ready
echo "⏳ Waiting for Grafana to be ready..."
sleep 10

# Configure Grafana datasource
echo "📈 Configuring Grafana datasource..."
curl -X POST http://localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -u admin:${GRAFANA_PASSWORD:-admin123} \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://homelab-prometheus:9090",
    "access": "proxy",
    "isDefault": true
  }'

echo "✅ Setup complete!"
echo "🌐 Access your services:"
echo "   Prometheus: http://${NAS_IP}:9090"
echo "   Grafana: http://${NAS_IP}:3000"
echo "   Username: admin"
echo "   Password: ${GRAFANA_PASSWORD:-admin123}"
echo ""
echo "📊 Your Synology NAS monitoring is now active!"
