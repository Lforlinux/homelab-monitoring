# Homelab Monitoring Stack Documentation

## Quick Start Guide

### What is this?
A simple monitoring setup for your home lab using Prometheus and Grafana.

### What you get:
- **Grafana**: Pretty dashboards to see your server stats
- **Prometheus**: Collects data from your servers
- **Node Exporter**: Shows CPU, memory, disk usage
- **cAdvisor**: Shows Docker container stats

### Get Started (5 minutes)

#### 1. Download and Setup
```bash
git clone <your-repo-url>
cd homelab-monitoring
```

#### 2. Set Your Password (Optional)
```bash
cp env.example .env
# Edit .env and change GRAFANA_PASSWORD to something secure
```

#### 3. Start Everything
```bash
docker-compose up -d
```

#### 4. Open Your Browser
- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin123` (or what you set in .env)
- **Prometheus**: http://localhost:9090

### That's it!

You now have monitoring running. Check out the dashboards in Grafana to see your server stats.

### Need to Monitor Another Server?

1. Add a node exporter to that server
2. Update the Prometheus config to scrape it
3. Reload Prometheus: `curl -X POST http://localhost:9090/-/reload`

### Something Not Working?

- **Can't access Grafana?** Check if port 3000 is free
- **No data showing?** Wait 2-3 minutes for data to collect
- **Want to stop everything?** Run `docker-compose down`

### Want More Details?

Check the main `README.md` for advanced configuration and troubleshooting.

---
