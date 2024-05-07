import socket
import threading
import time
import requests
import random

HOST = "10.42.0.1"
PORT = 8888
MAX_CONNECTIONS = 5
BUFFER_SIZE = 1024
TIMEOUT = 5
connected_devices = {}


def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    connected_devices[address[0]] = time.time()  # Initialize last message time

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            if address == "10.42.0.26":
                try:
                    response = requests.post(
                        "http://localhost:3000/api/array",
                        json={"string": "Cow 2 Connected"},
                    )
                    if response.status_code == 201:
                        print("Connected cow 2 request successful")
                    else:
                        print(
                            f"POST request failed with status code {response.status_code}"
                        )
                except Exception as e:
                    print(f"Error making POST request: {e}")
                print("Cow 2 Connected")
            else:
                try:
                    response = requests.post(
                        "http://localhost:3000/api/array",
                        json={"string": "Cow 1 Connected"},
                    )
                    if response.status_code == 201:
                        print("Connected cow 1 request successful")
                    else:
                        print(
                            f"POST request failed with status code {response.status_code}"
                        )
                except Exception as e:
                    print(f"Error making POST request: {e}")
                print("Cow 1 Connected")
            connected_devices[address[0]] = time.time()  # Update last message time
        except ConnectionResetError:
            break

    print(f"Device {address} disconnected")
    del connected_devices[address[0]]
    client_socket.close()


def accept_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)
        print(f"Listening for connections on {HOST}:{PORT}")

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, address)
            )
            client_thread.start()


def check_disconnected_devices():
    while True:
        disconnected_devices = []
        current_time = time.time()
        for device, last_message_time in connected_devices.items():
            if current_time - last_message_time > TIMEOUT:
                disconnected_devices.append(device)
            if device == "10.42.0.26":
                try:
                    response = requests.post(
                        "http://localhost:3000/api/array",
                        json={"string": "Absent of Cow 2"},
                    )
                    if response.status_code == 201:
                        print("Absent cow 2 request successful")
                    else:
                        print(
                            f"POST request failed with status code {response.status_code}"
                        )
                except Exception as e:
                    print(f"Error making POST request: {e}")
                print("Absent of Cow 2")
            else:
                try:
                    response = requests.post(
                        "http://localhost:3000/api/array",
                        json={"string": "Absent of Cow 1"},
                    )
                    if response.status_code == 201:
                        print("Absent cow 1 request successful")
                    else:
                        print(
                            f"POST request failed with status code {response.status_code}"
                        )
                except Exception as e:
                    print(f"Error making POST request: {e}")
                print("Absent of Cow 1")
        # this for loop not running
        for device in disconnected_devices:
            print(f"Device {device} disconnected")
            del connected_devices[device]
            # Make a POST request to the API endpoint
        try:
            print("dsdsd")
            response = requests.post(
                "http://localhost:3000/api/post",
                json={"count": len(connected_devices)},
            )
            if response.status_code == 201:
                print("POST request successful")
            else:
                print(f"POST request failed with status code {response.status_code}")
        except Exception as e:
            print(f"Error making POST request: {e}")
        print(f"Total connected devices: {len(connected_devices)}")
        time.sleep(3)


# Start the server
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Start the thread to check for disconnected devices
check_thread = threading.Thread(target=check_disconnected_devices)
check_thread.start()
