import bluetooth
import time

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

data = client_sock.recv(16)
print("Received: ", data)

y = "Hello World!"
print("Sending: ", y)
client_sock.send(y)

x = (2744356319).to_bytes(4,"little")
print("Sending: ", x)
client_sock.send(x)

time.sleep(5)

client_sock.close()
server_sock.close()

print("Closed")