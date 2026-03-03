
# 🛡️ Veritone AI
### **High-Fidelity Voice Fraud Detection & Acoustic Forensic API**

[![Vercel Deployment](https://img.shields.io/badge/Deploy-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com)
[![Python Version](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Veritone AI** is a specialized forensic tool designed to distinguish between genuine human speech and AI-generated synthetic voices. Engineered for the modern security landscape, it provides real-time protection against deepfake audio fraud and identity theft by analyzing unique vocal patterns and acoustic features.

---

## 🚀 Key Capabilities

* **Multilingual Forensic Engine**: Specialized detection for **English, Hindi, Tamil, Telugu, and Malayalam**.
* **Acoustic Fingerprinting**: Analyzes audio data to detect non-human resonance and synthetic patterns.
* **Probability Scoring**: Returns a granular `confidenceScore` for every scan to indicate prediction certainty.
* **Serverless Optimized**: Designed for low-latency execution and high availability.
* **Security First**: Built-in `x-api-key` validation to ensure only authorized clients access the forensic scanner.

---

## 🛠️ Technical Stack

* **Backend**: Python / Flask.
* **Dependencies**: Flask 2.3.3 and Werkzeug 2.3.7.
* **Processing**: Base64 Audio Decoding and specialized validation logic.
* **Deployment**: Optimized for Vercel and compatible with standard WSGI environments.

---

## 📡 API Architecture

### **Detect Voice Fraud**
`POST /api/voice-detection`

**Headers:**
```http
Content-Type: application/json
x-api-key: your_api_key_here
