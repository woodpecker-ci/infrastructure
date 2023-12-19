FROM alpine:3.19

RUN apk add --update --no-cache ansible ansible-lint openssh nano py3-ruamel.yaml

# Makes the Ansible directories
RUN mkdir /etc/ansible /ansible
RUN mkdir ~/.ssh

ENV EDITOR=nano

WORKDIR /ansible
