# 🏠 My Homelab Monitoring Stack

This is my personal homelab monitoring setup using Prometheus and Grafana. I've configured this to monitor my Synology NAS and other services in my home network.

## 🎯 What I'm Monitoring

- **Synology NAS** - Main storage and services
- **Docker Containers** - All my running containers
- **System Resources** - CPU, memory, disk, network
- **RAG Stack** - My AI/ML applications

## 🏗️ My Setup

### Services Running:
- **Prometheus** (Port 9090) - Metrics collection and storage
- **Grafana** (Port 3000) - Dashboards and visualization
- **Node Exporter** (Port 9100) - Host system metrics
- **cAdvisor** (Port 8080) - Container metrics

### My Dashboards:
- **Synology NAS Dashboard** - Complete monitoring of my NAS
- **RAG Stack Dashboard** - AI application monitoring
- **System Overview** - General system health

## 🚀 How I Deployed This

### 1. Local Development
```bash
git clone https://github.com/Lforlinux/homelab-monitoring.git
cd homelab-monitoring
docker-compose up -d
```

### 2. Production on Synology NAS
I deployed this stack on my Synology NAS using Portainer:
- Uploaded the `docker-compose.yml` to Portainer
- Configured environment variables for my network
- Set up persistent volumes for data retention

## 🔧 My Configuration

### Environment Variables I Use:
```bash
# My Grafana password
GRAFANA_PASSWORD=my_secure_password

# My Synology NAS IP
SYNOLOGY_IP=my_nas_ip_address
```

### My Prometheus Targets:
- `localhost:9090` - Prometheus itself
- `node-exporter:9100` - Host metrics
- `cadvisor:8080` - Container metrics
- `grafana:3000` - Grafana metrics
- `my_nas_ip:3001` - My Synology NAS

## 📊 My Monitoring Strategy

### What I Track:
- **System Health** - CPU, memory, disk usage
- **Network Traffic** - RX/TX on all interfaces
- **Storage** - Volume usage and I/O
- **Temperature** - Hardware sensors
- **Processes** - Running and blocked processes
- **Container Performance** - Resource usage per container

### My Alerts (Planned):
- High CPU usage (>80%)
- Low disk space (<20% free)
- High memory usage (>90%)
- Container restarts
- Network connectivity issues

## 🛠️ My Customizations

### Synology-Specific:
- Removed non-compatible volume mounts
- Configured for Synology's file system structure
- Optimized for ARM/x86 architecture

### Network Configuration:
- All services on internal Docker network
- External access via reverse proxy
- Secure authentication enabled

## 📈 My Results

Since implementing this monitoring stack:
- **Visibility** - I can see exactly what's happening on my NAS
- **Performance** - Identified bottlenecks and optimized accordingly
- **Reliability** - Proactive monitoring prevents issues
- **Automation** - Automated data collection and visualization

## 🔒 My Security Approach

- All sensitive data in environment variables
- No hardcoded passwords in git
- Local `.env` file with my actual credentials
- Reverse proxy for external access
- Regular security updates

## 📝 My File Structure

```
homelab-monitoring/
├── docker-compose.yml              # My main stack definition
├── env.example                     # Template for others
├── monitoring/
│   ├── prometheus.yml             # My Prometheus config
│   └── grafana/
│       ├── provisioning/          # My Grafana setup
│       └── dashboards/
│           ├── synology-nas-dashboard-new.json  # My NAS dashboard
│           └── rag-stack-dashboard.json         # My RAG dashboard
└── examples/                      # How I add exporters to other projects
```

## 🎯 My Next Steps

- [ ] Set up alerting with AlertManager
- [ ] Add monitoring for my router
- [ ] Implement log aggregation
- [ ] Add more custom dashboards
- [ ] Set up automated backups

## 🤝 Sharing My Setup

I've made this repository public so others can see how I've set up monitoring for my homelab. Feel free to use parts of my configuration for your own setup!

### Quick Start for Others:
See [QUICK-START.md](QUICK-START.md) for a simple setup guide.

---

**This is my personal homelab monitoring setup. Use it as inspiration for your own!** 🏠