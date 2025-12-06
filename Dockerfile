FROM alpine:3.23

# hadolint ignore=DL3018
RUN apk add --update --no-cache ansible ansible-lint openssh nano py3-ruamel.yaml py3-dateutil py3-jmespath  \
  && mkdir /etc/ansible /ansible ~/.ssh

ENV EDITOR=nano

WORKDIR /ansible
