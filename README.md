# Checkmk extension devcontainer template

## Description

This is a template to develop Checkmk Extensions derived from the original made by [Marius Rieder](https://github.com/jiuka/)

## Development

For the best development experience use [VSCode](https://code.visualstudio.com/) with the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension. This maps your workspace into a checkmk docker container giving you access to the python environment and libraries the installed extension has.

## Directories

The following directories in this repo are getting mapped into the Checkmk site.

* `agents`, `checkman`, `checks`, `doc`, `inventory`, `notifications`, `web` are mapped into `local/share/check_mk/`
* `agent_based` is mapped to `local/lib/check_mk/base/plugins/agent_based`
* `nagios_plugins` is mapped to `local/lib/nagios/plugins`
* `bakery` is mapped to `local/lib/check_mk/base/cee/plugins/bakery`
* `temp` is mapped to `local/tmp` for storing precreated agent output
