
# Based on http://pages.iu.edu/~rwisman/c490/html/pythonandbluetooth.htm

from bluetooth import *

services = find_service(name="BasuraPiBluetoothServer",
                        uuid="7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d")

for i in range(len(services)):
    match = services[i]

    if match["name"] == "BasuraPiBluetoothServer":
        port = match["port"]
        name = match["name"]
        host = match["host"]

        print(name, port, host)

        client_sock = BluetoothSocket(RFCOMM)
        client_sock.connect((host, port))

        # Get list of possible operations
        client_sock.send("op:getOperations")

        # Read the data sent by the server
        data = client_sock.recv(1024)
        data = data.decode('UTF-8')

        if len(data) == 0:
            break
        print("Received [%s]" % data)

        client_sock.close()
        break

