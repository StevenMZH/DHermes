# DHermes — Multi-Server, Multi-App Enviroments Orchestrator (DevOps-as-Code)

Hermes is a robust and extensible environment manager designed to orchestrate complex DevOps workflows across multiple servers, applications, and services.

It provides a DevOps-as-Code interface that simplifies:

- Infrastructure provisioning
- Application deployment
- Service lifecycle management
- Event-driven automation
- Secure multi-server credentials handling

Built with flexibility and scalability in mind, Hermes allows teams to define environments declaratively using a lightweight DSL (YAML), enabling:

- Seamless coordination of distributed deployments
- Reusable, composable event hooks (e.g., onDeploy, onUpdate)
- Specific Environment server/app/service configurations
- Importable configuration modules for better DRY practices


## Use Cases
- Deploy microservices to different VMs with event-triggered hooks
- Spin up isolated dev/stage/prod environments with different configs
- Automate CI/CD operations per service/app/server or global
- Centralize infrastructure configuration in a single source of truth


## Hermes File Structure

```hermes.yml

# File Extends
import?:
    - ...

# Server Dict
servers?:

    # Server
    <id>:
    server_name?:
    credentials: # Must contain either file or the other fields
        file: ".env.hermes"  
        project_id: ...
        vm_name: ...
        host_address: ...
        user: ...
        ssh_key: ...
    env: <file>

    # Apps
    apps?:
        # Must contain repository+branch and/or images
        <id>:
        app_name?: 
        repository?: 
        branch?: 
        images?:
        - ...
        services: 
        events?: 
        - ...

    # Server service-compose
    services?: <server_compose> # no tested

# Event Dict (interrupt + body)
events?:

    # Event
    <id>:
    when?: (default=call)

    # Body (actions & in-time calls)
    push?: 
        - from: <path>
        to: <path=server_root>
        - ...
    pull?: 
        - from: <path=server_path> 
        to: <path=call_root>   
        - ...
    remove?: 
        - path: <path>
        - ...
    migrate?: 
        - from: <path> 
        to: <path>    
        - ...

    call?:
        - <event>: <scope=self> 

    run_local:
        - ...
    run_serverside:
        - ...

    # annonymous loop func
    loop?:
        break: <event>
        # ... funcs

```
