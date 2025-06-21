import click
from hermes.services.deploy import deploy_all, deploy_server, deploy_app
from hermes.services.events import run_event, run_event_list
from hermes.services.getters import get_global_data, get_app, get_server
from hermes.services.connect import set_connection, access_server
from hermes.internal.setup import set_client, set_server, set_manager

@click.group()
def cli():
    """Hermes CLI - (DOaC) DevOps as Code """
    pass

# Setups
@cli.command()
def setup_client():
    """
    Set up local host as a Client, prepares the workspace for setting DevOps & Server management 
    """
    try:
        set_client()
    except(Exception):
        click.echo('Error during the Client Setup')

@cli.command()
@click.argument('server')
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
def setup_server(hermesfile, server):
    """
    Set up remote host as a Server, prepares the workspace to host multiple apps & services
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    server_data = get_server(parsed_data, server)
    
    if not servers_data:
        click.echo('No server defined')
        return
    elif not server_data:
        click.echo(f'{server} Server not defined')
        return
    
    try:
        click.echo(f"Setting Up Server (This may take a few minutes) ...")
        set_server(server_data)
        click.echo(f"Setup complete. The server is ready to receive deployments.")
    
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        

# Connections
@cli.command()
@click.argument('server')
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
def connect(server, hermesfile):
    """
    Set up connection between the Local Client and a Server
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    server_data = get_server(parsed_data, server)
    
    if not servers_data:
        click.echo('No server defined')
        return
    
    if (server_data):
        set_connection(server, server_data)
    else:
        click.echo('Define the scope --all, --server or --app, and provide the specific location to run it')
        
@cli.command()
@click.argument('server')
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
def access(server, hermesfile):
    """
    Access via SSH to a Server 
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    server_data = get_server(parsed_data, server)
    
    if not servers_data:
        click.echo('No server defined')
        return
    
    if (server_data):
        access_server(server, server_data)
    else:
        click.echo('Define the scope --all, --server or --app, and provide the specific location to run it')
        
        

@cli.command()
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (por defecto: ./hermes.yml)")
@click.option('--all', is_flag=True, default=True, help="Deploy all servers and projects.")
@click.option('--server', default=None, help="Deploy only the specified server.")
@click.option('--app', default=None, help="Deploy only the specified app_data across all servers.")
def deploy(hermesfile, all, server, app):
    """
    Deploy servers/apps/services based on the configuration file.
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    if not servers_data: return
    
    # Specific Server Deploy
    if server:        
        servers_data = servers_data.get(server, None)
        if not servers_data:
            click.echo(f"Server {server} not found")
            return

        click.echo(f"Deploying server: {server}")
        deploy_server(servers_data)
              
    # Specific App Deploy
    elif app:
        appHost, appHost_data, app_id, app_data  =  get_app(servers_data, app)
        if app_data:
            click.echo(f"Deploying App: {app}")
            deploy_app(appHost_data, app_data)
            return

        click.echo(f"App not found: {server}")
                   
    # Default: Deploy All
    elif all:
        click.echo("Deploying all servers and apps")
        deploy_all(parsed_data)
    else:
        click.echo("No deployment target specified. Use --all, --server or --app.")


@cli.command()
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
@click.option('--all', is_flag=True, default=True, help="Set the scope to Global.")
@click.option('--server', default=None, help="Set the scope to the specified server.")
@click.option('--app', default=None, help="Set the scope to the specified app.")
@click.option('--event', default=None, help="Set the event to call.")
def run(hermesfile, all, server, app, event):
    """
    Run Event from the specified scope 
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    if not servers_data: return
    
    if server:
        servers_data = parsed_data.get('servers', []).get(server)
        if servers_data:
            for app_ip, app_data in servers_data.apps.items():
                run_event_list(servers_data, events_data, app_data)
        else: click.echo('Server not defined') 
        
    elif app:
        appHost, appHost_data, app_id, app_data  =  get_app(servers_data, app)
        if(app_data): run_event_list(appHost_data, events_data, app_data)
            
    elif all: 
        event_data = parsed_data['events'].get(event, None)
        for server_id, servers_data in parsed_data.get('servers', []).items():
            for app_ip, app_data in servers_data.apps.items():
                run_event_list(servers_data, events_data, app_data)

    else:
        click.echo('Define the scope --all, --server or --app, and provide the specific location to run it')
        
        
@cli.command()
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
@click.option('--server', help="Set the scope to the specified server.")
@click.option('--event', help="Set the event to call.")
def call(hermesfile, server, event):
    """
    Run Event inside the specified scope 
    """
    parsed_data, servers_data, events_data = get_global_data(hermesfile)
    if not servers_data: return
    
    if (event and server):
        event_data = parsed_data.get('events', []).get(event)
        servers_data = parsed_data.get('servers', []).get(server)

        if servers_data:
            run_event(servers_data, events_data, event_data)
        else: click.echo('Server not defined')
          
    else:
        click.echo('Define the scope --all, --server or --app, and provide the specific location to run it')
               
    
@cli.command()
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (por defecto: ./hermes.yml)")
@click.option('--all', is_flag=True, default=False, help="Run global initialization process.")
@click.option('--server', default=None, help="Run the specified server initialization process.")
@click.option('--app', default=None, help="Run the specified app initialization process.")
def init(hermesfile, all, server, app):
    run(hermesfile, all, server, app, 'init')


@cli.command()
@click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
def list(hermesfile):
    """
    List all Hermes Objects (Servers, Apps, Events) on the current configuration.
    """
    parsed_data, servers, events = get_global_data(hermesfile)
    if not servers: return
    servers = parsed_data.get('servers', {})
        
        
    # List Servers
    click.echo(f"\n")
    for server_id, servers_data in servers.items():

        click.echo(f"(Server) {server_id}")    

        # List Apps & its Events
        if servers_data.apps:
            for app_id, app_data in servers_data.apps.items():
                click.echo(f"\t(App) {app_id}")    
                for id, event in app_data.events.items():
                    click.echo(f"\t\t({event.when} Event) {id}")
        
    # List Events
    click.echo(f"\n")
    if events: 
        for event_id, event_data in parsed_data.get('events', None).items():
            click.echo(f"({event_data.when} Event) {event_id}")    
        click.echo(f"\n")


# @cli.command()
# @click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
# @click.option('--servers', is_flag=True, default=False, help="Run global initialization process.")
# @click.option('--services', default=None, help="Run the specified server initialization process.")
# def status(hermesfile, servers, services):
#     """
#     List Servers or its Services status
#     """
#     click.echo(f"Under Development")            
#     return


# @cli.command()
# @click.argument('origin')
# @click.argument('target')
# @click.option('--hermesfile', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
# def migrate(origin, target, hermesfile):
#     raw_config = load_hermesfile(hermesfile)
#     parsed_data = hermesfile_parser(raw_config)
#     click.echo(f'{origin} to {target}')
#     click.echo('Under Development')
    


def main():
    cli()

if __name__ == "__main__":
    cli()
