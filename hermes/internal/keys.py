import os
from pathlib import Path
from click import echo
from hermes.core.models import Server

# Create keys
def sshKey_path(key_name):
    root = Path(os.path.abspath(os.sep)) 
    ssh_path = str(root / ".hermes_client" / ".ssh" / key_name)
    return ssh_path 

# Send Public Key
def set_keys(name: str) -> str:
    from hermes.internal.funcs import run_local
    ssh_path = sshKey_path(name)
    
    if os.path.exists(ssh_path) and os.path.exists(ssh_path):
        echo(f"SSH key already exists at {ssh_path}")
    else:
        echo("Generating keys...")
        run_local([f'ssh-keygen -t rsa -b 4096 -f "{ssh_path}" -N ""'])
        echo("Keys Generated\n")
    
    return ssh_path

# Use Private key
def remote_access_cmd(server:Server):
    return ["ssh", "-i", server.ssh_key, f"{server.user}@{server.host_address}"]
   