import os
import requests
import json
from datetime import datetime, timedelta
from client import *

# EDIT THESE
VCO_HOSTNAME = 'xxxxxxxx'
VC_USERNAME = 'xxxxxxxx'
VC_PASSWORD = 'xxxxxxxx'
IS_OPERATOR = True

VCG_NAME = 'VCG1'

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TIME = 60




def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(VC_USERNAME, VC_PASSWORD, IS_OPERATOR)

    params = {"with": ["site", "roles", "pools", "dataCenters", "certificates", "enterprises", "handOffEdges",
                       "enterpriseAssociationCounts"]}
    kwargs = {"timeout": 300}
    get_gateways = client.call_api('network/getNetworkGateways',params, **kwargs)

    current_time = datetime.utcnow()
    start_time = current_time - timedelta(minutes=TIME)

    print('Current Time (UTC)\t=\t' + current_time.strftime(DATE_FORMAT))
    print('Start Time (UTC)\t=\t' + start_time.strftime(DATE_FORMAT))
    print('\n')

    for gw in get_gateways:
        if gw["activationState"] == "ACTIVATED":
            if gw["name"] == VCG_NAME:
                print('Gateway = ' + gw["name"])
                GatewayID = gw["id"]
                params = { "interval": {"start": start_time.strftime(DATE_FORMAT)}, "gatewayId": GatewayID, "metrics": ["cpuPct", "memoryPct", "flowCount", "handoffQueueDrops", "tunnelCount"]}

                print('getGatewayStatusMetrics\n')
                gateway_status_metrics = client.call_api('metrics/getGatewayStatusMetrics',params, **kwargs)
                print(json.dumps(gateway_status_metrics, indent=4))
                print('\n\n')

                print('getGatewayStatusSeries\n')
                gateway_status_series = client.call_api('metrics/getGatewayStatusSeries',params, **kwargs)
                print(json.dumps(gateway_status_series, indent=4))
                print('\n\n')

if __name__ == '__main__':
    main()
