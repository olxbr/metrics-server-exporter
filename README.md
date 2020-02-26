# metrics-server-exporter [![CircleCI](https://circleci.com/gh/grupozap/metrics-server-exporter.svg?style=svg)](https://circleci.com/gh/grupozap/metrics-server-exporter) [![Total alerts](https://img.shields.io/lgtm/alerts/g/grupozap/metrics-server-exporter.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/grupozap/metrics-server-exporter/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/grupozap/metrics-server-exporter.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/grupozap/metrics-server-exporter/context:python)
metrics-server-exporter provides cpu and memory metrics for nodes and pods, directly querying the metrics-server API `/apis/metrics.k8s.io/v1beta1/{pods, nodes}`

### Node metrics

* kube_metrics_server_nodes_mem
	* Provides nodes memory information in kibibytes.
* kube_metrics_server_nodes_cpu
	* Provides nodes CPU information in nanocores.

##### labels

* instance

### Pod metrics

* kube_metrics_server_pods_mem
	* Provides pods/container memory information.
* kube_metrics_server_pods_cpu
	* Provides pods/container memory information.

##### labels

* pod_name
* pod_namespace
* pod_container_name

### API metrics

* kube_metrics_server_response_time
	* Provides API response time in seconds.

### Variables

  * K8S_ENDPOINT
    * Url of API of kubernetes (default kubernetes.default.svc)

  * K8S_TOKEN
    * The authorization token (default ServiceAccount token)

  * K8S_FILEPATH_TOKEN
    * Path of ServiceAccount token file (default /var/run/secrets/kubernetes.io/serviceaccount/token)

  * K8S_CA_CERT_PATH
    * Path of Kubernetes CA certificate (default /var/run/secrets/kubernetes.io/serviceaccount/ca.crt)

  * NAMES_BLACKLIST
    * A list of names from pods, containers or namespaces to exclude from metrics.
  * NAMESPACE_WHITELIST
    * A list of namespace to scrape from this way you can create namespaced rolebinding instead of cluster binding. ( quite useful for larger clusters ) ( default : '' (all namespaces))
  * LABEL_SELECTOR
    * A list of Label Selectors.
### Options

  * --insecure-tls
    * Disables TLS verification of the Kubernetes API Server.  (Not recommended in production)

### How to build

    $ docker build . -t vivareal/metrics-server-exporter

### How to run

You will need `K8S_TOKEN` and `K8S_ENDPOINT` to access the api-server.  Use "--insecure-tls" or mount the CA certificate into the container.  Kubernetes will provide the CA certificate in a Kubernetes installation.

    $ docker run -p 8000:8000 -e "K8S_ENDPOINT=${K8S_ENDPOINT}" -e "K8S_TOKEN=${K8S_TOKEN}" vivareal/metrics-server-exporter --insecure-tls

### How to deploy

Set you target k8s context and apply the deployment files

    $ kubectl apply -f deploy/

#### Blacklist

If you want, you could blacklist some names of namespaces, pods or containers, you just need to apply this ConfigMap, replacing the example names

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: metrics-server-exporter
  labels:
    k8s-app: metrics-server-exporter
data:
  NAMES_BLACKLIST: kube-proxy,calico-node,kube2iam # example names
```

### Minikube

How to test in Minikube

	$ minikube delete; minikube start --vm-driver=kvm2 --cpus=2 --memory=4096
	* Deleting "minikube" from kvm2 ...
	* The "minikube" cluster has been deleted.
	* minikube v1.2.0 on linux (amd64)
	* Creating kvm2 VM (CPUs=2, Memory=4096MB, Disk=20000MB) ...
	* Configuring environment for Kubernetes v1.15.0 on Docker 18.09.6
	* Downloading kubelet v1.15.0
	* Downloading kubeadm v1.15.0
	* Pulling images ...
	* Launching Kubernetes ...
	* Verifying: apiserver proxy etcd scheduler controller dns
	* Done! kubectl is now configured to use "minikube"

Enable metrics-server addon

	$ minikube addons enable metrics-server
	* metrics-server was successfully enabled

Deploy the files in minikube

	$ kubectl apply -R -f deploy/ -n kube-system

Then, test the connectivity

	$ kubectl port-forward -n kube-system svc/metrics-server-exporter 9104:9104 &
	$ curl http://localhost:9104/metrics

### Helm

To install metrics-server-exporter, use

	$ helm install --name=metrics-server-exporter --namespace kube-system helm/

You could set the variables using the `--set` parameters

	$ helm install --name=metrics-server-exporter --set custom.k8s_endpoint=https://kubernetes.default.svc helm/
