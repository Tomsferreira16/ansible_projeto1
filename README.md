# Suricata & Ansible Management

This project provides a graphical interface (GUI) for managing Suricata and Ansible configurations. Built using Python's Tkinter library, the application integrates with Ansible playbooks to automate key tasks such as Suricata installation, inventory management, log monitoring, and custom rule handling. The project was developed as part of a university assignment for the Networks and Systems Administration course at Instituto Politécnico de Viana do Castelo. It was supervised by Assistant Guest Prof. Silvestre Malta under the subject "Projeto 1."

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Ansible Playbooks](#ansible-playbooks)
- [File Structure](#file-structure)
- [Youtube Video](#Youtube-video)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Inventory Management**: Add, load, and delete servers from the inventory.
- **Install Suricata**: Install and configure Suricata on remote servers.
- **View Suricata Logs**: View Suricata fast logs.
- **Custom Rules Management**: Add, view, and delete custom Suricata rules.
- **Analyze Fast Logs**: Load, filter and export the Suricata file fast.log by IP, date, and protocol.
- **Analyze JSON Logs**: Load, filter and export the Suricata file eve.json by IP, date, and protocol.

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
**⚠️ Warning:** Don't run the application in the background, or else some functions will not work!

1. Run the application:
    ```sh
    chmod +x SAM.py
    ./SAM.py
    ```

2. Use the GUI to manage your Suricata and Ansible configurations:
    - **Setup Tab**: Generate and copy SSH keys to remote servers, and manage SSH identities.
    - **Inventory Tab**: Add, load, and delete servers.
    - **Install Suricata Tab**: Install Suricata on remote servers.
    - **Suricata Logs Tab**: View and export Suricata logs.
    - **Custom Rules Tab**: Add, view, and delete custom Suricata rules.
    - **Analyze Fast Logs Tab**: Load and filter log files.
    - **Analyze JSON Logs Tab**: Load and filter JSON log files.

## Ansible Playbooks

The following playbooks are included in the project:

- **install_suricata.yml**: Installs and configures Suricata.
- **read_log.yml**: Reads the Suricata `fast.log` file.
- **ls_ssh_keys.yml**: Lists SSH keys on remote servers.
- **add_custom_rule.yml**: Adds a custom Suricata rule.
- **delete_custom_rule.yml**: Deletes a custom Suricata rule.
- **view_custom_rules.yml**: Views custom Suricata rules.
- **change_interface.yml**: Changes the network interface in the Suricata configuration.
- **get_fast_log.yml**: Fetches the Suricata `fast.log` file.
- **get_eve_json.yml**: Fetches the Suricata `eve.json` file.

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
├── get_fast_log.yml
├── get_eve_json.yml
└── README.md
```
## [Youtube Video](https://www.youtube.com/watch?v=ho-SKOFaFyw)

## Screenshots

![setup_tab](https://github.com/user-attachments/assets/1285500f-c7c6-4c5c-ae58-ba2cf54d8e4a)


![inventory_tab](https://github.com/user-attachments/assets/9702c8e9-f7c4-4d34-90ea-465d77f9f07e)


![install_suricata_tab](https://github.com/user-attachments/assets/a931175c-15c3-4623-b2fc-e4f3b14831f3)


![suricata_logs_tab](https://github.com/user-attachments/assets/e81a950d-1157-4199-bded-97a9e8e471f2)


![custom_rules_tab](https://github.com/user-attachments/assets/1b13c2dd-f831-4bbf-b9b5-6bde6c0e45e3)


![analyze_fast_logs_tab](https://github.com/user-attachments/assets/6aadb667-2bf0-47a5-b8f7-51e93b250fad)



![analyze_json_logs_Tab](https://github.com/user-attachments/assets/df99dc3a-dd24-4d11-aacc-016a23fd4715)



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

