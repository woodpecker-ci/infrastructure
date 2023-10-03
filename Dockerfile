FROM alpine:3.18

RUN apk add --update --no-cache python3 py3-pip ansible openssh nano py3-ruamel.yaml

# Makes the Ansible directories
RUN mkdir /etc/ansible /ansible
RUN mkdir ~/.ssh

ENV EDITOR=nano

WORKDIR /ansible

RUN pip3 install ansible-lint
