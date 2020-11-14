# Get Meraki Events Count from Meraki Dashboard  - By Gabriel TOUBEAU (github.com/gabtoub)
# Recommended for security reasons : set meraki_apikey environment variable

import meraki
import argparse
import os
import sys
import datetime


def getorganisations(apikey):
    session = meraki.DashboardAPI(api_key=apikey, print_console=False, output_log=False, suppress_logging=True)
    org = session.organizations.getOrganizations()
    return org


def getnetworks(apikey, org):
    session = meraki.DashboardAPI(api_key=apikey, print_console=False, output_log=False, suppress_logging=True)
    net = session.organizations.getOrganizationNetworks(organizationId=org)
    return net


def getnbevents(apikey, netID, product, event_type, timestamp):
    session = meraki.DashboardAPI(api_key=apikey, print_console=False, output_log=False, suppress_logging=True)
    log = session.networks.getNetworkEvents(networkId=netID, productType=product, includedEventTypes=event_type,
                                            startingAfter=timestamp, perPage="1000")
    counter = 0
    for event in log['events']:
        counter = counter + 1
    return counter


def main():
    # set arguments
    var_parser = argparse.ArgumentParser()
    var_parser.add_argument("--key", help="Set up Meraki API Key or set into env var", type=str, required=False)
    var_parser.add_argument("--org", help="Set Org ID", type=str, required=False)
    var_parser.add_argument("--net", help="Set Network ID", type=str, required=False)
    var_parser.add_argument("--time", help="Set Timespan", type=str, required=False)
    var_parser.add_argument("--type", help="Set Event Type", type=str, required=False)
    var_parser.add_argument("--product", help="Set Product", type=str, required=False)

    # set parsed arguments in variables
    variables = var_parser.parse_args()
    org = variables.org
    net = variables.net
    span = variables.time
    type = variables.type

    if variables.key:
        apikey = variables.key
    else:
        try:
            apikey = (os.environ["MERAKI_APIKEY"])
        except:
            print("API Key error - Please set in Env variables or in arguments")
            sys.exit()

    organ = getorganisations(apikey)
    if not org:
        print("\n Please set Org ID in parameters \n")
    else:
        if net:
            timenow = datetime.datetime.now()
            timedelta = timenow - datetime.timedelta(days=1)
            timestamp = timedelta.strftime("%Y-%m-%dT%H:%M:%SZ")
            product = "wireless"
            event_type = "dfs_event"
            event_count = getnbevents(apikey, net, product, event_type, timestamp)
            print(f"Network : {net} , Number of {event_type} : {event_count}")

        else:
            networks = getnetworks(apikey, org)
            timenow = datetime.datetime.now()
            timedelta = timenow - datetime.timedelta(days=1)
            timestamp = timedelta.strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"Timespan : between {timedelta} and {timenow}")
            for each in networks:
                ti = 0
                netID = each.get('id')
                netname = each.get('name')
                product = "wireless"
                event_type = "dfs_event"
                event_count = getnbevents(apikey, netID, product, event_type, timestamp)
                print(f"Network : {netname} , Number of {event_type} : {event_count}")


main()
