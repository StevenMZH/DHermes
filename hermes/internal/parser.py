import os
from typing import Dict, List
import yaml
from hermes.core.models import Server, App, Event
from hermes.core.global_vars import event_funcs, call_conditions
from hermes.internal.keys import sshKey_path

def load_hermesfile(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file) or {}


def hermesfile_parser(data: dict) -> dict:
    imported_data = {'servers': {}, 'events': {}}
    events = event_parser(data.get('events', {})) or {}
    servers = {}
    apps = {}
    
    for file in data.get('import', {}):
        raw_data = load_hermesfile(file)
        parsed_data = hermesfile_parser(raw_data)
        imported_data['servers'] = imported_data['servers'] | parsed_data['servers']
        imported_data['events'] = imported_data['events'] | parsed_data['events']
    events = events | imported_data['events']

    for server_key, server_info in data.get('servers', {}).items():
        # Credentials Validations
        has_credentials_file = 'server_credentials' in server_info
        has_individual_fields = all(
            field in server_info
            for field in ['user', 'project_id', 'vm_name', 'host_address']
        )
        
        if not (has_credentials_file or has_individual_fields):
            raise ValueError(
                f"'{server_key}' should have server_credentials' "
                f"or its equivalent fields (user, project_id, vm_name, host_address)"
            )

        # Apps
        raw_apps = server_info.get('apps', None)
        if(raw_apps):
            apps = apps_parser(raw_apps, events)
   
        # Server Object
        if 'server_credentials' in server_info:
            credentials = serverCredentials_parser(server_info['server_credentials'])
        else:
            credentials = {
                'user': server_info['user'],
                'project_id': server_info['project_id'],
                'vm_name': server_info['vm_name'],
                'host_address': server_info['host_address'],
                'ssh_key': server_info['ssh_key']
            }
            
        # SSH Key    
        if(credentials['ssh_key'] == None):
            credentials['ssh_key'] = sshKey_path(server_key)

        server = Server(
            server_name=server_info.get('server_name', server_key),
            
            user=credentials['user'],
            project_id=credentials['project_id'],
            vm_name=credentials['vm_name'],
            host_address=credentials['host_address'],
            ssh_key=credentials['ssh_key'],
            
            env=server_info.get('env', None),
            
            apps=apps,
            events=events
        )

        servers[server_key] = server
    return {"servers": imported_data['servers'] | servers, "events": imported_data['events'] | events}



def serverCredentials_parser(env_path: str) -> dict:
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"server_credentials .env file not found: {env_path}")

    env_vars = {}

    with open(env_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")

    required_fields = ['user', 'project_id', 'vm_name', 'host_address']
    missing = [f for f in required_fields if f not in env_vars]

    if missing:
        raise ValueError(f"server_credentials .env file in ({env_path}) don't have the required fields: {', '.join(missing)}")

    return {
        'user': env_vars['user'],
        'project_id': env_vars['project_id'],
        'vm_name': env_vars['vm_name'],
        'host_address': env_vars['host_address'],
        'ssh_key': env_vars.get('ssh_key', None)
    }


# Object Parsers
def apps_parser(raw_apps: List[str], events:Dict[str, Event]) -> Dict[str, App]:
    if (raw_apps == None): 
        return None
    
    apps = {}
    for key, app in raw_apps.items():
        events = {event: events.get(event, None) for event in app.get('events', [])}

        apps[key] = App(
            name = app.get('app_name', key),
            repository = app.get('repository', None),
            branch = app.get('branch', None),
            images = app.get('images', None),
            services = app.get('services', None),
            events = events,
        )
    return apps
    

def event_parser(events: Dict[str, "Event"]) -> List[Event]:
    """
    Event:
        when: str
        func: List[Dict[command_name:str, List[content:str]] | Event]

    Args:
        events (Dict[str, &quot;Event&quot;]):

    Returns:
        List[Event]: 
    """
    if not events:
        return None
    
    parsed_events = {}    
    
    for name, event in events.items():
        breaker = event.get('break', None)
        when = event.get('when', "inline" if breaker else "call")
        funcs = []
        for command, content in event.items():
            # Event Commands
            if(command == 'loop'):
                funcs.append(event_parser({"loop": content}))

            elif(command in event_funcs): 
                funcs.append({command: content})

            elif(command == 'when'):
                when = name if name in call_conditions else "inline" if event.get('breaker') and not when else when
            elif(command == 'breaker'):
                breaker = command

            # Nested Event
            else:
                funcs.append( {command: Event(
                    when = name if name in call_conditions else "inline" if event.get('breaker') and not when else when,
                    breaker = breaker,
                    funcs = content
                )})
            
        parsed_events[name] = (Event(
            when = name if (name in call_conditions) else when, # explicite specified, elif name, if it's a call_condition, else call
            breaker = breaker,
            funcs = funcs # bulit-in funcs, loops or break
        ))
    return parsed_events # Dict[str, Event( List[List[function_name, content]] )]
    
                
        

