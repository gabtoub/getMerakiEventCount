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

Default timespan : 1 day 
If no Org ID is provided, the scripts displays the organizations available

    python getMerakiEventCount.py -p wireless
    Using default timespan : 1 day
    Please set Org ID in parameters - available organizations :
    Organization : 549236, Name : DevNet Sandbox
    Organization : 463308, Name : DevNet San Jose


Available product types  :

    wireless, appliance, switch, systemsManager, camera, cellularGateway,  environmental

## Examples : 
    python getMerakiEventCount.py -p wireless -t dfs_event -o 549236
    
    Using default timespan : 1 day
    Timespan : between 2020-11-14 16:37:07.722869 and 2020-11-15 16:37:07.722869
    Network : DevNet Sandbox ALWAYS ON , Number of dfs_event : 17
    Network : DNSMB3 , Number of dfs_event : 0
    Network : DNSMB2 , Number of dfs_event : 1
