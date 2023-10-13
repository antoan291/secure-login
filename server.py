import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

def handle_connection(c):
    c.send("Username:". encode())
    username = c.recv(1024).decode()
    c.send("Password:". encode())
    password = c.recv(1024).decode()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?" ,(username, hashed_password))
    user_data = cur.fetchone()

    if user_data:
        c.send("Login successful!".encode())
    else:
        c.send("Login failed".encode())

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()