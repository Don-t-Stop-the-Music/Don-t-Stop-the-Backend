import threading
import bluetooth
import json


class ConnectionService(threading.Thread):

    def connect(self):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        server_sock.bind(("",bluetooth.PORT_ANY))
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

        client_sock,address = server_sock.accept()
        print("Accepted connection from ",address)

        self.client_sock = client_sock
        self.server_sock = server_sock

    def transmit(self): 

        while(True):

            item = self.queue.get()

            if item is None:
                break

            self.cache_add(item)
            self.client_sock.send(json.dumps(self.cache))


    def cache_add(self, item):
        self.cache[item.tag] = item.body


    def join(self):

        self.client_sock.close()
        self.server_sock.close()

        print("Closed")
        super.join()

    def run(self, data_stream):

        self.queue = data_stream

        self.connect()
        self.transmit()
        self.join()


    