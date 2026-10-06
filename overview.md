# Infrastructure overview

Everything the Woodpecker CI project runs and has to maintain. The Ansible code in this repo is the source of truth, this page is the map to it.

<!-- TODO: add a "Backups" section and show them in overview/overview.py once backups are implemented (none exist yet). -->

## The big picture

![Overview of the Woodpecker CI infrastructure](overview/overview.png)

Generated from [`overview/overview.py`](overview/overview.py). Do not edit the image, change the script and run `python3 overview/overview.py` (needs Graphviz and `pip install diagrams`).

In short:

- One small Hetzner Cloud server (`server01`) runs everything permanent as Docker containers behind Caddy.
- Pipelines do not run on that server. The autoscaler creates a bigger Hetzner server when work is queued and deletes it again when idle.
- The website and mail are not on our servers at all: GitHub Pages and Porkbun.

The sections below zoom into one question each.

## Who answers which hostname

All DNS records of `woodpecker-ci.org` live in Hetzner DNS and are managed by the `hetzner_dns` role.

```mermaid
flowchart LR
  user([Browser, CLI, go get])

  subgraph dns[Hetzner DNS . woodpecker-ci.org]
    hosts[ci, grpc-ci, go, translate, vault<br/>CNAME server01]
    apex[apex, www]
    mx[MX]
  end

  subgraph server01[server01 . Hetzner Falkenstein]
    caddy[Caddy :80 :443<br/>TLS certificates]
    wp[woodpecker-server]
    vw[Vaultwarden]
    wl[Weblate]
    go[go. vanity imports<br/>answered by Caddy itself]
  end

  pages[GitHub Pages<br/>website and docs]
  porkbun[Porkbun mail forwarding]
  legacy[wp.laszlo.cloud<br/>legacy domain]

  user --> hosts -->|Hetzner firewall: 22, 80, 443| caddy
  user --> apex --> pages
  mx --> porkbun
  legacy -.->|redirect to ci.| caddy
  caddy -->|ci. to :8000| wp
  caddy -->|grpc-ci. to h2c :9000| wp
  caddy -->|vault. to :80| vw
  caddy -->|translate. to :8080| wl
  caddy --- go
```

`wp.laszlo.cloud` was the URL of the original project creator. The redirect stays as long as that domain points to us.

## What runs on server01

`server01` is a Hetzner `CAX11` (arm64, 2 vCPU, 4 GB RAM, 40 GB disk) with Ubuntu 24.04. Every service is one Ansible role and one or more Docker containers.

```mermaid
flowchart TB
  subgraph web[docker network: web]
    caddy[caddy]
    wp[woodpecker_server]
    as[woodpecker_autoscaler]
    vw[vaultwarden]
    wl[weblate]
  end

  subgraph weblate[docker network: weblate]
    pg[(weblate_database<br/>Postgres)]
    vk[(weblate_cache<br/>Valkey)]
  end

  subgraph state[State on disk]
    d1[/"/opt/woodpecker (SQLite)"/]
    d2[/vaultwarden_data/]
    d3[/weblate_weblate-data/]
    d4[/weblate_postgres-data/]
    d5[/weblate_redis-data/]
    d6[/"caddy_data (certificates)"/]
  end

  caddy --> wp & vw & wl
  as -->|API :8000| wp
  wl --> pg & vk

  wp --- d1
  vw --- d2
  wl --- d3
  pg --- d4
  vk --- d5
  caddy --- d6

  smtp[SMTP provider]
  vw -->|mail| smtp
  wl -->|mail| smtp
```

Also on the host: a daily `docker system prune` timer and a `reboot` cron pipeline.

## How a pipeline runs

No agent runs permanently. The autoscaler keeps between 0 and 1 agents on Hetzner `CPX42` servers in Helsinki.

```mermaid
sequenceDiagram
  participant GH as GitHub
  participant S as woodpecker-server
  participant A as autoscaler
  participant H as Hetzner Cloud API
  participant W as agent (CPX42, Helsinki)
  participant R as Docker Hub / Quay

  GH->>S: webhook (push, PR, tag)
  S->>S: queue workflows
  A->>S: poll queue (every 5s)
  A->>H: create server if none is free
  H-->>W: boot, start woodpecker-agent
  W->>S: connect gRPC via grpc-ci.woodpecker-ci.org:443
  S->>W: assign workflows (up to 4 per agent)
  W->>GH: clone
  W->>R: pull images, push releases
  W->>S: logs and status
  S->>GH: commit status
  A->>H: delete server after 50m idle
```

## How changes get deployed

This repo deploys itself through the CI server it manages.

```mermaid
flowchart LR
  renovate[Renovate] -->|version bump PR| repo
  maint([Maintainer]) -->|PR| repo[infrastructure repo]
  repo -->|PR and push:<br/>ansible-check, diff only| ci[ci.woodpecker-ci.org]
  maint -->|deploy button on main| ci
  ci -->|ansible-apply over ssh| server01[server01]
  ci -->|hetzner_dns role| dns[Hetzner DNS]
  vault[(Ansible vault<br/>encrypted in repo)] -.-> ci
```

Local runs are possible too, see the [README](README.md).

## Outside of Ansible

Things we depend on that this repo does not manage. Who owns and can access them is listed in [GOVERNANCE.md](https://github.com/woodpecker-ci/.github/blob/main/GOVERNANCE.md).

| What                | Used for                                      |
| ------------------- | --------------------------------------------- |
| GitHub org          | Source code, OAuth login for CI, webhooks     |
| GitHub Pages        | Website and docs (`woodpecker-ci.org`, `www`) |
| Docker Hub and Quay | Published `woodpeckerci` images               |
| Codeberg orgs       | `woodpecker-ci` and `woodpecker-plugins`      |
| Porkbun             | Mail forwarding for `@woodpecker-ci.org`      |
| SMTP provider       | Outgoing mail of Weblate and Vaultwarden      |
| Hetzner firewalls   | Allow 22, 80 and 443 to `server01`            |
| Renovate            | Dependency and image update PRs               |
| OpenCollective      | Donations                                     |
| Domain registration | `woodpecker-ci.org`                           |
