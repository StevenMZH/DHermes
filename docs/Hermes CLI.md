# Hermes CLI Commands


### Client Setup (setup-client)
- hermes setup-client

### Server Setup (setup-server)
- hermes setup-server <server: id> --hermesfile <path=hermes.yml>

### Establish connection to a Server (connect)
- hermes connect <server: id> --hermesfile <path=hermes.yml>

### Remote Access to a Server (access)
- hermes access <server: id> --hermesfile <path=hermes.yml>


### Deploy App/s (deploy)
scopes: {all, server, app}

- hermes deploy --<scope=all> <object: id> --hermesfile <path=hermes.yml>

### Run Objects Events (run)
scopes: {all, server, app}

- hermes deploy --<scope=all> <object: id> --hermesfile <path=hermes.yml>

### Call an event inside a context scope (call)
scopes: {all, server, app}

- hermes deploy --<scope=all> <object: id> --hermesfile <path=hermes.yml>

### List Objects
- hermes list --hermesfile <path=hermes.yml>



