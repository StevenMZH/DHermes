import getpass
import subprocess
from click import echo, prompt
from hermes.core.models import Server
from hermes.internal.keys import sshKey_path, set_keys

def transfer_keys(ssh_path: str, server_name: str, server: Server):
    zone = prompt('Zone: ')

    with open(ssh_path + ".pub", "r") as f:
        pub_key = f.read().strip()

    user = getpass.getuser()  # usuario local actual

    # Escapamos cualquier comilla simple dentro de la clave (por si acaso)
    pub_key_safe = pub_key.replace("'", "'\"'\"'")

    # Agregamos mensaje y clave pública
    remote_command = (
        f"echo '# Added by Hermes ({user})' >> ~/.ssh/authorized_keys && "
        f"echo '{pub_key_safe}' >> ~/.ssh/authorized_keys && "
        "chmod 600 ~/.ssh/authorized_keys"
    )

    command = (
        f"gcloud compute ssh {server.user}@{server_name} "
        f"--project={server.project_id} --zone={zone} "
        f'--command="{remote_command}"'
    )

    try:
        subprocess.run(command, check=True, shell=True)
        echo('Public key added to authorized_keys on remote instance')
    except subprocess.CalledProcessError as e:
        echo(f"Error al transferir la clave pública: {e}")



def set_connection(server_name:str, server: Server, provider: str = 'GCP'):
    ssh_path = set_keys(server_name)
    transfer_keys(ssh_path, server_name, server)
    
    

def access_server(server_name: str, server:Server):
    ssh_path = sshKey_path(server_name)
    ssh_path_quoted = f'"{ssh_path}"'

    command = f'ssh -i {ssh_path_quoted} {server.user}@{server.host_address}'

    echo(f"Connecting via SSH to {server.user}@{server.host_address} ({server_name})")

    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        echo(f"Error connecting to the server via SSH: {e}")




    
