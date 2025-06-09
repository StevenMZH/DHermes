import os
from pathlib import Path
from click import echo
from hermes.core.models import Server
from hermes.internal.funcs import run_serverside

# Set Developer Enviroment for hermes to manage servers
def set_client():
    """
    Creates in the root of the system:
    - a directory '.hermes'
    - an empty file '.hermes' inside that directory
    - a subdirectory '.ssh' inside the '.hermes' directory
    """
    root_path = Path(os.path.abspath(os.sep))

    hermes_dir = root_path / ".hermes_client"
    ssh_dir = hermes_dir / ".ssh"
    hermes_file = hermes_dir / ".hermes"

    try:
        if not hermes_dir.exists():
            hermes_dir.mkdir()
            echo(f"Directory {hermes_dir} created.")
        else:
            echo(f"Directory {hermes_dir} already exists.")

        if not ssh_dir.exists():
            ssh_dir.mkdir()
            echo(f"Directory {ssh_dir} created.")
        else:
            echo(f"Directory {ssh_dir} already exists.")

        if not hermes_file.exists():
            hermes_file.touch()
            echo(f"File {hermes_file} created.")
        else:
            echo(f"File {hermes_file} already exists.")

    except PermissionError:
        echo(f"Error: You do not have permissions to create folders or files in {root_path}")
    except Exception as e:
        echo(f"Unexpected error: {e}")


# Set host enviroment for Apps & Services hostage
def set_server(server: Server):
    setup_cmds = [
        # Update & install Git
        'sudo apt-get update',
        'sudo apt-get install -y git',

        # Docker dependencies
        'sudo apt-get install -y ca-certificates curl gnupg lsb-release',

        'sudo mkdir -p /etc/apt/keyrings',
        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null',
        'sudo chmod a+r /etc/apt/keyrings/docker.gpg',

        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
        'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | '
        'sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',

        'sudo apt-get update',

        # Install Docker Engine and plugins
        'sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin',

        # Add user to docker group
        'sudo usermod -aG docker $USER',

        # Print versions
        'git --version',
        'docker --version',
        'docker compose version'
    ]
    run_serverside(server, setup_cmds)
 

# Set host enviroment for a event-driven server to manage event for service servers 
def set_manager():
    # Install dependencies
    pass

