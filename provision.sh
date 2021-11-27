#!/bin/sh

RUN_ANSIBLE="docker run --rm -ti -v $(pwd):/ansible ansible"

# docker build -t ansible .

$RUN_ANSIBLE ansible-playbook site.yml
