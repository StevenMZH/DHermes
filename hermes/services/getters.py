import subprocess
from typing import Dict, List, Union
from hermes.core.models import Server, App, Event
from hermes.core.global_vars import event_funcs, call_conditions
from hermes.internal.app import remote_access_cmd, pull_app, run_services_cmd, push_env_cmd
from hermes.internal.funcs import server_config, push_data, pull_data, remove_data, run_local, run_serverside
from hermes.internal.parser import load_hermesfile, hermesfile_parser


# Get Servers/Events
def get_global_data(hermes_file) -> Server|Event:
    raw_data = load_hermesfile(hermes_file)
    parsed_data = hermesfile_parser(raw_data)
    
    servers = get_servers(parsed_data)
    events = get_global_events(parsed_data)    

    return parsed_data, servers, events

# Servers/Events
def get_servers(parsed_file: Dict) -> Dict[str, Server]:
    servers = parsed_file.get("servers",{})
    if(servers):
        return servers 
    return None

def get_global_events(parsed_file: Dict) -> List[Event]:
    events = parsed_file.get("events",[])
    if(events):
        return events 
    return None

# Servers/Apps
def get_server(parsed_file: Dict, server_id:str) -> Server:
    servers = get_servers(parsed_file)
    if(servers):
        for id, server_data in servers.items():
            if(id == server_id):
                return server_data    
    return None
    
def get_apps(servers: Dict[str, Server]) -> List[App]:
    apps = {}
    if(servers):
        for server_id, server_data in servers.items():
            if server_data.apps:
                for app_id, app_data in server_data.apps.items():
                    apps[app_id] = app_data
                
    return apps            

def get_app(servers: Dict[str, Server], app_id:str) -> List[Server | App]:
    if servers:
        for server_id, server_data in servers.items():
            if(server_data.apps):
                for id, app_data in server_data.apps.items():
                    if(id == app_id):
                        return server_id, server_data, id, app_data

    return None, None



def get_server_events(parsed_file: Dict):
    pass