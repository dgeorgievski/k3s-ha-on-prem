# Deploy High Availability etcd cluster with Ansible.

## Prerequisites

Before you begin, you need to install all these tools:
- [Ansible (at least the version 2.8)](https://www.ansible.com/)
- [Vagrant](https://www.vagrantup.com/)
- [Virtualbox](https://www.virtualbox.org/wiki/Downloads)


## Install Ansible

See the Ansible installation steps in the main `README.md` file in the parent directory.

## Configuration

* The PKI directory is defined in `group_vars/all`
* etcd version is defined in `roles/etcd/defaults/main.yaml`

## Deployment

1. Create the PKI infrastructure:
```bash
$ ansible-playbook pki.yaml

# The certs expiration date should be 10y from now
$ openssl x509 -dates -noout -in  pki/etcd1-peer.crt
notBefore=Mar 15 18:39:09 2022 GMT
notAfter=Mar 12 18:39:09 2032 GMT
```

2. Deploy Etcd cluster:
```bash
$ ansible-playbook etcd.yaml
```

## Verification

Run the following command to get the health status of the cluster
```bash
# ssh to etcd1
$ ssh 10.201.64.40
# RHEL... sigh. PATH=/sbin:/bin:/usr/sbin:/usr/bin
$ sudo bash 
$ export PATH=/usr/local/bin:$PATH

$ etcdctl \
--cert-file /etc/etcd/etcd1-server.crt \
--key-file /etc/etcd/etcd1-server.key \
--ca-file /etc/etcd/server-ca.crt cluster-health

member 259978b345e9b2f3 is healthy: got healthy result from https://10.201.64.40:2379
member 595e274fb51d6133 is healthy: got healthy result from https://10.201.64.42:2379
member 6f4a54727c6b742d is healthy: got healthy result from https://10.201.64.41:2379
cluster is healthy

```

Use API v3
```
export ETCDCTL_API=3
# etcdctl endpoint health
127.0.0.1:2379 is healthy: successfully committed proposal: took = 3.231751ms
```


## License
The source code in this repo is licenced under the GPL 3
