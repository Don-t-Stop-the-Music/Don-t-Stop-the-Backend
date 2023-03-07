"""
Bluetooth process
sets up bluetooth connection and sends data asyncronously
"""
import sys
import json
from time import sleep
import subprocess
from multiprocessing import Queue
from queue import Empty

import bluetooth


INITIAL_CACHE = {"frequency": [[59,75,63], [27,89,32]], "minFrequency": 0, "maxFrequency": 80,
                  "hiss": [False, False], "feedback": [[], []]} #
#All data fields are named before the cache is serialized and sent for the first time
#This prevents the client from attempting to parse fields that do not exist
#Although the data may be bogus


def open_server():
    """
    Open
    Listen on port 1 and advertise bluetooth service
    """

    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    print("listening on port:", bluetooth.PORT_ANY)

    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848" 
    #uuid common between client and server, used by the client to find the server easily

    bluetooth.advertise_service(
        server_sock,
        "raspberrypi",
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    ) #set up attributes of the bluetooth service 

    return server_sock

def connect(server_sock):
    """
    Connect
    Make pi discoverable and await connection
    """

    discoverable()
    #bluetooth device must be 'discoverable' for the client to find the server

    client_sock, address = server_sock.accept() #blocks until a connection is accepted
    print("Accepted connection from ", address)

    return client_sock


def transmit(data_stream, client_sock):
    """
    Transmit
    consumes items from data_stream, serialize and send them to the client socket
    """

    cache = INITIAL_CACHE
    #initilize cache so we don't ever send an unititilized cache

    while True:
        item = data_stream.get() #blocks until some/any items are available
        try:
            while True:
                cache[item[0]] = item[1]
                item = data_stream.get_nowait()
                #iterates through all currently available items updating the cache
        except Empty:
            #when out of currently available items
            print("socket response:", client_sock.send("\0" + json.dumps(cache) + "\0"))
            #serialize cache and send to client

def disconnect(client_sock, server_sock):
    """
    Disconnect
    closes the client and server sockets
    """

    client_sock.close()
    server_sock.close()

    print("Connection closed")

def discoverable():
    """
    Discoverable
    makes the pi discoverable
    """
    sleep(0.1)
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    #run the console command to make pi discoverable for 60 seconds
    sleep(0.1)

def bluetooth_proc(data_stream: Queue):
    """
    bluetooth_proc
    acts as an entry point for bluetoothConnection reset by peer
    """

    server_sock = open_server()
    #open and set up the server

    while True:

        client_sock = connect(server_sock)
        #wait for a connection

        try:

            transmit(data_stream, client_sock)
            #transmit data

        except bluetooth.btcommon.BluetoothError as bluetooth_error:
            #catch "connection reset" and "endpoint not connected" and restart connection

            if bluetooth_error.errno == 104:
                print("Connection reset by peer")
            elif bluetooth_error.errno == 107:
                print("Transport endpoint is not connected")
            else:
                raise bluetooth_error
            
        except KeyboardInterrupt:
            #catch keyboard interrupt and close connection (and close program)
            disconnect(client_sock, server_sock)
            sys.exit(0)
