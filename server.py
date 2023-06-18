import socket
import threading
import speech_recognition as sr



def handle_client(client_socket, client_address):
    audio_data = b''

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        audio_data += data

    print(audio_data)

def main():
    # Configurar el socket del servidor
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 8000  # Puerto en el que el servidor escuchará las conexiones

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Escuchar hasta 5 conexiones entrantes

    print('El servidor está listo para recibir conexiones.')

    while True:
        # Esperar a que llegue una conexión entrante
        client_socket, client_address = server_socket.accept()

        # Crear un subproceso para manejar la conexión con el cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    main()
