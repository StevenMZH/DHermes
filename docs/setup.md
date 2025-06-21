
## Installation

### Install Pip package:

```
pip install hermes-deployer
```
### or Executable:

```

```


## Client Setup

```CLI
hermes setup-client
```


## Server Setup

Requirements: The proyects to be able to be ran correctly must be dockerized, otherwise to properly run it, you must defined the actions to make.

First, download the SDK of the cloud service hosting your server, and login.

- Define the desire server into a Hermes-file (hermes.yml), with at least the following minimum configurations:

```hermes.yml
servers:
  <server-id>:
    server_credentials: <.env-path>
```

- If it's the first time managing the server with Hermes, run:

```CLI
hermes setup-server <server-id>
```

- If its's the first time managing the server with Hermes from this host, run:

```CLI
hermes connect <server-ip>
```

