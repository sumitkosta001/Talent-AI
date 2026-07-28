# Infrastructure Configurations

Infrastructure configs, deployment scripts, monitoring profiles, and orchestration declarations for the TalentAI platform.

## Directory Responsibilities

- **`docker/`**: Custom base images, build-optimized Dockerfiles.
- **`kubernetes/`**: K8s manifest files, Helm charts, service configurations, persistent volume claims.
- **`nginx/`**: Reverse proxy configs, API gateway routing, SSL settings.
- **`terraform/`**: Infrastructure as Code configs for cloud providers.
- **`prometheus/`**: Scrape targets, alert rules, monitoring metrics definitions.
- **`grafana/`**: Metrics dashboards, visual display layouts.
- **`loki/`**: Centralized log aggregation configuration.
- **`scripts/`**: CI/CD integration, orchestration, scaling, and provisioning scripts.
