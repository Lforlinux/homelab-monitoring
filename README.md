# Homelab Monitoring Stack

A dedicated Prometheus and Grafana monitoring stack for your homelab infrastructure. This setup provides centralized monitoring that can be used across multiple projects by simply adding exporters to your other docker-compose files.

## 🏗️ Architecture

This monitoring stack includes:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Node Exporter**: Host system metrics
- **cAdvisor**: Container metrics

## 🚀 Quick Start

> **New to this?** Check out the [QUICK-START.md](QUICK-START.md) for a simple 5-minute setup guide!

### Prerequisites

- Docker and Docker Compose installed
- Ports 3000, 8080, 9090, 9100 available on your host

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd homelab-monitoring
```

2. Configure environment variables (optional):
```bash
cp env.example .env
# Edit .env with your actual values
```

3. Start the monitoring stack:
```bash
docker-compose up -d
```

4. Access the services:
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8080

## 📊 Services Overview

### Prometheus (Port 9090)
- Collects metrics from various exporters
- Stores time-series data
- Provides query interface
- Configuration: `monitoring/prometheus.yml`

### Grafana (Port 3000)
- Web-based visualization platform
- Pre-configured dashboards
- Data source: Prometheus
- Default login: admin/admin123

### Node Exporter (Port 9100)
- Exposes host system metrics
- CPU, memory, disk, network statistics
- File system and hardware information

### cAdvisor (Port 8080)
- Container resource usage metrics
- Performance characteristics
- Resource isolation parameters

## 🔧 Configuration

### Adding New Services to Monitor

To monitor services from other docker-compose projects, add exporters to those projects and update the Prometheus configuration:

1. **Add exporter to your service's docker-compose.yml**:
```yaml
services:
  your-service:
    # your service config
  
  # Add exporter for your service
  your-service-exporter:
    image: appropriate-exporter-image
    ports:
      - "9187:9187"  # or appropriate port
    networks:
      - your-network
    # exporter-specific configuration
```

2. **Update Prometheus configuration** (`monitoring/prometheus.yml`):
```yaml
scrape_configs:
  - job_name: 'your-service'
    static_configs:
      - targets: ['your-service-host:9187']
    scrape_interval: 30s
```

3. **Reload Prometheus configuration**:
```bash
curl -X POST http://localhost:9090/-/reload
```

### Common Exporters

Here are some popular exporters you can add to your other projects:

#### PostgreSQL
```yaml
postgres-exporter:
  image: quay.io/prometheuscommunity/postgres-exporter:latest
  environment:
    - DATA_SOURCE_NAME=postgresql://user:password@postgres:5432/dbname?sslmode=disable
  ports:
    - "9187:9187"
```

#### MySQL
```yaml
mysql-exporter:
  image: prom/mysqld-exporter:latest
  environment:
    - DATA_SOURCE_NAME=user:password@(mysql:3306)/
  ports:
    - "9104:9104"
```

#### Redis
```yaml
redis-exporter:
  image: oliver006/redis_exporter:latest
  environment:
    - REDIS_ADDR=redis://redis:6379
  ports:
    - "9121:9121"
```

#### Nginx
```yaml
nginx-exporter:
  image: nginx/nginx-prometheus-exporter:latest
  command:
    - '-nginx.scrape-uri=http://nginx:8080/nginx_status'
  ports:
    - "9113:9113"
```

## 📈 Dashboards

The stack comes with pre-configured dashboards:

- **System Overview**: Host metrics, CPU, memory, disk usage
- **Container Metrics**: Docker container performance
- **RAG Stack Dashboard**: Custom dashboard for RAG applications

### Creating Custom Dashboards

1. Access Grafana at http://localhost:3000
2. Go to "Dashboards" → "New Dashboard"
3. Add panels and configure data sources
4. Export dashboard JSON and save to `monitoring/grafana/dashboards/`

## 🔍 Monitoring External Services

### Synology NAS
The configuration includes monitoring for Synology NAS (192.168.1.131:3001). Update the IP address in `monitoring/prometheus.yml` to match your NAS.

### Other Homelab Services
Add static targets in the Prometheus configuration for services like:
- Router metrics
- Switch statistics
- IoT devices
- Other servers

## 🛠️ Maintenance

### Backup
```bash
# Backup Grafana data
docker run --rm -v homelab-monitoring_grafana-data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz -C /data .

# Backup Prometheus data
docker run --rm -v homelab-monitoring_prometheus-data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz -C /data .
```

### Restore
```bash
# Restore Grafana data
docker run --rm -v homelab-monitoring_grafana-data:/data -v $(pwd):/backup alpine tar xzf /backup/grafana-backup.tar.gz -C /data

# Restore Prometheus data
docker run --rm -v homelab-monitoring_prometheus-data:/data -v $(pwd):/backup alpine tar xzf /backup/prometheus-backup.tar.gz -C /data
```

### Updates
```bash
# Pull latest images and restart
docker-compose pull
docker-compose up -d
```

## 🔒 Security Considerations

- Change default Grafana password
- Use reverse proxy (nginx/traefik) for external access
- Implement authentication for production use
- Consider using secrets management for sensitive data

## 📝 File Structure

```
homelab-monitoring/
├── docker-compose.yml              # Main stack definition
├── env.example                     # Environment variables template
├── QUICK-START.md                  # Simple 5-minute setup guide
├── examples/
│   └── example-with-exporters.yml  # How to add exporters to other projects
├── monitoring/
│   ├── prometheus.yml             # Prometheus configuration
│   └── grafana/
│       ├── provisioning/
│       │   ├── datasources/
│       │   │   └── prometheus.yml # Grafana data source config
│       │   └── dashboards/
│       │       └── dashboards.yml # Dashboard provisioning
│       └── dashboards/
│           ├── rag-stack-dashboard.json # RAG stack dashboard
│           └── synology-nas-dashboard-new.json # Synology NAS dashboard
└── README.md                      # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8080, 9090, 9100 are available
2. **Permission issues**: Check Docker volume permissions
3. **Configuration errors**: Validate YAML syntax
4. **Memory issues**: Monitor container resource usage

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs prometheus
docker-compose logs grafana
```

### Health Checks
```bash
# Check service health
docker-compose ps

# Test Prometheus
curl http://localhost:9090/-/healthy

# Test Grafana
curl http://localhost:3000/api/health
```
