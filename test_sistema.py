import time
import requests

URL_API = "http://127.0.0.1:8000/api/productos/"

print("Iniciando prueba de disponibilidad y rendimiento...")

try:
    inicio = time.time()
    # Se agrega un tiempo límite estricto de 5 segundos (ISO 27002 / Bandit B113)
    respuesta = requests.get(URL_API, timeout=5.0)
    duracion = (time.time() - inicio) * 1000

    print(f"Estado HTTP: {respuesta.status_code}")
    print(f"Tiempo de respuesta: {duracion:.2f} ms")
    print("Prueba finalizada con éxito.")

except requests.exceptions.RequestException as e:
    print(f"Error en la petición: {e}")