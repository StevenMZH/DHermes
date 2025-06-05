import click
from services.deploy import deploy_all, deploy_server, deploy_app
from services.events import run_event, run_event_list
from services.getters import get_global_data, get_app


@click.group()
def cli():
    """Hermes CLI - (DOaC) DevOps as Code """
    pass


@cli.command()
@click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (por defecto: ./hermes.yml)")
@click.option('--all', is_flag=True, default=True, help="Deploy all servers and projects.")
@click.option('--server', default=None, help="Deploy only the specified server.")
@click.option('--app', default=None, help="Deploy only the specified app_data across all servers.")
def deploy(hermes_file, all, server, app):
    """
    Deploy services based on the configuration file.
    """
    parsed_data, servers_data, events_data = get_global_data(hermes_file)
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
@click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
@click.option('--all', is_flag=True, default=True, help="Set the scope to Global.")
@click.option('--server', default=None, help="Set the scope to the specified server.")
@click.option('--app', default=None, help="Set the scope to the specified app.")
@click.option('--event', default=None, help="Set the event to call.")
def run(hermes_file, all, server, app, event):
    parsed_data, servers_data, events_data = get_global_data(hermes_file)
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
@click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
@click.option('--server', help="Set the scope to the specified server.")
@click.option('--event', help="Set the event to call.")
def call(hermes_file, server, event):
    parsed_data, servers_data, events_data = get_global_data(hermes_file)
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
@click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (por defecto: ./hermes.yml)")
@click.option('--all', is_flag=True, default=False, help="Run global initialization process.")
@click.option('--server', default=None, help="Run the specified server initialization process.")
@click.option('--app', default=None, help="Run the specified app initialization process.")
def init(hermes_file, all, server, app):
    run(hermes_file, all, server, app, 'init')


@cli.command()
@click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
def list(hermes_file):
    """
    List all servers on the current configuration.
    """
    parsed_data, servers, events = get_global_data(hermes_file)
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
# @click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
# @click.option('--servers', is_flag=True, default=False, help="Run global initialization process.")
# @click.option('--services', default=None, help="Run the specified server initialization process.")
# def status(hermes_file, servers, services):
#     """
#     List Servers or its Services status
#     """
#     click.echo(f"Under Development")            
#     return


# @cli.command()
# @click.argument('origin')
# @click.argument('target')
# @click.option('--hermes_file', default='hermes.yml', type=click.Path(exists=True), help="Path to hermes.yml file (def: ./hermes.yml)")
# def migrate(origin, target, hermes_file):
#     raw_config = load_hermesfile(hermes_file)
#     parsed_data = hermesfile_parser(raw_config)
#     click.echo(f'{origin} to {target}')
#     click.echo('Under Development')
    


def main():
    cli()

if __name__ == "__main__":
    cli()
