# Suricata & Ansible Management

This project provides a graphical interface (GUI) for managing Suricata and Ansible configurations. Built using Python's Tkinter library, the application integrates with Ansible playbooks to automate key tasks such as Suricata installation, inventory management, log monitoring, and custom rule handling. The project was developed as part of a university assignment for the Networks and Systems Administration course at Instituto Politécnico de Viana do Castelo. It was supervised by Assistant Guest Prof. Silvestre Malta (PhD) under the subject "Projeto 1."

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Ansible Playbooks](#ansible-playbooks)
- [File Structure](#file-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Inventory Management**: Add, load, and delete servers from the inventory.
- **Install Suricata**: Install and configure Suricata on remote servers.
- **View Suricata Logs**: View and export Suricata logs as a txt.
- **Custom Rules Management**: Add, view, and delete custom Suricata rules.
- **Analyze Logs**: Load and filter log files by IP, date, and protocol.

## Prerequisites

- Python 3.x
- Tkinter
- Ansible

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Tomsferreira16/ansible_projeto1.git
    cd ansible_projeto1
    ```

2. Ensure Ansible is installed:
    ```sh
    sudo apt-get update
    sudo apt-get install ansible
    ```

## Usage

1. Run the application:
    ```sh
    chmod +x SAM.py
    ./SAM.py
    ```
Warning: Don't run the application in background or else the setup tab will not work!

2. Use the GUI to manage your Suricata and Ansible configurations:
    - **Setup Tab**: Generate and copy SSH keys to remote servers, and manage SSH identities.
    - **Inventory Tab**: Add, load, and delete servers.
    - **Install Suricata Tab**: Install Suricata on remote servers.
    - **Suricata Logs Tab**: View and export Suricata logs.
    - **Custom Rules Tab**: Add, view, and delete custom Suricata rules.
    - **Analyze Logs Tab**: Load and filter log files.

## Ansible Playbooks

The following playbooks are included in the project:

- **install_suricata.yml**: Installs and configures Suricata.
- **read_log.yml**: Reads the Suricata `fast.log` file.
- **ls_ssh_keys.yml**: Lists SSH keys on remote servers.
- **add_custom_rule.yml**: Adds a custom Suricata rule.
- **delete_custom_rule.yml**: Deletes a custom Suricata rule.
- **view_custom_rules.yml**: Views custom Suricata rules.
- **change_interface.yml**: Changes the network interface in the Suricata configuration.

## File Structure

```
ansible_projeto1/
├── SAM.py
├── inventory
├── install_suricata.yml
├── read_log.yml
├── ls_ssh_keys.yml
├── add_custom_rule.yml
├── delete_custom_rule.yml
├── view_custom_rules.yml
├── change_interface.yml
└── README.md
```
## [Youtube Video](https://www.youtube.com/watch?v=ho-SKOFaFyw)
## Screenshots

![setup_tab](https://github.com/user-attachments/assets/fd72c495-8c37-4ba6-a3a5-df1e64f03fcf)

![inventory_tab](https://github.com/user-attachments/assets/6f44c25c-1d62-4bed-aa42-5ca497bc65d8)

![install_suricata_tab](https://github.com/user-attachments/assets/6e1eb128-4564-41ea-90d9-5dc2bf04f55e)

![suricata_logs_tab](https://github.com/user-attachments/assets/3bcb0996-a375-4738-8dcd-58994a75bafc)

![custom_rules_tab](https://github.com/user-attachments/assets/67dba868-b89a-4236-9a87-ca4ec306d3b8)

![analyze_logs_tab](https://github.com/user-attachments/assets/5efd0ead-6f5b-4bb9-bc17-b72e6ec8986d)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License

Copyright (c) 2025 Tomás Ferreira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

