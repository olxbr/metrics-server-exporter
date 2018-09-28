# -*- coding: utf-8 -*-

import os
import requests
import json
import time
import string

from prometheus_client import Metric, start_http_server
from prometheus_client.core import REGISTRY

SVC_TOKEN = os.environ.get('K8S_FILEPATH_TOKEN', '/var/run/secrets/kubernetes.io/serviceaccount/token')
TOKEN =     os.environ.get('K8S_TOKEN')
API_URL =   os.environ.get('K8S_ENDPOINT', 'https://kubernetes.default.svc')

API_NODES = "{}/apis/metrics.k8s.io/v1beta1/nodes".format(API_URL)
API_PODS  = "{}/apis/metrics.k8s.io/v1beta1/pods".format(API_URL)

class MetricsServerExporter:

    def __init__(self):
        if os.path.exists(SVC_TOKEN):
           with open(SVC_TOKEN, 'r') as f:
                  self.token = f.readline()
        else:
            self.token = TOKEN

    def kube_metrics(self):
        headers = { "Authorization": "Bearer {}".format(self.token) }

        payload = {
            'nodes': requests.get(API_NODES, headers=headers, verify=False),
            'pods':  requests.get(API_PODS,  headers=headers, verify=False)
        }

        return payload

    def collect(self):
        ret = self.kube_metrics()
        nodes = json.loads(ret['nodes'].text)
        pods = json.loads(ret['pods'].text)

        metrics_nodes_mem = Metric('kube_metrics_server_nodes_mem', 'Metrics Server Nodes Memory', 'gauge')
        metrics_nodes_cpu = Metric('kube_metrics_server_nodes_cpu', 'Metrics Server Nodes CPU', 'gauge')

        for node in nodes.get('items', []):
            node_instance = node['metadata']['name']
            node_cpu = node['usage']['cpu']
            node_cpu = node_cpu.translate(str.maketrans('', '', string.ascii_letters))
            node_mem = node['usage']['memory']
            node_mem = node_mem.translate(str.maketrans('', '', string.ascii_letters))

            metrics_nodes_mem.add_sample('kube_metrics_server_nodes_mem', value=int(node_mem), labels={ 'instance': node_instance })
            metrics_nodes_cpu.add_sample('kube_metrics_server_nodes_cpu', value=int(node_cpu), labels={ 'instance': node_instance })

        yield metrics_nodes_mem
        yield metrics_nodes_cpu

        metrics_pods_mem = Metric('kube_metrics_server_pods_mem', 'Metrics Server Pods Memory', 'gauge')
        metrics_pods_cpu = Metric('kube_metrics_server_pods_cpu', 'Metrics Server Pods CPU', 'gauge')

        for pod in pods.get('items', []):
            pod_name = pod['metadata']['name']
            pod_namespace = pod['metadata']['namespace']
            for container in pod['containers']:
                pod_container_name = container['name']
                pod_container_cpu = container['usage']['cpu']
                pod_container_cpu = pod_container_cpu.translate(str.maketrans('', '', string.ascii_letters))
                pod_container_mem = container['usage']['memory']
                pod_container_mem = pod_container_mem.translate(str.maketrans('', '', string.ascii_letters))

            metrics_pods_mem.add_sample('kube_metrics_server_pods_mem', value=int(pod_container_mem), labels={ 'pod_name': pod_name, 'pod_namespace': pod_namespace, 'pod_container_name': pod_container_name })
            metrics_pods_cpu.add_sample('kube_metrics_server_pods_cpu', value=int(pod_container_cpu), labels={ 'pod_name': pod_name, 'pod_namespace': pod_namespace, 'pod_container_name': pod_container_name })

        yield metrics_pods_mem
        yield metrics_pods_cpu

if __name__ == '__main__':
    REGISTRY.register(MetricsServerExporter())
    start_http_server(8000)
    while True:
        time.sleep(5)
