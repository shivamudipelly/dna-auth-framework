from flask import Flask, request, jsonify
from auth_logic import AuthenticationHandler
import threading
import time

app = Flask(__name__)
auth_handler = AuthenticationHandler()

def show_banner():
    time.sleep(1)
    print("\n" + "="*60)
    print("          🔐 CLOUD AUTHENTICATION BACKEND ACTIVE")
    print("          Listening: http://127.0.0.1:5000")
    print("          Status: Ready for device authentication")
    print("="*60 + "\n")

threading.Thread(target=show_banner, daemon=True).start()

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    print(f"📡 [IN] Connection from Device {data.get('id')}")
    resp = auth_handler.generate_challenge(data)
    status = 400 if 'error' in resp else 200
    if status == 200:
        print(f"✅ [OUT] Challenge sent to {data['id']}")
    return jsonify(resp), status

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    print(f"🔐 [IN] Validation from {data['id']}")
    is_valid = auth_handler.validate_response(data)
    result = 'success' if is_valid else 'failure'
    print(f"{'✅' if is_valid else '❌'} [AUTH] {data['id']} → {result.upper()}")
    return jsonify({'status': result})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
