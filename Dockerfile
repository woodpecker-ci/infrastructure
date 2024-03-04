FROM alpine:3.19

# hadolint ignore=DL3018
RUN apk add --update --no-cache ansible ansible-lint openssh nano py3-ruamel.yaml \
  && mkdir /etc/ansible /ansible ~/.ssh

ENV EDITOR=nano

WORKDIR /ansible
