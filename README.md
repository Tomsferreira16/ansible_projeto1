# ansible_projeto1

setup tab	
	-generate ssh key	
	-add the key_name.pub to the where we install suricata
	-eval $(ssh-agent)
	-ssh-add ~/.ssh/key_name(private)
	-alias ssha='eval $(ssh-agent) && ssh-add'

inventory tab
	-you can a new server (ip, user, password)
	-Load the inventory file (cat)
	-delete server (by selecting with the mouse)

install suricata
	-input the interface that suricata is using

suricata logs
	-view the /var/log/suricata/fast.log

custom rules tab
	-add custom rule
		action, protocol, source ip, source port, dest ip, dest port ,message, sid
	-view custom rules (/etc/suricata/rules/custom.rules)
