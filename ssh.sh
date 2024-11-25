#!/usr/bin/env bash

if [ ! -f "keys/ci_woodpecker-ci_org.id_ed25519" ]; then
  echo "Decrypting SSH keys ..."
  ./ansible.sh ansible-playbook playbooks/run.yaml --skip-tags always --tags ssh-key
  # TODO: chown key to current user
fi

#echo "open firewall for ssh"
#./ansible.sh ansible-playbook playbooks/run.yaml --skip-tags always --tags ssh-open

ssh -4 -i ./keys/ci_woodpecker-ci_org.id_ed25519 root@ci.woodpecker-ci.org

#echo "close firewall for ssh"
#./ansible.sh ansible-playbook playbooks/run.yaml --skip-tags always --tags ssh-close
