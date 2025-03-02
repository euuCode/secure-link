import random
import string
import time
import os
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

app = Flask(__name__)
active_links = {}
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/link/<link_id>', methods=['GET', 'POST'])
def access_link(link_id):
    if link_id not in active_links:
        return jsonify({"error": "Link inválido ou expirado"}), 404
    
    link_data = active_links[link_id]
    if datetime.now() > link_data["expiration"]:
        del active_links[link_id]
        return jsonify({"error": "Link expirado"}), 404
    
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin != link_data["pin"]:
            return jsonify({"error": "PIN incorreto"}), 401
        decrypted_content = cipher_suite.decrypt(link_data["content"]).decode() if isinstance(link_data["content"], bytes) else link_data["content"]
        return jsonify({"success": True, "content": decrypted_content})
    return '''
    <html><body style="background-color: #0F1419; color: #E5E7EB; font-family: Inter;">
        <h1 style="color: #10B981;">SecureLink - Acesso Seguro</h1>
        <form method="POST">
            <label style="color: #E5E7EB;" for="pin">Digite o PIN (4 dígitos):</label><br>
            <input type="password" id="pin" name="pin" maxlength="4" style="background-color: #1F2A37; color: #E5E7EB; border: 2px solid #10B981; border-radius: 15px; padding: 10px;" required><br><br>
            <button type="submit" style="background-color: #10B981; color: #E5E7EB; border-radius: 15px; padding: 10px 20px; box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);">Acessar</button>
        </form>
    </body></html>
    '''

@app.route('/create_link', methods=['POST'])
def create_link():
    data = request.get_json()
    message = data['message']
    pin = data['pin']
    expiration = int(data['expiration'])

    if not message or not pin or not pin.isdigit() or len(pin) != 4:
        return jsonify({"error": "Mensagem/arquivo e PIN de 4 dígitos são obrigatórios!"}), 400

    link_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    timestamp = datetime.now() + timedelta(minutes=expiration)
    encrypted_content = cipher_suite.encrypt(message.encode() if isinstance(message, str) else message)

    active_links[link_id] = {
        "content": encrypted_content,
        "pin": pin,
        "expiration": timestamp,
        "key": key,
        "original": message
    }

    link = f"http://127.0.0.1:8000/link/{link_id}"
    save_log(link, timestamp, pin)
    return jsonify({"link": link, "expiration": timestamp.strftime("%Y-%m-%d %H:%M:%S"), "pin": pin})

def save_log(link, expiration, pin):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": link,
        "expiration": expiration.strftime("%Y-%m-%d %H:%M:%S"),
        "pin": pin,
        "status": "Ativo"
    }
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "securelink_logs.json")
    logs = []
    if os.path.exists(desktop_path):
        with open(desktop_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append(log)
    with open(desktop_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

def generate_pdf():
    if not active_links:
        return {"error": "Nenhum link ativo para gerar relatório!"}, 400

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "securelink_report.pdf")
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        doc = SimpleDocTemplate(desktop_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("<font size=20><b>Relatório SecureLink</b></font>", styles["Title"]))
        elements.append(Spacer(1, 20))

        for link_id, data in active_links.items():
            elements.append(Paragraph(f"<font size=16><b>Link: http://127.0.0.1:8000/link/{link_id}</b></font>", styles["Heading2"]))
            elements.append(Paragraph(f"Conteúdo Original: {data['original']}", styles["Normal"]))
            elements.append(Paragraph(f"PIN: {data['pin']}", styles["Normal"]))
            elements.append(Paragraph(f"Expiração: {data['expiration'].strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
            elements.append(Spacer(1, 10))

        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<font size=12><i>Gerado por SecureLink - by euuCode</i></font>", styles["Italic"]))
        
        doc.build(elements)
        return {"success": f"Relatório salvo em PDF: {desktop_path}"}, 200
    except Exception as e:
        return {"error": f"Erro ao gerar PDF: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)