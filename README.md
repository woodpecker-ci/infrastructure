# Woodpecker-CI Infrastructure

## Remote apply

Is done through Woodpecker-CI itself using the [woodpecker ansible plugin](https://codeberg.org/woodpecker-plugins/ansible).

On the `main` branch the "deployment" approach is used, which means that run on the branch don't "apply" changes but one must manually click the "deploy" button of these runs to initiate the deployment.

## Local apply

### Preparation

For reproducibility, a Dockerfile is provided to run the ansible playbook locally.

1. Save the ansible vault password under `vault-pass.secret`
2. Run `docker build -t ansible .`
3. Install dependencies: `./ansible.sh ansible-galaxy install -r requirements.yaml`

### Provisioning

1. Run `./ansible.sh`

> [!NOTE]
> You can execute specific parts of the deployment by using a filter.
> For example to only update `woodpecker` you could use: `./ansible.sh ansible-playbook playbooks/run.yaml --tags woodpecker`

## Local SSH connection

- Use `./ssh.sh`. This will decrypt the local SSH key and connect to the server. (Only works if you're allowed to decrypt the key.)
