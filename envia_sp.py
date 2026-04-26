import socket
import sys

# Configuración
DESTINO_IP = "192.168.1.187"  # La IP real será 193.11.166.4
DESTINO_PUERTO = 3021
PUERTO_ESCUCHA = 3020
BUFFER_SIZE = 4096  # Tamaño máximo del datagrama UDP

def main():
    # Crear socket UDP para recibir (broadcast)
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Habilitar opción de broadcast (no necesaria para recibir, pero buena práctica)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Vincular a todas las interfaces en el puerto 3020
    recv_socket.bind(('', PUERTO_ESCUCHA))
    print(f"Escuchando en puerto UDP {PUERTO_ESCUCHA} (broadcast)...")
    
    # Crear socket UDP para reenviar
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # por si se necesita broadcast después
    
    destino = (DESTINO_IP, DESTINO_PUERTO)
    print(f"Reenviando líneas a {DESTINO_IP}:{DESTINO_PUERTO}")
    
    try:
        while True:
            # Recibir datagrama
            data, addr = recv_socket.recvfrom(BUFFER_SIZE)
            
            # Decodificar (asumimos UTF-8)
            try:
                linea = data.decode('utf-8')
            except UnicodeDecodeError:
                print(f"Error decodificando datos de {addr}, se omite")
                continue
            
            if linea.strip():
                partes = linea.split('>')
                id_modem = partes[1].split(';')[2]
                if id_modem == "448":
                    send_socket.sendto((linea + '\n').encode('utf-8'), destino)
#                    print(f"Reenviado desde {addr}: {linea.strip()}")                    
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
    finally:
        recv_socket.close()
        send_socket.close()
        print("Sockets cerrados.")

main()
