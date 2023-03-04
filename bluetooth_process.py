"""
Bluetooth process
sets up bluetooth connection and sends data asyncronously
"""
import json
from time import sleep
import subprocess
from multiprocessing import Queue
# pylint: disable-next=import-error
import bluetooth


INITIAL_CACHE = {"frequency": [[59,75,63], [27,89,32]], "minFrequency": 0, "maxFrequency": 80, "hiss": [False, False], "feedback": [[], []]}


def open():
    """
    Open
    Listen on port 1 and advertise bluetooth service
    """
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    print("listening on port:", bluetooth.PORT_ANY)

    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"

    bluetooth.advertise_service(
        server_sock,
        "raspberrypi",
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
        # protocols=[bluetooth.OBEX_UUID]
    )

    return server_sock

def connect(server_sock):
    """
    Connect
    Make pi discoverable and await connection
    """

    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    sleep(0.1)

    client_sock, address = server_sock.accept()
    print("Accepted connection from ", address)

    return client_sock


def transmit(data_stream, client_sock):
    """
    Transmit
    consumes items from data_stream, serialize and send them to the client socket
    """

    cache = INITIAL_CACHE

    while True:

        item = data_stream.get()

        if item is None:
            break

        cache[item[0]] = item[1]
        print("socket response:", client_sock.send("\0" + json.dumps(cache) + "\0"))

def disconnect(client_sock, server_sock):
    """
    Disconnect
    closes the client and server sockets
    """

    client_sock.close()
    server_sock.close()

    print("Closed")


def bluetooth_proc(data_stream: Queue):
    """
    bluetooth_proc
    acts as an entry point for bluetoothConnection reset by peer
    """
    
    server_sock = open()

    while True:

        client_sock = connect(server_sock)

        try:

            transmit(data_stream, client_sock)
            disconnect(client_sock, server_sock)

        except bluetooth.btcommon.BluetoothError as e:

            if e.errno == 104:
                print("Connection reset by peer")
            else:
                raise e
    
    
    
