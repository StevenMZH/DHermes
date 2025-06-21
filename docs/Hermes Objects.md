# Hermes Objects

## Server

```python
@dataclass
class Server:
    # Meta
    server_name: Optional[str]

    # Cloud Service Credentials
    user: str
    project_id: str
    vm_name: str
    host_address: str    
    ssh_key: str
    env: str

    # Global Services
    services: Optional[str] = None    
    
    # Apps & Events (Objects)
    apps: Optional[Dict[str, App]] = None
    events: Optional[Dict[str, "Event"]] = None
```
## App

```python
@dataclass
class App:
	# Meta
    name: str

	# Deployment Content
    repository: Optional[str]
    branch: Optional[str]
    images: Optional[List[str]]

	# Service Orchestrator (docker-compose)
    services: Optional[str] = None

	# Event
    events: Optional[List[Union[str, "Event"]]] = None
```
## Event (Interrupts + Functions)

```python
@dataclass
class Event:

    # Auto-called: before, before-deploy, after, after-deploy, after-external-deploy, after-sucess, after-failure
    # Build-in Functions: server_config, push, pull, remove, run_local, run_serverside, 'break'

    when: str = "call"
    breaker: str = "call"

    funcs: List[Union[str, "Event"]] = None

```
