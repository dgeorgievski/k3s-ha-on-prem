CoreDNS HA deployment
-----------------------

Make sure ETCD is deployed first. CoreDNS is configured to read zone data from a zone key `/taina` in ETCD. 

Zone records in ETCD could be managed manaaged manually by `etcdctl` as automatically through [external-dns](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/coredns.md) in k3s.

`external-dns` is an essential requirement for automation of deployments in Kubernetes.

# CoreDNS provisioning
```
$ cd coredns/
$ ansible-playbook -i inventory coredns.yaml
```