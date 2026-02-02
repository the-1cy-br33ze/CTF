from flask import Flask, render_template, request, redirect, make_response, send_file
import sqlite3
import os
import subprocess
import hmac
import hashlib
import base64
import json
from functools import wraps
import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Дебаг
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('CryptoRich')

# Инициализация БД
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                 ("admin", "OJSEHFkjao98u23rnl23", "admin"))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

init_db()

def generate_keys():
    if not os.path.exists('keys/public.pem'):
        os.makedirs('keys', exist_ok=True)
        subprocess.run(['openssl', 'genrsa', '-out', 'keys/private.pem', '2048'], check=True)
        subprocess.run(['openssl', 'rsa', '-in', 'keys/private.pem', '-pubout', '-out', 'keys/public.pem'], check=True)

generate_keys()

def get_pub_key():
    with open('keys/public.pem', 'r') as f:
        return f.read()

def decode_jwt(token):
    try:
        logger.debug(f"Raw token: {token}")
        parts = token.split(".")
        if len(parts) != 3:
            logger.error("Invalid token structure")
            return None
            
        header_b64, payload_b64, signature_b64 = parts
        
        header = json.loads(base64.urlsafe_b64decode(header_b64 + "==").decode())
        alg = header.get("alg")
        logger.debug(f"Algorithm: {alg}")
        
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = base64.urlsafe_b64decode(signature_b64 + "==")
        
        pub_key = get_pub_key()
        
        if alg == "HS256":
            # Уязвимость
            expected_sig = hmac.new(pub_key.encode(), signing_input, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected_sig):
                logger.error("HS256 signature mismatch")
                return None
                
        elif alg == "RS256":
            # RSA
            public_key = load_pem_public_key(pub_key.encode(), backend=default_backend())
            try:
                public_key.verify(
                    signature,
                    signing_input,
                    rsa_padding.PKCS1v15(),
                    hashes.SHA256()
                )
            except Exception as e:
                logger.error(f"RS256 verification failed: {str(e)}")
                return None
        else:
            logger.error(f"Unsupported algorithm: {alg}")
            return None
            
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
        return payload
        
    except Exception as e:
        logger.error(f"JWT decode error: {str(e)}")
        return None

def generate_jwt(username, role):
    header = json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":"))
    payload = json.dumps({"user": username, "role": role}, separators=(",", ":"))
    
    encoded_header = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
    encoded_payload = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    
    with open('keys/private.pem', 'rb') as f:
        private_key = load_pem_private_key(f.read(), password=None, backend=default_backend())
    
    signature = private_key.sign(
        signing_input,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token or not decode_jwt(token):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Пользователь уже существует!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            token = generate_jwt(username, user[3])
            response = make_response(redirect('/dashboard'))
            response.set_cookie('auth_token', token)
            return response
        return "Неверные учетные данные"
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    token = request.cookies.get('auth_token')
    user_data = decode_jwt(token)
    return render_template('dashboard.html', user_data=user_data)

@app.route('/api-docs')
def api_docs():
    return render_template('api_docs.html', pub_key=get_pub_key())

@app.route('/admin')
def admin_panel():
    token = request.cookies.get('auth_token')
    
    if not token:
        logger.error("No token provided")
        return "Требуется авторизация", 401
    
    user_data = decode_jwt(token)
    if not user_data:
        return "Неверный токен", 401
    
    if user_data.get('role') == 'admin':
        return "FLAG: flag{us3_t0k3n$_n0t_l1ke_f00ls}"
    
    return "Доступ запрещен", 403

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('auth_token')
    return response

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)