FROM python:3.12.12-slim

# Copiar el script (ajusta la ruta)
COPY envia_sp.py /app/envia_sp.py

# Crear directorio para logs (opcional, usar stdout sería mejor)
RUN mkdir -p /var/log && chmod 777 /var/log || true

WORKDIR /app

# No usar CMD con --stop, el contenedor debe ejecutar el daemon en foreground
# Pero nuestro script usa daemon.DaemonContext que ya se desprende del terminal.
# Para contenedores, mejor evitar doble fork. Modificaremos ligeramente.

# Por simplicidad, modifica el script para que NO haga daemonización dentro del contenedor.
# Explico el cambio abajo.

CMD ["python", "-u", "envia_sp.py"]
