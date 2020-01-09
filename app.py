# -*- coding: utf-8 -*-

import datetime
import getopt
import os
import requests
import string
import sys
import time

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from prometheus_client import Metric, start_http_server
from prometheus_client.core import REGISTRY

class MetricsServerExporter:

    def __init__(self):
        self.svc_token       = os.environ.get('K8S_FILEPATH_TOKEN', '/var/run/secrets/kubernetes.io/serviceaccount/token')
        self.ca_cert         = os.environ.get('K8S_CA_CERT_PATH', '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt')
        self.api_url         = os.environ.get('K8S_ENDPOINT', 'https://kubernetes.default.svc')
        self.names_blacklist = os.environ.get('NAMES_BLACKLIST', '').split(',')
        self.namespaces      = os.environ.get('NAMESPACE_WHITELIST','').split(',')
        self.labelSelector   = os.environ.get('LABEL_SELECTOR','')

        self.api_nodes_url   = "{}/apis/metrics.k8s.io/v1beta1/nodes".format(self.api_url)
        self.api_pods_url = "{}/apis/metrics.k8s.io/v1beta1/pods".format( self.api_url)

        self.insecure_tls = self.set_tls_mode()
        self.token = self.set_token()

    def set_tls_mode(self):
        return ('--insecure-tls','') in options

    def set_token(self):
        if os.environ.get('K8S_TOKEN') is not None:
            return os.environ.get('K8S_TOKEN')

        if os.path.exists(self.svc_token):
            with open(self.svc_token, 'r') as f:
                os.environ['K8S_TOKEN'] = f.readline()
            return os.environ.get('K8S_TOKEN')

        return None

    def set_namespaced_pod_url(self,namespace):
        return '{}/apis/metrics.k8s.io/v1beta1/namespaces/{}/pods?labelSelector={}'.format( self.api_url ,namespace,self.labelSelector )

    def kube_metrics(self):
        headers = { "Authorization": "Bearer {}".format(self.token) }
        query = { 'labelSelector' : self.labelSelector }
        session = requests.Session()
        retry = Retry(total=3, connect=3, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        if self.insecure_tls:
            session.verify = False
        elif os.path.exists(self.ca_cert):
            session.verify = self.ca_cert
        if self.namespaces:
            pod_data = None
            for namespace in self.namespaces:
                if pod_data is None:
                    pod_data = session.get(self.set_namespaced_pod_url(namespace), headers=headers, params=query).json()
                else:
                    pod_data['items'] += session.get(self.set_namespaced_pod_url(namespace), headers=headers, params=query).json()['items']
            payload = {
                'nodes': session.get(self.api_nodes_url, headers=headers, params=query).json(),
                'pods':  pod_data
            }
        else:
            payload = {
                'nodes': session.get(self.api_nodes_url, headers=headers, params=query).json(),
                'pods':  session.get(self.api_pods_url,  headers=headers, params=query).json()
            }

        return payload

    def collect(self):
        start_time = datetime.datetime.now()
        ret = self.kube_metrics()
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds()

        nodes = ret['nodes']
        pods = ret['pods']

        metrics_nodes_mem = Metric('kube_metrics_server_nodes_mem', 'Metrics Server Nodes Memory', 'gauge')
        metrics_nodes_cpu = Metric('kube_metrics_server_nodes_cpu', 'Metrics Server Nodes CPU', 'gauge')

        metrics_response_time = Metric('kube_metrics_server_response_time', 'Metrics Server API Response Time', 'gauge')
        metrics_response_time.add_sample('kube_metrics_server_response_time', value=total_time, labels={ 'api_url': '{}/metrics.k8s.io'.format(self.api_url) })
        yield metrics_response_time

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

            pod_container_mem = 0
            pod_container_cpu = 0
            pod_container_name = ""

            for container in pod['containers']:
                pod_container_name = container['name']
                pod_container_cpu = container['usage']['cpu']
                pod_container_cpu = pod_container_cpu.translate(str.maketrans('', '', string.ascii_letters))
                pod_container_mem = container['usage']['memory']
                pod_container_mem = pod_container_mem.translate(str.maketrans('', '', string.ascii_letters))

                if not any(blacklisted in self.names_blacklist for blacklisted in [pod_container_name, pod_name, pod_namespace]):
                    metrics_pods_mem.add_sample('kube_metrics_server_pods_mem', value=int(pod_container_mem), labels={ 'pod_name': pod_name, 'pod_namespace': pod_namespace, 'pod_container_name': pod_container_name })
                    metrics_pods_cpu.add_sample('kube_metrics_server_pods_cpu', value=int(pod_container_cpu), labels={ 'pod_name': pod_name, 'pod_namespace': pod_namespace, 'pod_container_name': pod_container_name })

        yield metrics_pods_mem
        yield metrics_pods_cpu

if __name__ == '__main__':
    options, remainder = getopt.gnu_getopt(sys.argv[1:], '', ['insecure-tls'])
    REGISTRY.register(MetricsServerExporter())
    start_http_server(8000)
    while True:
        time.sleep(5)
