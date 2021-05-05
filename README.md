# Reverse Backdoor

This repository includes a victim end backdoor script and a listener script for the server. On executing the backdoor script on the victim's machine, it forms a reverse connection to the server providing a shell prompt to the victim's machine.

## Scripts

### server_listener.py
This script needs to be run on the server as;
> python3 listener/server_listener.py --ip-address *\<Server IP>* --port *\<Port>*

The listener listens for any clients requesting connection (requested by the backdoor on the victim's end). Once the connection is established, the script opens a shell prompt on the victim machine. The shell prompt is able to execute most commands including two additional commands; *rb_download* and *rb_upload* to download files from the victim's machine and upload files to the victim's machine respectively. The command can be used as;
> \\> rb_upload *\<filename>*

Or
> \\> rb_download *\<filename>*

### reverse_backdoor.py
This script needs to be run in the victims machine. It is imperative that the victim's machine have python installed in it. If not, then this script needs to be packaged as an executable. (The steps to package the file can be read in *Packaging.md*)
Before packaging the backdoor, edit the *backdoor_ip* and *backdoor_port* variable in *main* function in the script. Also change the name of the cover file in the script. The backdoor also ensures persistence after restart.