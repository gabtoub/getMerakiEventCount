# Get Meraki Events Count from Meraki Dashboard  - By Gabriel TOUBEAU (github.com/gabtoub)
# Recommended for security reasons : set meraki_apikey environment variable

import meraki
import argparse
import os
import sys
import datetime

span = 1


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
    var_parser.add_argument("--span", help="Set Number of days", type=int, required=False)
    var_parser.add_argument("--type", help="Set Event Type", type=str, required=False)
    var_parser.add_argument("--product", help="Set Product", type=str, required=True)

    # Set parsed arguments in variables
    variables = var_parser.parse_args()
    org = variables.org
    net = variables.net
    span = variables.span
    eventtype = variables.type
    prod = variables.product
    #timestamp
    timenow = datetime.datetime.now()
    if not span:
        timedelta = timenow - datetime.timedelta(days=1)
        print("Using default timespan : 1 day")
    else:
        timedelta = timenow - datetime.timedelta(days=span)

    timestamp = timedelta.strftime("%Y-%m-%dT%H:%M:%SZ")

    if variables.key:
        apikey = variables.key
    else:
        try:
            apikey = (os.environ["MERAKI_APIKEY"])
        except:
            print("API Key missing - Please set in Env variables or in arguments")
            sys.exit()

    if not org:
        organ = getorganisations(apikey)
        print("Please set Org ID in parameters - available organizations : ")
        for each in organ:
            # display available Org IDs
            print(f"Organization : {each.get('id')}, Name : {each.get('name')}")

    else:
        if net:
            product = prod
            event_type = type
            event_count = getnbevents(apikey, net, product, event_type, timestamp)
            print(f"Network : {net} , Number of {event_type} : {event_count}")

        else:
            networks = getnetworks(apikey, org)
            print(f"Timespan : between {timedelta} and {timenow}")
            for each in networks:
                netID = each.get('id')
                netname = each.get('name')
                product = prod
                event_type = eventtype
                event_count = getnbevents(apikey, netID, product, event_type, timestamp)
                print(f"Network : {netname} , Number of {event_type} : {event_count}")


main()
