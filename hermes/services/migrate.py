from typing import Dict, List
import subprocess
from hermes.core.models import Server, Project

def migrate(server1: Server, server2:Server, origin_path: list[str], destination_path: str):
    # Create a hermes.migration.yml (Contain instruction to push to destination & delete local files)
    # push hermes.migration.yml to origin
    # install hermes dependencies if it's needed
    # local command to execute hermes.migration.yml
    # send message to local
    # local rm hermes.migration.yml files & dependecies no previously installed
    pass