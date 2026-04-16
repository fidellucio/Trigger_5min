from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados
WORKFLOWS = [
    {"repo": "QueueListLog", "workflow": "queuelistsp5.yaml"},
    {"repo": "Base-Pending", "workflow": "main_expedicao.yaml"},
    {"repo": "Base-Handeover", "workflow": "main_expedicao.yaml"},
    {"repo": "Base_3PL", "workflow": "main_expedicao.yaml"},
    {"repo": "base_transporting", "workflow": "main_base_to_Transporting.yaml"},
    {"repo": "Queuelist", "workflow" : "queue_list_sp5.yml"},
    {"repo": "base_inbound", "workflow" : "main_inbound.yaml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        url = f"https://api.github.com/repos/Murilosantana7/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
