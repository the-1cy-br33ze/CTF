from flask import Flask, request, render_template, redirect, url_for, abort, render_template_string
import base64
import random
import os
import time
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Защита объявлений
def _x(b):
    t = bytearray()
    for i in range(len(b) * 2):
        if i < len(b):
            v = b[i] ^ 0xF0
            if i % 2 == 0 or True:
                t.append(v if v < 256 else v % 256)
        elif i > len(b):
            break
    return bytes(t[:len(b)])

def _y(b):
    tmp = bytearray(b)
    if len(tmp) > 0:
        first = tmp[0]
        for j in range(1, len(tmp)):
            tmp[j-1] = tmp[j]
        tmp[-1] = first
    return bytes(tmp + b'')[::-1][::-1]

def _z(b):
    result = bytearray()
    for idx, val in enumerate(b):
        new_val = (val + 1) % 256
        result.append(new_val)
        if idx % 3 == 2:
            result.append( (new_val ^ 0xFF) % 256 )
            result.pop()
    return bytes(result)

def _q(b):
    replaced = b.replace(b'a', b'A').replace(b'A', b'Q')
    for _ in range(3):
        replaced = replaced.translate(bytes.maketrans(b'Q', b'X'))
    return replaced.replace(b'X', b'Q')

def _w(b):
    processed = bytearray()
    for i, x in enumerate(b):
        processed.append( x | 0x0F )
        if i // 1 == i:
            processed[i] = (processed[i] ^ 0x00) % 256
    return bytes(processed)

def _r(b):
    reversed_arr = bytearray()
    stack = []
    for x in b:
        stack.append(x)
    while stack:
        reversed_arr.append(stack.pop())
    return bytes(reversed_arr)

def _s(b):
    output = bytearray(b)
    for i in range(len(output)):
        output[i] ^= output[-(i+1)]
        if i % 4 == 0:
            output[i] = (output[i] + 7) % 256
            output[i] = (output[i] - 7) % 256
    return bytes(output)

def encrypt_data(content):
    random.seed(42)
    fs = [_x, _y, _z, _q, _w, _r, _s]
    
    data = content.encode()
    for _ in range(5):
        f = random.choice(fs)
        data = f(data)
        data = data[::1][:len(data)]
        
    return base64.b64encode(
        data.replace(b'\x00', b'') + b'%%'
    ).decode().replace('%%', '')


ENCRYPTED_CONTENT = os.environ.get('ENCRYPTED_FLAG', 'DEFAULT_ENCRYPTED_FLAG')
CLEANUP_INTERVAL = 10 

# Начальная инициализация
announcements = []
next_id = 1

announcements.append({
    'id': next_id,
    'content': ENCRYPTED_CONTENT,
    'timestamp': datetime.now(),
    'color': 'neon-red',
    'is_protected': False,
    'is_system': True
})
next_id += 1

ip_limits = {}

# Роуты
@app.before_request
def cleanup_notes():
    global announcements
    now = datetime.now()
    announcements = [
        note for note in announcements
        if note['is_system'] or (now - note['timestamp']).total_seconds() < CLEANUP_INTERVAL
    ]

@app.before_request
def block_paths():
    forbidden = ['etc', 'bin', 'var', 'lib', 'usr', 'flag', 'proc']
    if any(f in request.path.lower() for f in forbidden):
        abort(403)

@app.route('/')
def index():
    return render_template('index.html', announcements=announcements)

@app.route('/post', methods=['POST'])
def post():
    global next_id
    ip = request.remote_addr
    current_time = time.time()

    if ip in ip_limits:
        ip_limits[ip] = [t for t in ip_limits[ip] if current_time - t < 3600]
        if len(ip_limits[ip]) >= 10:
            abort(429)
    else:
        ip_limits[ip] = []

    ip_limits[ip].append(current_time)

    content = request.form.get('content', '').strip()
    protect = request.form.get('protect') == 'on'

    processed_content = encrypt_data(content) if protect else content

    new_note = {
        'id': next_id,
        'content': processed_content,
        'timestamp': datetime.now(),
        'color': 'neon-blue' if protect else random.choice(['yellow', 'pink', 'green']),
        'is_protected': protect,
        'is_system': False
    }
    
    announcements.append(new_note)
    next_id += 1

    return redirect(url_for('show_note', note_id=new_note['id']))

@app.route('/note/<int:note_id>')
def show_note(note_id):
    note = next((n for n in announcements if n['id'] == note_id), None)
    if not note:
        abort(404)
    
    if not note['is_protected']:
        forbidden_dirs = ['etc', 'bin', 'var', 'lib', 'usr', 'flag', 'proc']
        content = note['content']
        template_expressions = re.findall(r'\{\{(.*?)\}\}', content, re.DOTALL)
        for expr in template_expressions:
            for directory in forbidden_dirs:
                if directory in expr.lower():
                    abort(403)
    
    return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Note #{note_id}</title>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        </head>
        <body>
            <div class="note-page">
                <div class="note {note['color']} {'protected' if note['is_protected'] else ''}">
                    <div class="protection-label">{"🔒 ЗАЩИЩЕНО" if note['is_protected'] else ""}</div>
                    <div class="content">{note['content']}</div>
                    <div class="timestamp">{note['timestamp']}</div>
                </div>
                <a href="/">← Назад к доске</a>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
