#!/usr/bin/env python3
"""Overview of the Woodpecker CI project infrastructure.

Renders overview.png next to this file.
Needs: graphviz, `pip install diagrams`. Icons live in ./icons.

Keep this picture coarse. Ports, volumes, mail, deploy flow and the
pipeline life cycle are in the Mermaid views of ../overview.md.

TODO: add backups here once implemented (none exist yet).
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.network import Firewall
from diagrams.onprem.client import Users

HERE = Path(__file__).resolve().parent
ICONS = HERE / "icons"


def icon(label: str, name: str) -> Custom:
    return Custom(label, str(ICONS / f"{name}.png"))


GRAPH = {"splines": "spline", "fontsize": "16", "pad": "0.3", "nodesep": "0.6", "ranksep": "1.1"}
DNS = {"style": "dotted", "color": "#888888"}
CI = {"color": "#4CAF50", "penwidth": "2"}

with Diagram(
    "Woodpecker CI infrastructure",
    filename=str(HERE / "overview"),
    outformat="png",
    show=False,
    direction="LR",
    graph_attr=GRAPH,
):
    users = Users("Users and\ncontributors")

    with Cluster("External"):
        github = icon("GitHub\nrepos, OAuth, webhooks", "github")
        pages = icon("GitHub Pages\nwoodpecker-ci.org", "githubpages")
        registries = icon("Docker Hub, Quay\nwoodpeckerci images", "docker")
        porkbun = icon("Porkbun\nmail forwarding", "porkbun")

    with Cluster("Hetzner Cloud project"):
        dns = icon("Hetzner DNS\nwoodpecker-ci.org", "hetzner")
        api = icon("Hetzner Cloud API", "hetzner")
        fw = Firewall("Firewall\n22, 80, 443")

        with Cluster("server01 . CAX11 arm64 . Ubuntu 24.04 . Falkenstein"):
            caddy = icon("Caddy\nTLS, reverse proxy", "caddy")
            server = icon("woodpecker-server\nci.", "woodpecker")
            autoscaler = icon("woodpecker-autoscaler", "woodpecker")
            vaultwarden = icon("Vaultwarden\nvault.", "vaultwarden")
            weblate = icon("Weblate\ntranslate.", "weblate")
            sqlite = icon("SQLite", "sqlite")
            postgres = icon("Postgres", "postgresql")
            valkey = icon("Valkey", "valkey")

        with Cluster("Autoscaled . 0 to 1 . CPX42 . Helsinki"):
            agent = icon("woodpecker-agent\nruns pipelines", "woodpecker")

    # web traffic
    users >> Edge(label="https") >> fw >> caddy
    users >> pages
    caddy >> server
    caddy >> vaultwarden
    caddy >> weblate
    server >> sqlite
    weblate >> postgres
    weblate >> valkey

    # dns
    dns >> Edge(label="ci, grpc-ci, go,\ntranslate, vault", **DNS) >> caddy
    dns >> Edge(label="apex, www", **DNS) >> pages
    dns >> Edge(label="MX", **DNS) >> porkbun

    # ci
    # reversed so that External stays on the right of the layout
    server << Edge(label="webhooks", **CI) << github
    autoscaler >> Edge(label="queue", **CI) >> server
    autoscaler >> Edge(label="create, delete", **CI) >> api
    api >> Edge(style="dashed", **CI) >> agent
    agent >> Edge(label="gRPC via Caddy", **CI) >> server
    agent >> Edge(label="pull, push", **CI) >> registries
    weblate >> Edge(label="translation PRs") >> github
