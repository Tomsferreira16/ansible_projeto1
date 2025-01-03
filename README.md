# Suricata & Ansible Management

This project provides a graphical user interface (GUI) for managing Suricata and Ansible configurations. The application is built using Python's Tkinter library and integrates with Ansible playbooks to perform various tasks such as installing Suricata, managing inventory, viewing logs, and handling custom rules.

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
- **View Suricata Logs**: View and export Suricata logs.
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
    python SAM.py
    ```

2. Use the GUI to manage your Suricata and Ansible configurations:
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

## Screenshots

Include screenshots of your application here to give users a visual overview of the GUI.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License

Copyright (c) 2023 Tomás Ferreira

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

