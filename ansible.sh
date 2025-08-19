#!/usr/bin/env bash

IMAGE_NAME="ansible-woodpecker-ci"
RUN_ANSIBLE="docker run --rm -ti -e ANSIBLE_PRIVATE_KEY_FILE=keys/ci_woodpecker-ci_org.id_ed25519 -e ANSIBLE_VAULT_PASSWORD_FILE=vault-pass.secret -v $(pwd):/ansible $IMAGE_NAME"

# Check if image exists locally
if ! docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
  echo "🏗️ Image '$IMAGE_NAME' not found. Building it now..."
  docker build -t "$IMAGE_NAME" .
else
  echo "✅ Image '$IMAGE_NAME' already exists. Skipping build."
fi

P="$@"
CMD="${P:=ansible-playbook playbooks/run.yaml}"

# shellcheck disable=SC2086
$RUN_ANSIBLE $CMD
