# metrics-server-exporter [![CircleCI](https://circleci.com/gh/grupozap/metrics-server-exporter.svg?style=svg)](https://circleci.com/gh/grupozap/metrics-server-exporter)

metrics-server-exporter provides cpu and memory metrics for nodes and pods, directly querying the metrics-server API `/apis/metrics.k8s.io/v1beta1/{pods, nodes}`

### Node metrics

* kube_metrics_server_nodes_mem
	* Provides nodes memory information.
* kube_metrics_server_nodes_cpu
	* Provides nodes CPU information.

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

  * NAMES_BLACKLIST
    * A list of names from pods, containers or namespaces to exclude from metrics.

### How to build

    $ docker build . -t vivareal/metrics-server-exporter

### How to run

You will need `K8S_TOKEN` and `K8S_ENDPOINT` to access the api-server

    $ docker run -p 8000:8000 -e "K8S_ENDPOINT=${K8S_ENDPOINT}" -e "K8S_TOKEN=${K8S_TOKEN}" vivareal/metrics-server-exporter

### How to deploy

Set you target k8s context and apply the deployment files

    $ kubectl apply -n platform -f deploy/

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


