# Woodpecker-CI infrastructure

## Preparation

- save the ansible vault password under `vault-pass.secret`
- run `docker build -t ansible .`
- install dependencies: `./ansible.sh ansible-galaxy install -r requirements.yaml`

## Provisioning

- run `./ansible.sh`

> Hint: You can provision / update specific parts of the deployment by using a filter. For example to only update `woodpecker` you cloud use: `./ansible.sh ansible-playbook site.yaml --tags woodpecker`

## SSH

- Connect to main server using SSH with: `./ssh.sh`
