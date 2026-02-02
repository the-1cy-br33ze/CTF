from flask import Flask, render_template, Response
from flask_sock import Sock
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto import Random
import base64
import random
import hashlib
import time

app = Flask(__name__)
sock = Sock(app)

FLAG = "flag{Th3_M4tr1x_H4s_Y0u}"
KEY = hashlib.sha256(b'matrix_architect_1337').digest()[:16]

def encrypt(text):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(pad(text.encode(), AES.block_size))).decode('latin-1')

parts = [encrypt(FLAG[i:i+5]) for i in range(0, len(FLAG), 5)]
random.shuffle(parts)

@app.route('/sys/err_log')
def key_leak():
    return Response(
        "ERR#4582: CORE DUMP\n"
        "FRAGMENT_KEY: " + base64.b64encode(KEY).decode(),
        mimetype='text/plain'
    )

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/data_stream')
def ws(conn):
    for part in parts:
        conn.send(part)
        time.sleep(30)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
