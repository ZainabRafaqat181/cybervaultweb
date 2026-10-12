from flask import Flask, render_template, request, send_file, jsonify
from cryptography.fernet import Fernet
import io
import os

app = Flask(__name__)

def load_key():
    return b"9kTM8U9WaaXsYuHsuroaDEADnk2GmKl6aYjNtoKyxLI="

enc_count = 0
dec_count = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    global enc_count
    file = request.files.get('file')
    if not file or file.filename == "":
        return jsonify({"msg": "Select a file first"}), 400
    try:
        key = load_key()
        f = Fernet(key)
        data = file.read()
        encrypted = f.encrypt(data)
        enc_count += 1
        return send_file(io.BytesIO(encrypted), download_name=file.filename, as_attachment=True)
    except Exception as e:
        return jsonify({"msg": f"Encrypt Error: {e}"}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    global dec_count
    file = request.files.get('file')
    if not file or file.filename == "":
        return jsonify({"msg": "Select a file first"}), 400
    try:
        key = load_key()
        f = Fernet(key)
        data = file.read()
        decrypted = f.decrypt(data)
        dec_count += 1
        return send_file(io.BytesIO(decrypted), download_name=file.filename, as_attachment=True)
    except Exception as e:
        return jsonify({"msg": "Decrypt failed - wrong key or file not encrypted"}), 400

@app.route('/stats')
def get_stats():
    return jsonify({"enc": enc_count, "dec": dec_count})

if __name__ == '__main__':
    load_key()
    print("Starting Cyber Vault...")
    app.run(debug=True)