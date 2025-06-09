import subprocess
import click
from typing import Dict, Union
from hermes.core.models import Server, App
from hermes.internal.app import remote_access_cmd, pull_app, run_services_cmd, push_env_cmd

def deploy_all(servers: Dict[str, Server]):
    for server in servers['servers'].values():
        deploy_server(server)

def deploy_server(server: Server):
    # Updating Apps Changes
    if server.apps:
        for app_id, app_data in server.apps.items():
            pull_app(server, app_data)

        # Build/Run Global Services
        if server.services:
            subprocess.run(remote_access_cmd(server) + run_services_cmd(server.services), shell=False)

        # Run Services
        else:
            if server.apps:
                for app_id, app_data in server.apps.items():
                    if app_data.services:
                        run_services(server, app_data, app_id)


def deploy_app(server:Server, app: App):
    # Updating App Changes
    pull_app(server, app)

    # Running Services
    for app_id, app_data in server.apps.items():
        if app_data.services: run_services(server, app_data, app_id)
    

def run_services(server:Server, app: App, id:str):
    click.echo(f"Running {id} services: {app.services}")
    docker_cmd = f"cd {app.name} && docker compose -f {app.services} up -d && cd .."
    push_env_cmd(server, app.name)
    subprocess.run(remote_access_cmd(server) + [docker_cmd], shell=False)