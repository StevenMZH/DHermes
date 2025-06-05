from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union

@dataclass
class Server_Config:
    config: Optional[str] = None

@dataclass
class Event:
    # Auto-called: before, before-deploy, after, after-deploy, after-external-deploy, after-sucess, after-failure
    # Build-in Functions: server_config, push, pull, remove, run_local, run_serverside, 'break' 
    when: str = "call"
    breaker: str = "call"
    funcs: List[Union[str, "Event"]] = None
    

@dataclass
class App:
    name: str
    repository: Optional[str]
    branch: Optional[str]
    images: Optional[List[str]]
    services: Optional[str] = None
    
    events: Optional[List[Union[str, "Event"]]] = None


@dataclass
class Server:
    # Meta
    server_name: Optional[str]
    
    # Credentials
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



