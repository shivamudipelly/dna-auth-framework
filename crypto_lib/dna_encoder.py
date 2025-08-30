class DNAEncoder:
    """Encodes bytes to DNA string using 2-bit mapping."""
    MAP = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    REV = {v: k for k, v in MAP.items()}

    @staticmethod
    def encode(data_bytes: bytes) -> str:
        binary = ''.join(f"{b:08b}" for b in data_bytes)
        if len(binary) % 2 != 0:
            binary += '0'
        return ''.join(DNAEncoder.MAP[binary[i:i+2]] for i in range(0, len(binary), 2))

    @staticmethod
    def decode(dna_string: str) -> bytes:
        try:
            binary = ''.join(DNAEncoder.REV[nuc] for nuc in dna_string)
            binary = binary[:len(binary)//8*8]  # Trim to full bytes
            return int(binary, 2).to_bytes(len(binary)//8, 'big')
        except Exception:
            return b''
