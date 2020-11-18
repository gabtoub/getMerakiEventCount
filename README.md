# getMerakiEventCount
Displays count of an event type from Meraki Dashboard  on a defined time frame

## Prerequisites

- Meraki Dashboard API access , see documentation here : https://documentation.meraki.com/General_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API

## Installation

#### Clone the repo
```
$ git clone https://github.com/gabtoub/getMerakiEventCount.git
```

#### Set up a Python venv
Python3 needs to be installed on the machine. 
Creating a virtual environment is recommended. 

##### Install virtualenv via pip
```
$ pip install virtualenv
```

##### Create a new virtual environment
```
Change to your project folder
$ cd getMerakiEventCount

Create virtual environment
$ virtualenv venv

Activate virtual environment
$ source venv/bin/activate
```

#### Install dependencies
```
$ pip install -r requirements.txt
```

## How to Use 

- -k / --key : provide API key - optional (or set in environment variable as meraki_apikey)
- -o / --org : set an organization ID - optional
- -n / --net : set a network ID - optional
- -s / --span : set the time span (in days) - optional
- -t / --type : set event type - mandatory (syslog notation)
- -p / --product : set product type - mandatory
    
### Details

Default time span : 1 day 

If no Org ID is provided, the scripts displays the organizations available

    python getMerakiEventCount.py -p wireless
    Using default timespan : 1 day
    Please set Org ID in parameters - available organizations :
    Organization : 549236, Name : DevNet Sandbox
    Organization : 463308, Name : DevNet San Jose


Available product types  :

    wireless, appliance, switch, systemsManager, camera, cellularGateway,  environmental

## Examples : 
Getting DFS Events count for all networks in Org ID 549236

    python getMerakiEventCount.py -p wireless -t dfs_event -o 549236
    
    Using default timespan : 1 day
    Timespan : between 2020-11-14 16:37:07.722869 and 2020-11-15 16:37:07.722869
    Network : DevNet Sandbox ALWAYS ON , Number of dfs_event : 17
    Network : DNSMB3 , Number of dfs_event : 0
    Network : DNSMB2 , Number of dfs_event : 1
