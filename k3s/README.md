# Build a Kubernetes cluster using k3s via Ansible

Author: <https://github.com/itwars>

## K3s Ansible Playbook

Build a Kubernetes cluster using Ansible with k3s. The goal is easily install a Kubernetes cluster on machines running:

- [X] Debian
- [X] Ubuntu
- [X] CentOS

on processor architecture:

- [X] x64
- [X] arm64
- [X] armhf

## System requirements
Ensure Ansible VENV has been activated.
### Install/Update dev l3s cluster
Review settings in `inventory/dev/` dir first.

Make sure VPN connection is up.

Manage k3s cluster
```

```

## Usage

First create a new directory based on the `sample` directory within the `inventory` directory:

```bash
cp -R inventory/sample inventory/my-cluster
```

Second, edit `inventory/my-cluster/hosts.ini` to match the system information gathered above. For example:

```bash
[master]
192.16.35.12

[node]
192.16.35.[10:11]

[k3s_cluster:children]
master
node
```

If needed, you can also edit `inventory/my-cluster/group_vars/all.yml` to match your environment.

Start provisioning of the cluster using the following command:

## Provision k3s in dev environment
```bash
ansible-playbook site.yml -i inventory/dev/hosts.ini
```

## Kubeconfig
To get access to your **Kubernetes** cluster just

```bash
scp k3s-iac@master_ip:~/.kube/config ~/.kube/config
```
