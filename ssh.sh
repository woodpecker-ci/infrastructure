#!/usr/bin/env bash

SSH_KEY="keys/ci_woodpecker-ci_org.id_ed25519"

if [ ! -f "$SSH_KEY" ]; then
  echo "🔑 Decrypting SSH keys ..."
  ./ansible.sh ansible-playbook playbooks/run.yaml --skip-tags always --tags ssh-key
  ./ansible.sh chown --from=0:0 $(id -u):$(id -g) "$SSH_KEY"
fi

echo "🔑 Connecting to the server ..."
ssh -4 -i "$SSH_KEY" root@ci.woodpecker-ci.org
