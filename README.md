# k3s-ha-on-prem

Ansible automation for provisioning of K3S HA on-prem infrastructure using ETCD cluster for persistence. 

The primary purpose of this project was to provide ML/BigData on-prem platform which is considerably cheaper in terms of operational costs compared to equivalent platforms or deployments in AWS.

# Install Ansible

First time setup. Only if ansible is not installed yet.
```
$ cd k3s-ha-on-prem
$ python3 -m venv ./venv
$ . ./venv/bin/activate
(venv) $ pip install --upgrade pip
```

Install requirements
```
(venv) $ pip install -r requirements.txt
```

# k3s HA deployment 

## Prerequisites
### Enable SSH PKI authentication on new nodes

Hopefully you control VM provisining and PKI access is built into the VM images. In case you don't and you need to use a password to access the VM nodes, you might want to try this script [hack/pki/configure-nodes.py](hack/pki/configure-nodes.py), a hack, to move in your public key to running VM nodes.

See [hack/pki/README.md](hack/pki/README.md) for more details.

After this step you should never use the password for authentication.


## Set-up

Provision in the order specified.

### ETCD HA cluster 
ETCD v3 HA cluster provisioning. See [etcd-ha/Readme.md](etcd-ha/Readme.md) for more details.

To maintain HA the ECTD cluster requires at least 3 nodes. ETCD serviee could re-use the the control plane nodes.

### Optional - CoreDNS service
In case you want to use a custom DNS service for an internal domain or maybe
delegate a sub-zone from another DNS service like Route 53 or CloudFlare.

See [coredns/README.md](coredns/README.md) for more details.

## k3s HA cluster
K3s HA cluster provisioning. Sse [k3s/README.md](k3s/README.md)

### TODO:
1. HA for k8s API server: At the moment of this writing only one API server is deployed until I figure out how to deploy a load balancer that works with the DNS service and zone to manage API endpoints automatically.

## Custtomization of k3s

TOOO: Review and document all the services listed below. The first 3 services - Colium CNI, MetalLB and External-DNS - are the bare minimum for having a fully automated environment when it comes to managing deployments automatically.

1. Cilium CNI - excellent CNI that could take advantage of host networking. Cilium supports l7/HTTP policies and could replace kube-proxy.
2. MetalLB - your on-prem ELB.
3. external-dns - dynamic management of DNS records. Works well with lots of DNS servcies including some like InfoBlox that are popular on-prem DNS servers.
4. Ingress controllers:
 - nginx - easy to deploy and use.
 - Istio - easy to deploy, but using it requires some thought and planning. Istio is manages a Service Mesh and its policies might overlap with Cilium L7 policies.

5. Apache Spark for ML/BigData workloads - Easy to deploy but requires some planning on using persistence in Kubernetes. Rancher's local provisioner works well with storage attached to VM nodes but you'd like to use MinIO as a long term solution.

6. KubeFlow - it would be possible to deploy KubeFlow, in which case you need to deploy Istio and address users` SSO with Dex. 

# License
This project is a collection of other projects that are focused on individual services - k3s, etcd, coredns - that are required to create a fuly functional Kubernetes cluster.

These projects are licensed under different Open Source license types that need to be observed.