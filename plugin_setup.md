# NetBox Plugin Development environment

A development environment to development NetBox plugins. Provides a instance of NetBox and facilities
to automatically set up the plugin within NetBox.

## Devenv Setup

 1. Run `setup.sh` or clone netbox into ./netbox
 2. Mark directory ./netbox/netbox as a source directory in PyCharm. This enables usage of imports in from netbox in PyCharm
 3. Set up your plugin now if this is a new project
 4. Build the docker container
 5. Configure .env with .env.example
 6. docker-compose.yml can now be used to launch the environment

> Note: The container needs to be rebuilt on every change in `plugins/your_plugin/setup.py`, `netbox_config.py` or `requirements.txt`.

## Plugin setup

 1. Update the files `plugins/plugin_template`
    - Rename both directories
    - Edit `setup.py` and `__init__.py` with plugin details
 2. Add the plugin name to `netbox_config.py`
 3. Add any requirements for development in `requirements.txt` (do not add requirements of your plugin, define those in `setup.py`)


### Notes

NetBox plugins are Django modules. See the relevant documentation for Django modules for general purpose information.
NetBox exposes specific modules for plugins. See here on how to use them: https://netbox.readthedocs.io/en/stable/plugins/development/
