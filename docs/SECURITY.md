# SECURITY

## Assumptions
- ECC (SECP384R1) is secure
- SHA-256 is strong
- DNA adds obscurity

## Attack Resistance
- ✅ Replay: one-time challenges
- ✅ MITM: ECC identity
- ✅ Tampering: HMAC integrity
