Docker Interactive Shell Runner
===============================

The `docker-shell` command makes it quick and easy to start an interactive shell inside a Docker container, with the following features:

- Both Windows and Linux containers are supported.

- The current working directory is automatically bind-mounted into the container and set as the container's working directory.

- When running Linux containers under Linux host systems, [host networking mode](https://docs.docker.com/network/host/) is enabled automatically to eliminate the need for exposing individual ports or port ranges.

- GPU support is automatically enabled when running GPU-enabled Linux containers under Linux host systems with the NVIDIA binary drivers and the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) installed.

- Short aliases are provided for running popular shells:
  
  - `dbash` for [GNU Bash](https://www.gnu.org/software/bash/)
  - `dsh` for the [Bourne shell]()
  - `dzsh` for [Zsh](https://www.zsh.org/)
  - `dcmd` for the Windows Command Prompt
  - `dps` and `dpowershell` for [PowerShell](https://docs.microsoft.com/en-us/powershell/)


## Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic usage](#basic-usage)
  - [Passing additional flags to Docker](#passing-additional-flags-to-docker)
  - [Working with alias tags](#working-with-alias-tags)
- [Legal](#legal)


## Installation

To install `docker-shell`, run the following command:

```bash
# This may need to be prefixed with sudo under Linux and macOS
pip3 install docker-shell
```


## Usage

### Basic usage

To start a GNU Bash shell in an [official Python container](https://hub.docker.com/_/python) under Windows, macOS or Linux, run either of the following commands:

```bash
# Long version
docker-shell bash python

# Short version
dbash python
```

To start a Windows Command Prompt in a [Windows Server Core container](https://hub.docker.com/_/microsoft-windows-servercore) under Windows, run either of the following commands:

```bash
# Long version
docker-shell cmd mcr.microsoft.com/windows/servercore:ltsc2019

# Short version
dcmd mcr.microsoft.com/windows/servercore:ltsc2019
```

To start a PowerShell session in a [Windows Server Core container](https://hub.docker.com/_/microsoft-windows-servercore) under Windows, run any of the following commands:

```bash
# Long version
docker-shell powershell mcr.microsoft.com/windows/servercore:ltsc2019

# Short versions
dps mcr.microsoft.com/windows/servercore:ltsc2019
dpowershell mcr.microsoft.com/windows/servercore:ltsc2019
```

### Passing additional flags to Docker

Any additional flags that are specified on the command-line will be propagated automatically to the underlying [docker run](https://docs.docker.com/engine/reference/run/) command:

```bash
# The flags `-u 1000 --name mycontainer` will be passed directly to Docker
docker-shell bash python -u 1000 --name mycontainer
```

### Working with alias tags

When working with lengthy image tags it is often more convenient to use the [docker tag](https://docs.docker.com/engine/reference/commandline/tag/) command to create concise aliases, for example:

```bash
# Add a shorter tag alias for the Windows Server Core image
docker tag mcr.microsoft.com/windows/servercore:ltsc2019 windows:latest

# Run a Windows Command Prompt using the short tag
dcmd windows
```


## Legal

Copyright &copy; 2020, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/docker-shell/blob/master/LICENSE) for details.
