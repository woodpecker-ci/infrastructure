#! /bin/bash

if [ ! -f "keys/ci_woodpecker-ci_org.id_ed25519" ]; then
  echo "Decrypting SSH keys ..."
  ./ansible.sh ansible-playbook site.yaml --skip-tags always --tags ssh-key
  # TODO: chown key to current user
fi

ssh -i ./keys/ci_woodpecker-ci_org.id_ed25519 root@ci.woodpecker-ci.org
