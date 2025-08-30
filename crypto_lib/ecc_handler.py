from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

class ECCHandler:
    """Handles ECC key generation, signing, and ECDH."""
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()

    def get_public_pem(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    def sign_message(self, message: bytes) -> bytes:
        return self.private_key.sign(message, ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_signature(pub_pem: str, signature: bytes, message: bytes) -> bool:
        try:
            pub = serialization.load_pem_public_key(pub_pem.encode('utf-8'))
            pub.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False

    def compute_shared_secret(self, peer_pem: str) -> bytes:
        peer = serialization.load_pem_public_key(peer_pem.encode('utf-8'))
        return self.private_key.exchange(ec.ECDH(), peer)
