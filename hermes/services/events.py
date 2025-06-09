import subprocess
from typing import Dict, List
from hermes.core.global_vars import event_funcs, call_conditions
from hermes.core.models import Server, App, Event
from hermes.internal.app import remote_access_cmd, pull_app, run_services_cmd, push_env_cmd
from hermes.internal.funcs import server_config, push_data, pull_data, remove_data, run_local, run_serverside
import click
from .getters import get_server

def run_event(server:Server, events:List[Event], event: Event):
    when = event.when
    funcs = event.funcs
    for func in funcs:
        command, content = next(iter(func.items()))
        # Special Keys
        if(command == 'loop'):
            while(True):
                out = run_event(server, content)
                if(out == 'break'): 
                    break

        elif(command == 'call'):
            for call in content:
                for id, scope in call.items():
                    run_event(server, events, events.get(id, None))
                

        # Build-In Functions
        elif(command == 'server_config'): server_config(content)
        elif(command == 'push'): [push_data(server, func.get('from'), func.get('to', None)) for func in content]
        elif(command == 'pull'): [pull_data(server, func.get('from'), func.get('to', None)) for func in content]
        elif(command == 'remove'): [remove_data(server, func.get('path')) for func in content]
        elif(command == 'run_local'): run_local(content)
        elif(command == 'run_serverside'): run_serverside(server, content)



def run_event_list(server:Server, events:List[Event], app:App):
    for event_id, event_data in app.events.items():
        click.echo(f"({event_id} Event) called\n")
        if(event_data.when == 'call'):
            run_event(server, events, event_data)

def before():
    pass

def before_deploy():
    pass

def after():
    pass

def after_deploy():
    pass

def after_sucess():
    pass

def after_failure():
    pass



