# getMerakiEventCount
Displays count of an event type from Meraki Dashboard  on a defined time frame

## Prerequisites

- Meraki Dashboard API access , see documentation here : https://documentation.meraki.com/General_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
- Meraki Module installed (pip3 install meraki)

## How to Use : 

- -k / --key : provide API key - optional
- -o / --org : set an organization ID - optional
- -n / --net : set a network ID - optional
- -s / --span : set the time span (in days) - optional
- -t / --type : set event type - mandatory
- -p / --product : set product type - mandatory
    
### Details :

If no Org ID provided, the scripts displays the organizations available

Default timespan if not provided : 1 day 

Available product types  :

    wireless, appliance, switch, systemsManager, camera, cellularGateway,  environmental