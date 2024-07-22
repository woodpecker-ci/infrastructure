#!/usr/bin/env bash

RUN_ANSIBLE="docker run --rm -ti -e ANSIBLE_PRIVATE_KEY_FILE=keys/ci_woodpecker-ci_org.id_ed25519 -e ANSIBLE_VAULT_PASSWORD_FILE=vault-pass.secret -v $(pwd):/ansible ansible"

# docker build -t ansible .
P=$@
CMD="${P:=ansible-playbook playbooks/run.yaml}"

$RUN_ANSIBLE $CMD
