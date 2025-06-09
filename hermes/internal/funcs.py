from typing import Dict, List
import os
import click
import subprocess
from hermes.core.models import Server, App
 
def run_serverside(server: Server, commands: List[str]):
    from hermes.internal.keys import remote_access_cmd
    
    command_str = " && ".join(commands)
    ssh_cmd = remote_access_cmd(server) + [command_str]
    result = subprocess.run(ssh_cmd, capture_output=True, text=True)
    click.echo(f"({server.server_name}): {result.stdout}")
    if result.stderr:
        click.echo(f"({server.server_name}) [error]: {result.stderr}")

def run_local(commands: List[str]):
    command_str = " && ".join(commands)
    result = subprocess.run(command_str, check=True, capture_output=True, text=True, shell=True)
    click.echo(f"(local): {result.stdout}")
    if result.stderr:
        click.echo(f"(local): {result.stderr}")


def push_data(server: Server, local_path: str, remote_path: str = None):
    local_path = get_relative_file(local_path)
    if not os.path.isfile(local_path):
        click.echo(f"File not found: {local_path}")
        return

    scp_cmd = ["scp", "-i", server.ssh_key, local_path, f"{server.user}@{server.host_address}:{remote_path}"]
    subprocess.run(scp_cmd, shell=False)
    click.echo(f"Push to {server.server_name}")

def pull_data(server: Server, remote_path: str, local_path: str):
    local_path = get_relative_file(local_path)
    if(local_path):
        scp_cmd = ["scp", "-i", server.ssh_key, f"{server.user}@{server.host_address}:{remote_path}", local_path]
        subprocess.run(scp_cmd, shell=False)
        click.echo(f"Pull from {server.server_name}")
        

def remove_data(server: Server, paths: List[str]):
    cmds = [f"rm -rf {path}" for path in paths]
    run_serverside(server, cmds)
    click.echo(f"Remove {paths} from {server.server_name}")
    
    

def get_relative_file(local_path:str = ""):
    abs_path = os.path.abspath(os.path.join(os.getcwd(), local_path))
    return abs_path 
    
def server_config(data: List[str]):
    pass
