#!/usr/bin/env python3

# Python script to create Prometheus Reporting Task and open up a specified port
# to expost the /metrics

# Environment variables for base nifi url (BASENIFIURL) and port number (METRICSPORT)

import requests
import os

def main():
    URL = os.environ.get("BASENIFIURL")   #where is the nifi instance including port
    portNum = os.environ.get("METRICSPORT") #what port do you want to expose metrics

    #First, create the reporting task

    createJson = {"revision":{"version":"0"},"disconnectedNodeAcknowledged":"false","component":
                        {"type":"org.apache.nifi.reporting.prometheus.PrometheusReportingTask","bundle":
                            {"group":"org.apache.nifi","artifact":"nifi-prometheus-nar","version":"1.12.1"}}}
    createPostEndpoint = "nifi-api/controller/reporting-tasks"

    resp = requests.post(url=URL + "/" + createPostEndpoint, json=createJson)

    #Get the id of the new reporting task
    processorId = (dict(resp.json()))["id"]

    # if ok, then set the properties and start
    propertiesPutEndpoint = "nifi-api/reporting-tasks/" + processorId

    propertiesDict = {"component": {"id": "", "name": "PrometheusReportingTask",
                        "properties": {"prometheus-reporting-task-metrics-endpoint-port": "", "prometheus-reporting-task-metrics-send-jvm": ""}},
                        "revision": {"version":"1"}}
    propertiesDict["component"]["id"] = processorId
    propertiesDict["component"]["properties"]["prometheus-reporting-task-metrics-endpoint-port"] = portNum
    propertiesDict["component"]["properties"]["prometheus-reporting-task-metrics-send-jvm"] = "true"

    resp = requests.put(url=URL + "/" + propertiesPutEndpoint, json=propertiesDict)

    statusDict = {"revision":{"version":2},"state":"RUNNING"}
    statusPutEndpoint = "nifi-api/reporting-tasks/" + processorId + "/run-status"
    resp = requests.put(url=URL + "/" + statusPutEndpoint, json=statusDict)

if __name__ == '__main__':
    main()
