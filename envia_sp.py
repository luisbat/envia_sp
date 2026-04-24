import socket
import sys

# Configuración
DESTINO_IP = "192.168.1.187"  # CAMBIA ESTA IP POR LA DIRECCIÓN DE DESTINO
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
                texto = data.decode('utf-8')
            except UnicodeDecodeError:
                print(f"Error decodificando datos de {addr}, se omite")
                continue
            
            # Separar en líneas (asumiendo que el texto puede tener múltiples líneas)
            lineas = texto.splitlines()
            for linea in lineas:
                if linea.strip():  # opcional: omitir líneas vacías
                    # Reenviar la línea añadiendo un salto de línea al final
                    send_socket.sendto((linea + '\n').encode('utf-8'), destino)
                    print(f"Reenviado: {linea}")
                else:
                    print(f"Línea vacía recibida de {addr}, ignorada")
                    
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
    finally:
        recv_socket.close()
        send_socket.close()
        print("Sockets cerrados.")

main()
