# DESIGN

## Architecture
- Client: Simulated IoT device
- Server: Flask app (simulated cloud)
- Protocol: ECC + DNA encoding + HMAC

## Flow
1. Device sends signed public key
2. Server sends DNA-encoded challenge
3. Device computes HMAC(response)
4. Server validates → success/failure
