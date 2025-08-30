# 🔐 Lightweight Authentication Framework for Cloud Integration Using DNA Cryptography

> A secure, lightweight authentication system for IoT devices using **Elliptic Curve Cryptography (ECC)** and **DNA-based encoding**, simulating cloud backend behavior.

This project demonstrates a secure challenge-response handshake between a simulated IoT device and a local Flask server — identical to protocols used in AWS IoT Core.

---

## 🧩 Features

- ✅ **ECC (SECP384R1)** for identity and key exchange
- ✅ **DNA Encoding** as a novel data representation layer
- ✅ **HMAC-SHA256** for integrity and replay attack prevention
- ✅ **Challenge-Response** authentication flow
- ✅ **Test Suite** with 6 security scenarios
- ✅ **No AWS Required** — runs locally for accessibility

---

## 📁 Folder Structure

```
dna-auth-framework/
├── crypto_lib/   # Shared ECC & DNA logic
├── backend/      # Simulated cloud server (Flask)
├── client/       # Simulated IoT device
└── docs/         # Design & security docs
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install flask requests cryptography
```

### 2. Start Server (Terminal 1)
```bash
python backend/server.py
```

### 3. Run Client (Terminal 2)
```bash
python client/device.py
```

You’ll see:
```
✅ AUTHENTICATION SUCCESSFUL!
```

### 🧪 Run Test Suite
```bash
python client/test_scenarios.py
```
Tests:
- ✅ Normal Success
- ✅ Invalid Signature
- ✅ Replay Attack
- ✅ Tampered Response
- ✅ Unknown Device
- ❌ No Server (only passes if server is down)

---

## 📚 Documentation

- `docs/DESIGN.md` — Architecture & flow
- `docs/SECURITY.md` — Threat model

---

## 👥 Team Roles

- **V. Nithin Raj** — Cryptography Developer
- **G. Likhitha Reddy** — Backend Logic Developer
- **M. Shiva** — Backend API Developer
- **K. Santosh** — Client Developer

---

## 📄 License

MIT License — see LICENSE file.

---