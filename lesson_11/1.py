import socket

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8082))
s.listen()

print("Started server on 8080 port...")

conn, addr = s.accept()
print(f"Connection from {addr}")

data = conn.recv(1024)
print(f"Received: {data.decode()}")

conn.close()
s.close()
