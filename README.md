# 🔐 Lightweight Authentication Framework for Cloud Integration Using DNA Cryptography

> A secure, lightweight authentication system for IoT devices using **Elliptic Curve Cryptography (ECC)** and **DNA-based encoding**, simulating cloud backend behavior.

This project demonstrates a **realistic IoT-cloud authentication handshake** using ECC for identity and HMAC challenge-response for integrity — all simulated locally using a Flask server.  
No AWS required. Fully self-contained.

Designed for **minor project evaluation**, this system mimics the security protocols used in platforms like **AWS IoT Core**, but runs entirely on a local machine.

---

## 🧩 Key Features

| Feature | Description |
|--------|-------------|
| ✅ **ECC-Based Identity** | Uses `SECP384R1` for secure key generation and digital signatures |
| ✅ **Challenge-Response Flow** | Prevents replay attacks with one-time challenges |
| ✅ **DNA-Based Encoding** | Novel data representation layer (A, C, G, T) for obfuscation |
| ✅ **HMAC-SHA256** | Ensures message integrity using ECDH-derived shared secret |
| ✅ **Replay Attack Protection** | Each challenge is used only once |
| ✅ **No Cloud Dependency** | Simulates cloud backend using Flask (runs locally) |
| ✅ **Test Suite** | Validates success, invalid signatures, tampering, and replay |

---

## 📁 Folder Structure

```
dna-auth-framework/
│
├── crypto_lib/           # Shared security core
│   ├── ecc_handler.py    # ECC: keys, signing, ECDH
│   └── dna_encoder.py    # DNA: encode/decode
│
├── backend/              # Simulated cloud backend
│   ├── server.py         # Flask API: /connect, /validate
│   ├── auth_logic.py     # Authentication logic
│   └── requirements.txt  # Flask, cryptography
│
├── client/               # Simulated IoT device
│   ├── device.py         # Clean UI: successful authentication
│   ├── test_scenarios.py # 6 test cases (security validation)
│   └── requirements.txt  # requests, cryptography
│
├── docs/                 # Documentation
│   ├── DESIGN.md         # System architecture
│   └── SECURITY.md       # Threat model & assumptions
│
├── .gitignore            # Excludes venv/, pycache, etc.
├── README.md             # This file
└── LICENSE               # MIT License
```

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/dna-auth-framework.git
cd dna-auth-framework
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# OR on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install backend packages
pip install -r backend/requirements.txt

# Install client packages
pip install -r client/requirements.txt
```

### 4. Start the Server (Terminal 1)
```bash
python backend/server.py
```
You’ll see:
```
☁️ Cloud Backend Active: http://127.0.0.1:5000
```

### 5. Run the Client (Terminal 2)
```bash
python client/device.py
```
You’ll see:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔐 LIGHTWEIGHT AUTHENTICATION FRAMEWORK
    Device: SIM-DEVICE-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ✅ AUTHENTICATION SUCCESSFUL!
```

### 🧪 Run the Security Test Suite
To validate robustness, run:
```bash
python client/test_scenarios.py
```
**✅ Test Cases Covered:**
- Normal Success: Baseline working case
- Invalid Signature: Proves identity verification
- Replay Attack: Prevents reuse of old responses
- Unknown Device ID: Blocks unauthorized access
- Tampered Response: Detects modified HMAC
- No Server Running: Only passes if server is down

🔁 This proves the system is not just functional — it’s secure.

---

## 📚 Documentation

- `docs/DESIGN.md` — Explains system architecture, data flow, and API design
- `docs/SECURITY.md` — Describes threat model, assumptions, and attack resistance

---

## 👥 Team Roles & Responsibilities

- **V. Nithin Raj** — Cryptography Developer (Built `crypto_lib`: ECC + DNA encoding)
- **G. Likhitha Reddy** — Backend Logic Developer (Designed auth flow, challenge/response logic)
- **M. Shiva** — Backend API Developer (Built Flask server and API endpoints)
- **K. Santosh** — Client Developer (Developed simulated IoT device and UI)

---

## 🎓 Project Explanation for Viva

> "This project simulates a secure IoT authentication system using ECC and DNA-based encoding.
> The device proves its identity by signing its public key.
> The server issues a one-time challenge encoded in DNA.
> The device responds using a shared secret (ECDH + HMAC).
> The system prevents replay attacks and runs locally — no AWS needed.
> We tested it against 6 real-world scenarios to prove security."

---

## 📄 License

 [LICENSE](./LICENSE) for details.