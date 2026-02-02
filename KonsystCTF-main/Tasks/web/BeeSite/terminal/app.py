from flask import Flask, request, jsonify
import subprocess
import urllib.parse
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ALLOWED_COMMANDS = {
    'ls': r'^ls$',  # ТОЛЬКО "ls" без аргументов
    'cat': r'^cat\s+[\w\-\.]+$',  # ТОЛЬКО "cat файл" (без путей)
    'ping': r'^ping\s+([\w\.\-]+)$'  # ТОЛЬКО "ping хост"
}

def is_allowed(cmd):
    cmd = cmd.strip()
    first_word = cmd.split()[0] if cmd else ''
    if first_word not in ALLOWED_COMMANDS:
        return False
    return re.fullmatch(ALLOWED_COMMANDS[first_word], cmd) is not None

def decode_hex_url_encoded(cmd):
    try:
        # Удаляем все % и декодируем как HEX
        hex_str = cmd.replace('%', '')
        decoded = bytes.fromhex(hex_str).decode('utf-8')
        return decoded if is_allowed(decoded) else None
    except:
        return None

def decode_command(cmd):
    # Разрешаем 'ping' в чистом виде
    if cmd.startswith('ping '):
        return cmd if is_allowed(cmd) else None

    # Для ls и cat требуем HEX+URL кодирование
    if cmd.startswith(('%6c%73', '%63%61%74')):
        return decode_hex_url_encoded(cmd)
    
    return None

@app.route("/exec", methods=["GET"])
def exec_command():
    encoded_cmd = request.args.get("cmd", "")
    decoded_cmd = decode_command(encoded_cmd)

    if not decoded_cmd:
        return jsonify({"error": "Invalid or unauthorized command"}), 403

    try:
        result = subprocess.run(
            decoded_cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        if result.returncode == 0:
            return jsonify({"output": result.stdout.decode('utf-8')})
        else:
            return jsonify({"error": result.stderr.decode('utf-8')})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5454)
