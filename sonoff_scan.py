import os
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)

# Configurações de sessão e chave secreta
app.secret_key = os.urandom(24)  # Chave secreta para gerir a sessão

# Determina a pasta onde o script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "sonoff.db")  # Base de dados na mesma pasta da aplicação

# Credenciais de login do .env
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Função para criar a base de dados caso não exista
def create_db():
    if not os.path.exists(DB_FILE):
        print("[DB] A criar a nova base de dados...") #para debug
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE sonoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT UNIQUE NOT NULL,
                mac TEXT NOT NULL,
                name TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()
        print("[DB] Base de dados criada com sucesso.")
    else:
        print("[DB] Base de dados já existe.")

# Função para fazer scan da rede e encontrar Sonoffs
def scan_network():
    devices = []
    print("[SCAN] A INICIAR o scan da rede...") #para debug
    #ajusta o comando nmap para scan da rede local
    #result = os.popen("nmap -sn 192.168.6.1-50 | grep report").read()  # Limita a pesquisa aos primeiros 50 IPs
    result = os.popen("nmap -sn 192.168.6.0/24 | grep report").read()  # Ajusta para pesquisa total da rede
    lines = result.split("\n")
    print(f"[SCAN] Resultados do Nmap: {len(lines)} resultados encontrados.")

    for line in lines:
        if "Nmap scan report" in line:
            ip = line.split(" ")[-1]
            print(f"[SCAN] A verificar IP: {ip}")
            mac = get_mac_address(ip)
            print(f"[SCAN] MAC obtido: {mac}")
            if mac and test_sonoff(ip):
                print(f"[SCAN] Sonoff detectado: {ip} ({mac})")
                devices.append((ip, mac))
            else:
                print(f"[SCAN] {ip} não é um Sonoff ou não respondeu.")
    print(f"[SCAN] Total de dispositivos encontrados: {len(devices)}")
    return devices

# Obtém o MAC Address de um IP
def get_mac_address(ip):
    url = f"http://{ip}/cm?cmnd=Status%200"
    print(f"[HTTP] A obter MAC para IP: {ip} através de {url}")
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        mac = data.get("StatusNET", {}).get("Mac")
        if mac:
            return mac
        else:
            print(f"[HTTP] Campo 'Mac' não encontrado em 'StatusNET' para IP {ip}")
    
    except requests.exceptions.RequestException as e:
        print(f"[HTTP] Erro ao obter MAC para IP {ip}: {e}")
    
    return None

# Testa se um IP pertence a um Sonoff com Tasmota
def test_sonoff(ip):
    print(f"[TEST] A testar se {ip} é um Sonoff...")
    try:
        response = requests.get(f"http://{ip}/cm?cmnd=Status%200", timeout=1)
        data = response.json()
        if "Status" in data:
            print(f"[TEST] {ip} confirmou como Sonoff.")
            return True
        else:
            print(f"[TEST] {ip} respondeu mas não é um Sonoff.")
            return False
    except Exception as e:
        print(f"[TEST] Erro ao contactar {ip}: {e}")
        return False

# Verifica o status atual do Sonoff (Ligado/Desligado)
def get_sonoff_status(ip):
    print(f"[STATUS] A verificar o status de {ip}")
    try:
        response = requests.get(f"http://{ip}/cm?cmnd=Power", timeout=1)
        data = response.json()
        return data.get("POWER", "OFF") == "ON"
    except Exception as e:
        print(f"[STATUS] Erro ao obter o status de {ip}: {e}")
        return None

# Guarda ou atualiza o Sonoff na base de dados
def save_sonoff(ip, mac, name="Sonoff"):
    print(f"[DB] A gravar/atualizar dispositivo: {ip} ({mac})")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sonoffs (ip, mac, name) VALUES (?, ?, ?)
        ON CONFLICT(ip) DO UPDATE SET mac = ?, name = ?""",
        (ip, mac, name, mac, name)
    )
    conn.commit()
    conn.close()
    print(f"[DB] Dispositivo gravado com sucesso.")

# Pesquisa todos os Sonoffs guardados
#def get_sonoffs():
#    print("[DB] Pesquisa de dispositivos na base de dados...")
#    conn = sqlite3.connect(DB_FILE)
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM sonoffs")
#    devices = cursor.fetchall()
#   conn.close()
#    print(f"[DB] {len(devices)} dispositivos encontrados.")
#   return [{"id": d[0], "ip": d[1], "mac": d[2], "name": d[3], "status": get_sonoff_status(d[1])} for d in devices]

def get_sonoffs():
    print("[DB] Pesquisa de dispositivos na base de dados...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sonoffs")
    devices = cursor.fetchall()
    conn.close()
    print(f"[DB] {len(devices)} dispositivos encontrados.")
    return [
        {
            "id": d[0],
            "ip": d[1],
            "mac": d[2],
            "name": d[3],
            "status": get_sonoff_status(d[1]),
            "blocked": is_ip_blocked(d[1])
        }
        for d in devices
    ]

# Função para verificar se o utilziador está autenticado
def is_authenticated():
    return session.get('logged_in', False)

# Função para bloquear um IP
def block_ip(ip):
    try:
        # Comando iptables para bloquear o IP
        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
        print(f"[IPTABLES] IP {ip} bloqueado com sucesso.")
    except Exception as e:
        print(f"[IPTABLES] Erro ao bloquear IP {ip}: {e}")

# Função para desbloquear um IP
def unblock_ip(ip):
    try:
        # Comando iptables para desbloquear o IP
        os.system(f"sudo iptables -D INPUT -s {ip} -j DROP")
        print(f"[IPTABLES] IP {ip} desbloqueado com sucesso.")
    except Exception as e:
        print(f"[IPTABLES] Erro ao desbloquear IP {ip}: {e}")

# Verifica se o IP está bloqueado no iptables
def is_ip_blocked(ip):
    try:
        result = os.popen(f"sudo iptables -L INPUT -v -n | grep {ip}").read()
        return "DROP" in result
    except Exception as e:
        print(f"[IPTABLES] Erro ao verificar se IP está bloqueado: {e}")
        return False

# Página de Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return "Credenciais incorretas", 401
    return render_template("login.html")

# Página de administração (somente autenticada)
@app.route("/admin")
def admin():
    if not is_authenticated():
        return redirect(url_for("login"))  # Redireciona para o login se não estiver autenticado
    return render_template("admin.html", devices=get_sonoffs())

# Rota da interface web (Página principal)
@app.route("/")
def index():
    print("[ROTA] / -> Página principal")
    return render_template("index.html", devices=get_sonoffs())

# API para fazer scan de rede e guardar dispositivos
@app.route("/scan")
def scan():
    print("[ROTA] /scan -> A iniciar scan via web")
    found_devices = scan_network()
    for ip, mac in found_devices:
        save_sonoff(ip, mac)
    return jsonify({"success": True, "devices": get_sonoffs()})

# API para renomear um dispositivo
@app.route("/rename", methods=["POST"])
def rename():
    data = request.json
    print(f"[ROTA] /rename -> {data}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE sonoffs SET name = ? WHERE ip = ?", (data["name"], data["ip"]))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# API para ligar/desligar Sonoff
@app.route("/toggle", methods=["POST"])
def toggle():
    data = request.json
    ip, state = data["ip"], data["state"]
    cmd = "On" if state else "Off"
    print(f"[ROTA] /toggle -> A enviar '{cmd}' para {ip}")
    try:
        requests.get(f"http://{ip}/cm?cmnd=Power%20{cmd}")
        return jsonify({"success": True})
    except Exception as e:
        print(f"[ROTA] /toggle -> Erro ao enviar comando: {e}")
        return jsonify({"success": False}), 500
    
# Rota para bloquear IP
@app.route('/block_ip', methods=['GET'])
def block_ip_route():
    ip = request.args.get('ip')
    if ip:
        block_ip(ip)  # Bloqueia o IP
        return jsonify({"success": True, "message": f"IP {ip} bloqueado com sucesso!"})
    else:
        return jsonify({"success": False, "message": "IP não fornecido!"}), 400

# Rota para desbloquear IP
@app.route('/unblock_ip', methods=['GET'])
def unblock_ip_route():
    ip = request.args.get('ip')
    if ip:
        unblock_ip(ip)  # Desbloqueia o IP
        return jsonify({"success": True, "message": f"IP {ip} desbloqueado com sucesso!"})
    else:
        return jsonify({"success": False, "message": "IP não fornecido!"}), 400

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    print("[APP] A iniciar a aplicação...")
    create_db()  # Cria a base de dados se não existir
    app.run(host="0.0.0.0", port=7500, debug=True)
    #print("[APP] A correr em http://0.0.0.0:7500")