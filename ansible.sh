#!/bin/sh

RUN_ANSIBLE="docker run --rm -ti -v $(pwd):/ansible ansible"

# docker build -t ansible .
P=$@
CMD="${P:=ansible-playbook playbooks/run.yaml}"

$RUN_ANSIBLE $CMD
