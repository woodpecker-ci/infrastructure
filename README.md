# Woodpecker-CI infrastructure

## Provisioning

- save the ansible vault password under `vault-pass.secret`
- run `docker build -t ansible`
- run `./provision.sh`