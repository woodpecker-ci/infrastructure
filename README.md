# Woodpecker-CI infrastructure

## Provisioning

- save the ansible vault password under `vault-pass.secret`
- run `docker build -t ansible`
- run `./provision.sh`

> Hint: You can provision / update specific parts of the deployment by using a filter. For example to only update `woodpecker` you cloud use: `./provision.sh ansible-playbook site.yml --tags woodpecker`