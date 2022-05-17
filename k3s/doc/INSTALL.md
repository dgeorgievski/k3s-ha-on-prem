./configure-nodes.py \
--username dgeorgievs \
--init-password dgeorgievs#2022 \
--strong-password foksi234Ubro#

RHEL
=============
https://rancher.com/docs/k3s/latest/en/advanced/#additional-preparation-for-red-hat-centos-enterprise-linux


systemctl disable firewalld --now
systemctl disable nm-cloud-setup.service nm-cloud-setup.timer
setenforce 0
iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -t nat -F
    iptables -t mangle -F
    iptables -F
    iptables -X
    iptables-save
    iptables -L
   
   sestatus
    ip route
    ip link

journalctl -u k3s-node -f

dig google.com @10.0.0.5

systemctl disable nm-cloud-setup.service nm-cloud-setup.timer

reboot
systemctl status firewalld
systemctl status nm-cloud-setup.service
systemctl status nm-cloud-setup.timer
 - not found

 route -n
 ip link

 kubectl exec -it -n kube-system cilium-nx2p6 -- cilium status 

## MetalLB

```shell
$ cd apps
$ k apply -k metallb 
```

## Ingress Nginx
```shell
helm upgrade --install \
ingress-nginx ingress-nginx \
--namespace ingress-nginx \
--create-namespace \
-f nginx.yaml \
--debug --dry-run
```

## Istio 

Use `istioctl` to manage Istio in k3s. 
More details provided at https://istio.io/latest/docs/setup/install/istioctl/
```shell
$ cd k3s-ha/apps/istio
$ istioctl install --set profile=demo
$ kubectl -n istio-system get IstioOperator installed-state -o yaml > installed-state.yaml

$ istioctl verify-install -f  installed-state.yaml
✔ ClusterRole: istiod-istio-system.istio-system checked successfully
✔ ClusterRole: istio-reader-istio-system.istio-system checked successfully
...
Checked 15 custom resource definitions
Checked 3 Istio Deployments
✔ Istio is installed and verified successfully

$ istioctl version
client version: 1.13.2
control plane version: 1.13.2
data plane version: 1.13.2 (2 proxies)
```

## Zone certs
https://confluence.wiley.com/display/GKB/Apache+-+Create+SSL+cert+signed+by+Digicert

Generate server key and cert signing request.
```shell
$ cd k3s-ha/apps/certs/dev2_dsp_private_wiley_host
$ openssl genrsa -out server.key 2048
Generating RSA private key, 2048 bit long modulus
...+++
.....................................................................+++
e is 65537 (0x10001)
```

wildcard cert for *.dev2.dsp.private.wiley.host
```shell
openssl req -new -key server.key -out server.csr
```

Check DigiCert signed request
```shell
$ openssl x509 -text -in star_dev2_dsp_private_wiley_host.crt 
```

Add the Intermediate Certificate to your SSL Certificate
```shell
$ cat DigiCertCA.crt >> star_dev2_dsp_private_wiley_host.crt 
```

Create `cert-manager` namespace to place certs, and later maybe use it
for deploying the `cert-manager` components.

Deploy DigiCerts as a k8s tls secret.
```shell
$ k create ns cert-manager

$ kubectl create secret tls wildcard-dev2-dsp-private-wiley-host \
  --namespace cert-manager \
  --cert=star_dev2_dsp_private_wiley_host.crt \
  --key=server.key
  secret/wildcard-dev2-dsp-private-wiley-host created
```

Install Kubed to manage secrets replication.
See for more https://appscode.com/products/kubed/v0.12.0/setup/install/
```shell
$ helm install kubed appscode/kubed \
  --version v0.12.0 \
  --namespace kube-system

$ kubectl get deployment --namespace kube-system -l "app.kubernetes.io/name=kubed,app.kubernetes.io/instance=kubed"
 NAME    READY   UP-TO-DATE   AVAILABLE   AGE
 kubed   1/1     1            1           8s  
```

Annotate dev2 cert secret for replication with kubed
```shell
$ k annotate secret/wildcard-dev2-dsp-private-wiley-host kubed.appscode.com/sync="kubed=dev2"
secret/wildcard-dev2-dsp-private-wiley-host annotated
```

Label namespaces for secret replication
```shell
$ k label ns istio-system kubed=dev2
namespace/istio-system labeled

$ k get secret/wildcard-dev2-dsp-private-wiley-host -n istio-system
NAME                                   TYPE                DATA   AGE
wildcard-dev2-dsp-private-wiley-host   kubernetes.io/tls   2      45s
```

## Test app for validating ingress conrollers, and certs

Podinfo is a really useful app for validating and exploring interesting solutions in Kubernetes.
See for more https://github.com/stefanprodan/podinfo

Deploy PodInfo with Nginx Ingress.
```shell
$ cd k3s-ha/apps/podinfo

$ k create ns podinfo

$ k label ns podinfo kubed=dev2

$ k get secret/wildcard-dev2-dsp-private-wiley-host -n podinfo
NAME                                   TYPE                DATA   AGE
wildcard-dev2-dsp-private-wiley-host   kubernetes.io/tls   2      3m44s

$ helm upgrade frontend podinfo/podinfo \
--install \
--wait \
--namespace podinfo \
--set replicaCount=2 \
--set backend=http://backend-podinfo:9898/echo \
-f ingress.yaml \
--debug --dry-run


$ helm upgrade --install --wait backend \
--namespace podinfo \
podinfo/podinfo
```




