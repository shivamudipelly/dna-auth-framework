# client/test_scenarios.py
import requests
import time
import hmac
import hashlib
from crypto_lib.ecc_handler import ECCHandler
from crypto_lib.dna_encoder import DNAEncoder

SERVER = "http://127.0.0.1:5000"

def result(scenario: str, passed: bool, msg: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n[{status}] {scenario}")
    if msg:
        print(f"   → {msg}")

def wait():
    time.sleep(1.5)

# -----------------------------------------------
# 🔹 Test 1: Normal Success
# -----------------------------------------------
def test_success():
    ecc = ECCHandler()
    pub = ecc.get_public_pem()
    sig = ecc.sign_message(pub.encode('utf-8')).hex()

    try:
        r = requests.post(f"{SERVER}/connect", json={'id': 'DEV-001', 'pub': pub, 'sig': sig})
        if r.status_code != 200:
            result("Success", False, f"Connect failed: {r.json().get('error', 'Unknown')}")
            return

        data = r.json()
        chal = DNAEncoder.decode(data['challenge_dna'])
        secret = ecc.compute_shared_secret(data['server_public_key'])
        resp = DNAEncoder.encode(hmac.new(secret, chal, hashlib.sha256).digest())

        res = requests.post(f"{SERVER}/validate", json={'id': 'DEV-001', 'resp': resp})
        success = res.json().get('status') == 'success'
        result("Success", success, "Authentication should succeed")
    except Exception as e:
        result("Success", False, f"Exception: {e}")

# -----------------------------------------------
# 🔹 Test 2: Invalid Signature (Valid Hex, Wrong Sig)
# -----------------------------------------------
def test_invalid_sig():
    ecc = ECCHandler()
    # Use a valid-length hex string that is NOT the real signature
    fake_sig = 'a' * 64  # 64 chars = 32 bytes → valid hex

    try:
        r = requests.post(f"{SERVER}/connect", json={
            'id': 'DEV-002',
            'pub': ecc.get_public_pem(),
            'sig': fake_sig
        })
        # Should reject with 400 due to invalid signature
        passed = r.status_code == 400
        result("Invalid Signature", passed, "Server should reject invalid signature")
    except Exception as e:
        result("Invalid Signature", False, f"Exception: {e}")

# -----------------------------------------------
# 🔹 Test 3: Replay Attack
# -----------------------------------------------
def test_replay():
    ecc = ECCHandler()
    pub = ecc.get_public_pem()
    sig = ecc.sign_message(pub.encode('utf-8')).hex()

    try:
        r = requests.post(f"{SERVER}/connect", json={'id': 'DEV-003', 'pub': pub, 'sig': sig})
        if r.status_code != 200:
            result("Replay Attack", False, "First connect failed")
            return

        data = r.json()
        chal = DNAEncoder.decode(data['challenge_dna'])
        secret = ecc.compute_shared_secret(data['server_public_key'])
        resp = DNAEncoder.encode(hmac.new(secret, chal, hashlib.sha256).digest())

        # First validation → should succeed
        requests.post(f"{SERVER}/validate", json={'id': 'DEV-003', 'resp': resp})

        # Second validation → should fail (replay)
        r2 = requests.post(f"{SERVER}/validate", json={'id': 'DEV-003', 'resp': resp})
        failed = r2.json().get('status') == 'failure'
        result("Replay Attack", failed, "Second attempt should be rejected")
    except Exception as e:
        result("Replay Attack", False, f"Exception: {e}")

# -----------------------------------------------
# 🔹 Test 4: Unknown Device ID
# -----------------------------------------------
def test_unknown():
    try:
        r = requests.post(f"{SERVER}/validate", json={'id': 'HACKER', 'resp': 'AGCT'})
        failed = r.json().get('status') == 'failure'
        result("Unknown Device ID", failed, "Unknown ID should fail")
    except Exception as e:
        result("Unknown Device ID", False, f"Exception: {e}")

# -----------------------------------------------
# 🔹 Test 5: Tampered Response (Modified HMAC)
# -----------------------------------------------
def test_tampered():
    ecc = ECCHandler()
    pub = ecc.get_public_pem()
    sig = ecc.sign_message(pub.encode('utf-8')).hex()

    try:
        r = requests.post(f"{SERVER}/connect", json={'id': 'DEV-005', 'pub': pub, 'sig': sig})
        if r.status_code != 200:
            return

        data = r.json()
        chal = DNAEncoder.decode(data['challenge_dna'])
        secret = ecc.compute_shared_secret(data['server_public_key'])
        digest = hmac.new(secret, chal, hashlib.sha256).digest()

        # Modify one byte of the HMAC
        tampered_digest = bytes([digest[0] ^ 1]) + digest[1:]
        tampered_dna = DNAEncoder.encode(tampered_digest)

        r2 = requests.post(f"{SERVER}/validate", json={'id': 'DEV-005', 'resp': tampered_dna})
        failed = r2.json().get('status') == 'failure'
        result("Tampered Response", failed, "Modified HMAC should fail")
    except Exception as e:
        result("Tampered Response", False, f"Exception: {e}")

# -----------------------------------------------
# 🔹 Test 6: No Server Running
# -----------------------------------------------
def test_no_server():
    try:
        # Try to connect to server
        requests.get("http://127.0.0.1:5000", timeout=2)
        result("No Server Test", False, "Server is running — stop it to test this case")
    except requests.exceptions.ConnectionError:
        result("No Server Test", True, "Connection failed as expected")
    except Exception as e:
        result("No Server Test", False, f"Unexpected error: {e}")

# -----------------------------------------------
# 🚀 Run All Tests
# -----------------------------------------------
if __name__ == '__main__':
    print("🔍 Running Authentication Test Suite...")
    print("💡 Note: 'No Server Test' only passes if server is NOT running")
    print("-" * 60)

    wait(); test_success(); wait()
    test_invalid_sig(); wait()
    test_replay(); wait()
    test_unknown(); wait()
    test_tampered(); wait()
    test_no_server()

    print("\n" + "🎯 TEST SUITE COMPLETE" + "\n")