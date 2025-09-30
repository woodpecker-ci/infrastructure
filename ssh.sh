#!/usr/bin/env bash

SSH_KEY="keys/ci_woodpecker-ci_org.id_ed25519"

if [ ! -f "$SSH_KEY" ]; then
  echo "🔑 Decrypting SSH keys ..."
  ./ansible.sh ansible-playbook playbooks/ssh.yaml --skip-tags always --tags ssh-key --extra-vars ssh_key_base_dir=/ansible
  ./ansible.sh chown "$(id -u)":"$(id -g)" "$SSH_KEY"
fi

echo "🔑 Connecting to the server ..."
ssh -4 -i "$SSH_KEY" -o IdentitiesOnly=yes root@ci.woodpecker-ci.org
