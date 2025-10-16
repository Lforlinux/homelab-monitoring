## Technical Documentation

### Project Overview

This monitoring stack uses Prometheus and Grafana for comprehensive homelab monitoring. The architecture consists of:

• **Prometheus** (port 9090): Time-series database for metrics collection and storage
• **Grafana** (port 3000): Visualization layer with custom dashboards
• **Node Exporter** (port 9100): Collects host system metrics (CPU, memory, disk, network)
• **cAdvisor** (port 8080): Container performance monitoring

This stack is industry-standard, highly scalable, and provides real-time insights into system performance. The configuration is embedded directly in docker-compose.yml using Docker configs, making it fully automated for deployment via Portainer git integration.

---

### Configuration Management

Configuration management is achieved through embedded Docker configs with inline content. This eliminates external file dependencies and makes deployment fully automated.

The key implementation uses:

```yaml
configs:
  prometheus_config:
    content: |
      global:
        scrape_interval: 15s
      # ... entire config embedded here
```

This approach works perfectly with Portainer's git deployment because there are no external files to copy or mount. Everything is self-contained and version-controlled.

---

### Monitoring Targets & Service Discovery

Currently monitoring:

• **Prometheus itself** (localhost:9090) - Self-monitoring
• **Node Exporter** (node-exporter:9100) - Host metrics
• **cAdvisor** (cadvisor:8080) - Container metrics
• **Grafana** (grafana:3000) - Application metrics
• **Synology NAS** (192.168.1.131:3001) - Ready for node-exporter

To add new services, add a new scrape job in the embedded Prometheus config:

```yaml
- job_name: 'new-service'
  static_configs:
    - targets: ['new-service:port']
  scrape_interval: 30s
```

Then update the stack in Portainer. The configuration is version-controlled, so changes are tracked and reversible.

---

### Data Persistence & Retention Strategy

Data persistence is handled through Docker volumes:

• **prometheus-data**: Stores time-series data
• **grafana-data**: Stores dashboard configurations and user data

Retention is configured with `--storage.tsdb.retention.time=30d`, which keeps 30 days of metrics data. This balances storage usage with historical analysis needs.

The volumes are managed by Docker and persist across container restarts. For backup, volume data can be easily backed up or a backup strategy can be implemented for the Synology NAS.

---

### Challenges & Solutions

The main challenge was making the deployment fully automated for Portainer git integration. Initially, external configuration files needed to be copied to the NAS, which broke the automation.

**Problems encountered:**
1. Bind mount failures: External config files didn't exist during git deployment
2. Permission issues: Docker commands not available in user context
3. Port conflicts: Multiple services trying to use the same ports

**Solutions implemented:**
1. Embedded configuration: Used Docker configs with inline content
2. Self-contained deployment: No external file dependencies
3. Port management: Carefully planned port allocation (3000, 8080, 9090, 9100)

The result is a production-ready monitoring stack that deploys automatically from git with zero manual intervention.

---

### Data Retention & Deletion Process

Prometheus uses a built-in Time Series Database (TSDB) with automatic garbage collection. Here's how it works:

**Data Structure:**
```
/prometheus/
├── wal/                                    ← Write-Ahead Log (recent data)
├── 01K7N1METCBEHK94Y0X5PKRWZN/chunks/     ← Data block 1
├── 01K7NP7G3FXX77PARR0R8JPJSN/chunks/     ← Data block 2
└── ... (more blocks)
```

**Deletion Process:**
• No external scripts - Built into Prometheus core
• Block-based deletion - Removes entire 2-hour data blocks
• Automatic process - Runs continuously in background
• After 30 days - Old blocks are automatically deleted
• Rolling window - Always keeps the most recent 30 days

**Retention Configuration:**
```yaml
command:
  - '--storage.tsdb.retention.time=30d'  # 30 days retention
```

---

### cAdvisor Metrics & Queries

cAdvisor provides comprehensive container metrics. Here are key queries used:

**Container Health:**
```promql
up{job="cadvisor"}
```

**Total Running Containers:**
```promql
count(container_last_seen{name!=""})
```

**Top 5 CPU Usage:**
```promql
topk(5, rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100)
```

**Memory Usage:**
```promql
container_memory_usage_bytes{name!=""} / 1024 / 1024
```

**Network I/O:**
```promql
rate(container_network_receive_bytes_total{name!=""}[5m])
```

---

### Grafana Dashboard Management

Dashboard management is achieved through version-controlled JSON files stored in the git repository under `monitoring/grafana/dashboards/`:

**Dashboard Files:**
• container-monitoring-dashboard.json - cAdvisor metrics
• synology-nas-dashboard-new.json - NAS-specific monitoring
• rag-stack-dashboard.json - Application monitoring

**Benefits:**
• Version controlled - Track changes over time
• Auto-provisioned - Loads automatically with stack
• Team collaboration - Others can see dashboard config
• Backup - Safely stored in git

**Dashboard Types:**
• Stat panels - Single values (CPU usage, memory)
• Time series - Historical trends
• Tables - Top N lists
• Gauges - Percentage displays

---

### Service Discovery & Access

Service access is managed through a service discovery approach with memorable URLs:

**Service URLs:**
• Grafana: http://192.168.1.131:3000 (Monitoring dashboards)
• Prometheus: http://192.168.1.131:9090 (Metrics collection)
• cAdvisor: http://192.168.1.131:8080 (Container metrics)

**For better service management, recommended solutions:**
• Heimdall Dashboard - Service discovery portal
• Homer Dashboard - Lightweight service directory
• Organizr - Full-featured dashboard with authentication

---

### Technical Implementation Details

The monitoring stack is implemented using Docker Compose with the following structure:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    configs:
      - source: prometheus_config
        target: /etc/prometheus/prometheus.yml
    command:
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
```

**Key Features:**
• Embedded configuration - No external file dependencies
• Health checks - Container status monitoring
• Volume persistence - Data survives restarts
• Network isolation - Custom Docker network
• Restart policies - Automatic recovery

**Deployment Process:**
1. Git push - Code changes committed
2. Portainer pull - Automatically pulls from git
3. Stack update - Deploys new configuration
4. Zero downtime - Rolling updates

---

### Scaling & Future Improvements

For scaling to larger environments, the following improvements would be implemented:

**Immediate Improvements:**
• Service discovery instead of static targets
• Alertmanager for notifications
• Grafana provisioning for automated dashboard deployment
• Backup strategies for data protection

**Enterprise Scaling:**
• Prometheus federation for multiple instances
• Load balancing for high availability
• External storage for longer retention
• Multi-tenant Grafana setup
• RBAC for user management

**Monitoring Expansion:**
• Application metrics (APM)
• Log aggregation (ELK stack)
• Infrastructure monitoring (Terraform)
• Security monitoring (SIEM)

---

### Key Takeaways

• Fully automated deployment via Portainer git integration
• Self-contained configuration with embedded Prometheus config
• Production-ready monitoring with proper retention and persistence
• Version-controlled dashboards for team collaboration
• Scalable architecture ready for enterprise expansion

---

### Technical References

• Prometheus Documentation: https://prometheus.io/docs/
• Grafana Documentation: https://grafana.com/docs/
• Docker Compose: https://docs.docker.com/compose/
• cAdvisor: https://github.com/google/cadvisor
• Node Exporter: https://github.com/prometheus/node_exporter

---

This document covers the complete implementation of a production-ready monitoring stack for homelab environments, demonstrating expertise in DevOps, monitoring, and infrastructure automation.