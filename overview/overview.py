#!/usr/bin/env python3
"""Overview of the Woodpecker CI project infrastructure.

Renders overview.png next to this file.
Needs: graphviz, rsvg-convert (librsvg), `pip install diagrams` and network
access on the first run: the icons are downloaded into ./icons (not in git).

Keep this picture coarse. Ports, volumes, mail, deploy flow and the
pipeline life cycle are in the Mermaid views of ../overview.md.

TODO: add backups here once implemented (none exist yet).
"""

import hashlib
import subprocess
import urllib.request
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.network import Firewall
from diagrams.onprem.client import Users

HERE = Path(__file__).resolve().parent
ICONS = HERE / "icons"
ICON_SIZE = "256"

RAW = "https://raw.githubusercontent.com"

# name: (url, sha256 of the download, optional fill colour for SVGs without one)
#
# Official sources only. Git hosted files are pinned to a commit, the
# sha256 pins the rest and protects against a moved or replaced file.
# To update an icon change the url, run the script and copy the sha256
# from the error message after checking the new picture.
SOURCES = {
    "caddy": (
        f"{RAW}/caddyserver/website/19575198cce1ea5f1bb37895ef3f9f2ec0f1997a/src/resources/images/icon-transparent.png",
        "16d9b4bbb96f34238e4f116a646bcb940f21a2b0f008d969617c84eeb62483e3",
    ),
    "docker": (
        f"{RAW}/docker/docs/65aa5cd4815d988f8e4407b15a57f1b7e6f68aa6/static/assets/images/favicon-192x192.png",
        "0ecc60fc860c611cbf042c65ce9137775b6f67bf795af09a7760a4acab054f37",
    ),
    "github": (
        f"{RAW}/primer/octicons/f04253eb4088fb9869418771effb391fa13a2744/icons/mark-github-24.svg",
        "bce494189797623c34e39a41c2c38a132bdca23ce4e6ac06b70116ed7e91ce26",
    ),
    # no public repo to pin to
    "githubpages": (
        "https://pages.github.com/images/logo.svg",
        "02467868bcffbe08476e2085de7593b8f52c1c8588eed7372de54710a3fe3b51",
    ),
    # no public repo to pin to
    "hetzner": (
        "https://www.hetzner.com/_resources/themes/hetzner/images/favicons/android-icon-192x192.png",
        "897187cc02d363f3685e74a7b517d8e0e3f1e382ab1c42c9e00771969294f242",
    ),
    # no public repo to pin to
    "porkbun": (
        "https://porkbun.com/images/favicons/android-icon-192x192.png",
        "78655e43e4617b7c950dbcb928fa3382275d35d004c1ec8f80eee8a10ede337c",
    ),
    "postgresql": (
        f"{RAW}/postgres/pgweb/8eb38fb244de66486bb1121813d2e161e2fa045e/media/img/about/press/elephant.png",
        "ff92fb5d12a7fa6b23c2eb403d2edf4fbc58ced802021e1f02c3583cb70957be",
    ),
    "sqlite": (
        f"{RAW}/sqlite/sqlite/9d50c7ebfc02a8f71661797cef69d457bb22493c/art/sqlite370.svg",
        "462c4ce8229b585dd6880cd308b121d9de63eb619db05e469598594e80d7b151",
    ),
    "valkey": (
        f"{RAW}/valkey-io/assets/45d2f1d78ebb8a0b28746e5e3d31ea56ffe6f2cc/slides/icons/valkey-mark-color.svg",
        "f5d1281ccd76575aefe1455ebfeedf2cbbd6c35a0d91939c811541c0c2d7d25f",
    ),
    "vaultwarden": (
        f"{RAW}/dani-garcia/vaultwarden/1f802f8e6ae9b788e1e9cc5dffb7e83780417332/resources/vaultwarden-icon.svg",
        "c58fe91554bda6e1be51bd0cf56ac84ab63f798d5173e41e71e1aa1de515c7ef",
    ),
    "weblate": (
        f"{RAW}/WeblateOrg/graphics/349baa193057932718209b68d88b8fed371188ec/logo/weblate.svg",
        "0c193c1283afa5a8a554a01fa1e168f31ae9477da396cf8dfc1c665c6f576bee",
    ),
    # the official logo has no colour, use the primary one from design/colors.md
    "woodpecker": (
        f"{RAW}/woodpecker-ci/design/64d61d710ce2eff65ffa4ef814387c0ef045f818/logo/logo.svg",
        "499a7cbd8c8f173a18d00ed7919034021f6b5bef97a567ddfe0889548e2c612d",
        "#4CAF50",
    ),
}


def fetch(name: str) -> Path:
    """Download, verify and cache one icon as PNG."""
    url, sha256, *fill = SOURCES[name]
    # the checksum in the name makes a changed pin miss the cache
    png = ICONS / f"{name}-{sha256[:12]}.png"
    if png.exists():
        return png

    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    got = hashlib.sha256(data).hexdigest()
    if got != sha256:
        raise SystemExit(f"icon {name}: sha256 is {got}, expected {sha256} ({url})")

    ICONS.mkdir(exist_ok=True)
    if url.endswith(".svg"):
        if fill:
            data = data.replace(b"<svg ", f'<svg fill="{fill[0]}" '.encode(), 1)
        size = ["--width", ICON_SIZE, "--height", ICON_SIZE, "--keep-aspect-ratio"]
        subprocess.run(["rsvg-convert", *size, "--output", str(png)], input=data, check=True)
    else:
        png.write_bytes(data)
    return png


def icon(label: str, name: str) -> Custom:
    return Custom(label, str(fetch(name)))


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
    weblate >> Edge(label="translations") >> github
