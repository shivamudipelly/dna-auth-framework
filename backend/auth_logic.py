import os
import hmac
import hashlib
from crypto_lib.ecc_handler import ECCHandler
from crypto_lib.dna_encoder import DNAEncoder

class AuthenticationHandler:
    def __init__(self):
        self.server_ecc = ECCHandler()
        self.pending_challenges = {}

    def generate_challenge(self, data):
        client_id = data['id']
        client_pub = data['pub']
        signature = bytes.fromhex(data['sig'])

        if not ECCHandler.verify_signature(client_pub, signature, client_pub.encode('utf-8')):
            return {'error': 'Invalid signature'}

        challenge = os.urandom(32)
        self.pending_challenges[client_id] = {
            'challenge': challenge,
            'public_key': client_pub
        }

        return {
            'challenge_dna': DNAEncoder.encode(challenge),
            'server_public_key': self.server_ecc.get_public_pem()
        }

    def validate_response(self, data):
        client_id = data['id']
        response_dna = data['resp']

        if client_id not in self.pending_challenges:
            return False

        session = self.pending_challenges.pop(client_id)
        orig_challenge = session['challenge']
        client_pub = session['public_key']

        shared = self.server_ecc.compute_shared_secret(client_pub)
        expected = hmac.new(shared, orig_challenge, hashlib.sha256).digest()
        expected_dna = DNAEncoder.encode(expected)

        return hmac.compare_digest(response_dna, expected_dna)
