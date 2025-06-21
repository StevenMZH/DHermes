# Hermes-file Structure

Hermes-files are composed of 3 main segments (neither of them have to be defined for the file to be ran):

## import

Import segment it's a path list, use to extend the file with other hermes-files, adding foreign events & servers to the local segments, capable of managing chain imports from multiple files 

```hermes.yml
import?:
  - <hermesfile2-path>
  - <hermesfile3-path>
  - ...
```

## servers

The servers segment is a dictionary with a string key, and an Server value. 

```
servers:
  <server-id>:
    server_name?: ""
    credentials: # Must contain either the path to the .env file or the following fields
      project_id: ...
      vm_name: ...
      host_address: ...
      user: ...
      ssh_key: ... # If your using hermes connect system don't add this field

    env: <path>

	# Dictionarty with string keys and App values 
    apps?:
    
      <id>:
        # Must contain repository+branch and/or images
        app_name?: 
        repository?:
        branch?:
        images?:
        - ...
        services: <docker-compose.yml>
        events?:
        - ...

    # server servicer-compose
    services?: <server_compose> 

```
## events

The events segment is a dictionary with a string key, and an Event value. 

```hermes.yml
events?:

  <event-id>:
    when?: (default=call)
    
	<action>?:
		<arguments>

	<action2>?:
		<arguments>

```

