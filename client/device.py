import requests
import time
import hmac
import hashlib
from crypto_lib.ecc_handler import ECCHandler
from crypto_lib.dna_encoder import DNAEncoder
import sys


DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "SIM-DEVICE-001"
SERVER_URL = "http://127.0.0.1:5000"

class IoTDevice:
    def __init__(self):
        self.ecc = ECCHandler()

    def animate(self, msg, steps=8):
        for _ in range(steps):
            for c in ".  .. ...":
                print(f"\r[ DEVICE ] {msg}{c}", end="", flush=True)
                time.sleep(0.2)

    def run(self):
        print("\n" + "━" * 50)
        print("    🔐 LIGHTWEIGHT AUTHENTICATION FRAMEWORK")
        print("    Device: " + DEVICE_ID)
        print("━" * 50)

        self.animate("Booting Up")
        self.animate("Connecting to Cloud", 6)

        pub_key = self.ecc.get_public_pem()
        sig = self.ecc.sign_message(pub_key.encode('utf-8')).hex()

        try:
            resp = requests.post(f"{SERVER_URL}/connect", json={
                'id': DEVICE_ID,
                'pub': pub_key,
                'sig': sig
            })

            if resp.status_code != 200:
                print(f"\n❌ Connection failed: {resp.json().get('error')}")
                return

            data = resp.json()
            self.animate("Computing Response", 6)

            chal_bytes = DNAEncoder.decode(data['challenge_dna'])
            secret = self.ecc.compute_shared_secret(data['server_public_key'])
            hmac_digest = hmac.new(secret, chal_bytes, hashlib.sha256).digest()
            response_dna = DNAEncoder.encode(hmac_digest)

            result = requests.post(f"{SERVER_URL}/validate", json={
                'id': DEVICE_ID,
                'resp': response_dna
            })

            if result.json().get('status') == 'success':
                print("\n" + "✅" * 20)
                print("     ✅ AUTHENTICATION SUCCESSFUL!")
                print("     Secure tunnel established.")
                print("✅" * 20)
            else:
                print("\n" + "❌" * 20)
                print("     ❌ AUTHENTICATION FAILED!")
                print("❌" * 20)

        except Exception as e:
            print(f"\n🚨 Network Error: {e}")

if __name__ == '__main__':
    device = IoTDevice()
    device.run()
