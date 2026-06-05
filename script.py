import os
import subprocess
import sys
from flask import Flask, send_file, request
from colorama import Fore, Style, init

init(autoreset=True) # biar warna auto reset kayak chalk

app = Flask(__name__)
port = 5000
nombre_imagen = "carajoputa.png" # El nombre del archivo donde está la imagen.! Ponerlo con extensión.

# Banner ASCII
banner = f"""{Fore.MAGENTA}

     ██▓ ███▄ ▄███▓ ▄▄▄ ▄████ ▓█████ ██▓ ██▓███ ██▓ ▒█████ ▄████ ▄████ ▓█████ ██▀███
    ▓██▒▓██▒▀█▀ ██▒████▄ ██▒ ▀█▒▓█ ▀ ▓██▒▓██░ ██▒ ▓██▒ ▒██▒ ██▒ ██▒ ▀█▒ ██▒ ▀█▒▓█ ▀ ▓██ ▒ ██▒
    ▒██▒▓██ ▓██░▒██ ▀█▄ ▒██░▄▄▄░▒███ ▒██▒▓██░ ██▓▒ ▒██░ ▒██░ ██▒██░▄▄▄░▒██░▄▄▄░▒███ ▓██ ░▄█ ▒
    ░██░▒██ ▒██ ░██▄▄██ ░▓█ ██▓▒▓█ ▄ ░██░▒██▄█▓▒ ▒ ▒██░ ▒██ ██░░▓█ ██▓░▓█ ██▓▒▓█ ▄ ▒██▀▀█▄
    ░██░▒██▒ ░██▒ ▓█ ▓██▒░▒▓███▀▒░▒████▒ ░██░▒██▒ ░ ░ ░██████▒░ ████▓▒░░▒▓███▀▒░▒▓███▀▒░▒████▒░██▓ ▒██▒
    ░▓ ░ ▒░ ░ ░ ▒▒ ▓▒█░ ░▒ ▒ ░░ ▒░ ░ ░▓ ▒▓▒░ ░ ░ ░ ▒░▓ ░░ ▒░▒░▒░ ░▒ ▒ ░▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
     ▒ ░░ ░ ░ ▒ ▒▒ ░ ░ ░ ░ ░ ▒ ░░▒ ░ ░ ▒ ░ ░ ▒░ ░ ░ ░ ░ ░ ░ ░▒ ░ ▒░
     ▒ ░░ ░ ░ ▒ ░ ░ ░ ▒ ░░░ ░ ░ ▒ ░ ░ ░ ░ ░░ ░
     ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░

    ~ by ZenX$Team - {Fore.WHITE}.gg/kEB3PCPkzc{Fore.MAGENTA}
    {Style.RESET_ALL}"""

def conectar_serveo():
    """Buka tunnel SSH ke serveo.net kayak di Node.js"""
    cmd = f"ssh -o StrictHostKeyChecking=no -R {port}:localhost:{port} serveo.net"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in proc.stdout:
        line = line.strip()
        if line.startswith('HTTP request from'):
            continue
        if 'Forwarding HTTP traffic from' in line:
            b = line.replace("Forwarding HTTP traffic from ", "").strip()
            print(f"{Fore.CYAN}[$] Host: {Fore.WHITE}{b}")
            print(f"{Fore.CYAN}[$] Image: {Fore.WHITE}/{nombre_imagen}")

@app.route(f'/{nombre_imagen}')
def serve_image():
    # Log mirip Node.js: IP + User-Agent
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    print(f"{Fore.MAGENTA}[$] Víctima: {ip} - {ua}{Style.RESET_ALL}")

    if os.path.exists(nombre_imagen):
        return send_file(nombre_imagen, mimetype='image/png')
    return f"File {nombre_imagen} tidak ditemukan", 404

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear') # console.clear()
    print(banner)
    print(f"{Fore.CYAN}[i] Se abrió el servidor en el puerto: {port}{Style.RESET_ALL}")

    # Jalanin serveo di thread biar gak ngeblock Flask
    import threading
    threading.Thread(target=conectar_serveo, daemon=True).start()

    app.run(host='0.0.0.0', port=port)
