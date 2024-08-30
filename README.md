# Woodpecker-CI Infrastructure

## Remote apply

Is done through Woodpecker-CI itself using the [woodpecker ansible plugin](https://codeberg.org/woodpecker-plugins/ansible).

On the `main` branch the "deployment" approach is used. This means that every run on the main branch will automatically check the changes and you can apply them by clicking the "deploy" button in the Woodpecker-CI UI.

## Local apply via docker

**Preparation**:

For reproducibility, a Dockerfile is provided to run the ansible playbook locally.

1. Save the ansible vault password under `vault-pass.secret`
2. Run `docker build -t ansible .`
3. Install dependencies: `./ansible.sh ansible-galaxy install -r requirements.yaml`

**Provisioning**:

1. Run `./ansible.sh`

> [!NOTE]
> You can execute specific parts of the deployment by using a filter.
> For example to only update `woodpecker` you could use: `./ansible.sh ansible-playbook playbooks/run.yaml --tags woodpecker`

## SSH

- Use `./ssh.sh`. This will decrypt the local SSH key and connect to the server. (Only works if you have the vault password stored in `vault-pass.secret`)

## Local apply via nix

enter the environment:

```sh
nix develop -c $SHELL
```

**Provisioning**:

run the playbook as usual:

```sh
ansible-playbook playbooks/run.yaml --tags woodpecker
```

> [!NOTE]
> Only works if you have the vault password stored in `vault-pass.secret`
