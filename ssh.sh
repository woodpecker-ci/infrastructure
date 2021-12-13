#! /bin/bash

if [ "$1" == "open" ]; then
  echo "Opening SSH ..."
  echo "Don't forget to close afterwards"
  ./ansible.sh ansible-playbook site.yml --skip-tags ssh-close --tags ssh-open
elif [ "$1" == "close" ]; then
  echo "Closing SSH ..."
  ./ansible.sh ansible-playbook site.yml --skip-tags ssh-open --tags ssh-close
elif [ "$1" == "connect" ]; then
  if [ ! -f "keys/ci_woodpecker-ci_org.id_ed25519" ]; then
    echo "Decrypting SSH keys ..."
    ./ansible.sh ansible-playbook site.yml --skip-tags always --tags ssh-key
    # TODO: chown key to current user
  fi

  ssh -i ./keys/ci_woodpecker-ci_org.id_ed25519 root@ci.woodpecker-ci.org
else
  echo "Usage: $0 open|close|connect"
fi
