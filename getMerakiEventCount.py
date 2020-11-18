# Get Meraki Events Count from Meraki Dashboard  - By Gabriel TOUBEAU (github.com/gabtoub)
# Recommended for security reasons : set meraki_apikey environment variable

import argparse
import datetime
import os
import sys
import meraki


def session(apikey):
    # Open a session to Meraki Dashboard
    s = meraki.DashboardAPI(api_key=apikey, print_console=False, output_log=False, suppress_logging=True)
    return s


def getorganisations(s):
    # Get all organizations available
    org = s.organizations.getOrganizations()
    return org


def getnetworks(s, org):
    # Get all networks available in a specified organization
    net = s.organizations.getOrganizationNetworks(organizationId=org)
    return net


def getnbevents(s, netID, product, event_type, timestamp):
    # Events counter - using Event Log getNetworkEvents Request
    log = s.networks.getNetworkEvents(networkId=netID, productType=product, includedEventTypes=event_type,
                                      startingAfter=timestamp, perPage="1000")
    return len(log['events'])


def main():
    # Set arguments
    var_parser = argparse.ArgumentParser()
    var_parser.add_argument("-k", "--key", help="Set up Meraki API Key or set into Env variable", type=str,
                            required=False)
    var_parser.add_argument("-o", "--org", help="Set Org ID", type=str, required=False)
    var_parser.add_argument("-n", "--net", help="Set Network ID", type=str, required=False)
    var_parser.add_argument("-s", "--span", help="Set Timespan in days", type=int, required=False, default=1)
    var_parser.add_argument("-t", "--type", help="Set Event Type", type=str, required=False)
    var_parser.add_argument("-p", "--product", help="Set Product", type=str, required=True,
                            choices=['wireless', 'appliance', 'switch', 'systemsManager', 'camera', 'cellularGateway',
                                     'environmental'])

    # Set parsed arguments in variables
    try:
        variables = var_parser.parse_args()
        org = variables.org
        net = variables.net
        span = variables.span
        eventtype = variables.type
        prod = variables.product
    except SystemExit:
        return
    except:
        print("Could not parse arguments")
        var_parser.print_help()
        return
    # Timestamp generation for usage in API requests
    timenow = datetime.datetime.now()
    timedelta = timenow - datetime.timedelta(days=span)
    timestamp = timedelta.strftime("%Y-%m-%dT%H:%M:%SZ")

    if variables.key:
        apikey = variables.key
    else:
        try:
            apikey = (os.environ["MERAKI_APIKEY"])
        except:
            sys.exit()
    try:
        s = session(apikey)
    except meraki.APIError:
        print("API Error - check arguments")
        return
    except meraki.APIKeyError:
        print("API Key Error")
        return

    if not org:
        # If no Org ID provided, display all organizations
        try:
            organ = getorganisations(s)
        except meraki.APIError:
            print("API Error - check arguments")
            return
        except meraki.APIKeyError:
            print("API Key Error")
            return
        print("Please set Org ID in parameters - available organizations : ")
        for each in organ:
            # Display available Org IDs
            print(f"Organization : {each.get('id')}, Name : {each.get('name')}")
        sys.exit()

    else:
        if net:
            # Parsing one network only if a network ID is set
            product = prod
            event_type = type
            try:
                event_count = getnbevents(s, net, product, event_type, timestamp)
                print(f"Network : {net} , Number of {event_type} : {event_count}")
            except meraki.APIError:
                print("API Error - check arguments")
                return
            except meraki.APIKeyError:
                print("API Key Error")
                return
        else:
            # Parsing all networks if no network ID set
            try:
                networks = getnetworks(s, org)
                print(f"Timespan : between {timedelta} and {timenow}")
            except meraki.APIError:
                print("API Error - check arguments")
                return
            except meraki.APIKeyError:
                print("API Key Error")
                return
            for each in networks:
                netid = each.get('id')
                netname = each.get('name')
                product = prod
                event_type = eventtype
                event_count = getnbevents(s, netid, product, event_type, timestamp)
                print(f"Network : {netname} , Number of {event_type} : {event_count}")


main()
