FROM alpine

RUN apk add --update --no-cache python3 py3-pip ansible openssh gcc

# Makes the Ansible directories
RUN mkdir /etc/ansible /ansible
RUN mkdir ~/.ssh

WORKDIR /ansible

RUN pip3 install ansible-lint hcloud docker docker-compose

