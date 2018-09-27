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

