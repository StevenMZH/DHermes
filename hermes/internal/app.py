import subprocess
import click
from typing import Dict
from hermes.core.models import Server, App
from hermes.internal.keys import remote_access_cmd

def push_env_cmd(server:Server, app_name:str):
    remote_path = f"{server.user}@{server.host_address}:/home/{server.user}/{app_name}/.env.dev"
    scp_cmd = ["scp", "-i", server.ssh_key, server.env, remote_path]
    subprocess.run(scp_cmd, shell=False)
    
def pull_app(server:Server, app: App):
    click.echo(f"Deploying {app.name} changes")
    if(app.repository):
        pull_cmd= [f"""
            if [ ! -d {app.name} ]; then
                git clone -b {app.branch} {app.repository} {app.name};
            else
                cd {app.name} && git pull origin {app.branch} && cd ..;
            fi
        """]
        subprocess.run(remote_access_cmd(server) + pull_cmd, shell=False) 
        
    # elif (app.images):
    #     pass
    
def run_services_cmd(services):
    return [f"docker compose -f {services} up -d"]

def run_project(app: App, cmd:str):
    docker_cmd = f"cd {app.app_name} && docker-compose -f {app.services} up -d && cd .."
    subprocess.run(remote_access_cmd() + [docker_cmd], shell=False)

