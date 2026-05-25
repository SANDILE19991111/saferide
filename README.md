# 🛡️ SafeRide - AI-Powered Biometric Ride Safety System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 🌐 Live Deployment

| **Item** | **Link** |
|----------|----------|
| **Live App** | [https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app](https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app) |
| **GitHub Repository** | [https://github.com/SANDILE19991111/saferide](https://github.com/SANDILE19991111/saferide) |

---

## 📌 Overview

SafeRide is an **AI-powered biometric safety layer** for ride-hailing platforms in South Africa. It addresses a critical gap in existing services like Bolt and Uber: **passenger identity verification**.

Currently, drivers undergo rigorous background checks, vehicle inspections, and license verification. Passengers, however, face no equivalent scrutiny. Anyone can register with a fake name, and account sharing is common. This asymmetry creates real danger for both drivers and passengers.

**SafeRide solves this by requiring every rider to pass face recognition verification before any driver is assigned.**

✅ **Live, working app deployed to Streamlit Cloud – accessible from any phone or browser.**

---

## 🔐 User Authentication System

### Sign Up (New Users)
1. Navigate to **Register Page**
2. Enter your Full Name, Phone Number, Email
3. Add Emergency Contact Name & Number
4. Upload a clear face photo
5. Click Register
6. Save your unique **User ID**

### Sign In (Existing Users)
1. Navigate to **Verify Identity Page**
2. Enter your User ID
3. Take a live selfie with your camera
4. AI matches your face with stored data
5. Access ride services after verification

### Database Storage
All user data is securely stored including:
- User profiles with 128-point face encodings (not raw images)
- Complete ride history
- SOS event logs
- SAPS monitoring records

---

## ✨ Features

### 🔐 Biometric Security
- **Face Recognition** – 128-point encoding using DeepFace VGG-Face
- **Live Selfie Capture** – Real-time camera verification
- **Confidence Scoring** – 0-100% match display
- **Secure database storage** – POPIA compliant foundation

### 👤 User Management
- Sign Up with face photo registration
- Sign In with biometric verification
- Profile Management
- Emergency Contacts storage
- Ride History tracking

### 🤖 AI Integration
- **Google Gemini 2.5 Flash** – Generates personalized driver safety reports
- **Free tier** – 250 requests/day, no credit card required
- **Prompt engineering** – Structured prompts with rider history

### 🚨 Emergency Features
- **One-Tap SOS button** – Pulse animation, immediate alert
- **GPS Location Tracking** – Real-time location sharing
- **Automatic Emergency Contact notification**
- **SAPS evidence unlocking framework**

### 🚗 Ride Management
- **Distance-Based Pricing** – Per kilometer rates (R12–R25/km)
- **Multiple Ride Types** – Standard, Comfort, Premium, XL, Electric
- **Peak Hour Surcharge** – 30% extra during 7-9am & 4-7pm
- **Live Route Map** – Interactive route visualization
- **13 SA Locations** – Johannesburg, Cape Town, Durban, OR Tambo, etc.

### 👮 SAPS Real-Time Monitoring (Framework)
- **Unique Monitoring ID** generated for every ride
- **Ride details logged** – Rider, driver, route, timestamps
- **GPS tracking simulation** – Route progress monitoring
- **Framework ready** for direct SAPS API connection

### 📊 User Dashboard
- Profile Information
- Ride Statistics (total rides & spending)
- Ride History
- Emergency Contacts management

---

## 🚀 How It Works
┌─────────────────────────────────────────────────────────────────────────┐
│ USER FLOW │
├─────────────────────────────────────────────────────────────────────────┤
│ │
│ 📝 SIGN UP → Take face photo → Get User ID │
│ │ │
│ ▼ │
│ 🔐 SIGN IN → Enter User ID → Take live selfie → AI verification │
│ │ │
│ ▼ │
│ 🚗 REQUEST RIDE → Select pickup/destination → Choose ride type │
│ │ │
│ ▼ │
│ 👮 SAPS MONITORING → Unique ID generated → Route tracking │
│ │ │
│ ▼ │
│ 🆘 SOS (If needed) → One-tap alert → Emergency services notified │
│ │
└─────────────────────────────────────────────────────────────────────────┘

text

---

## 💰 Price Calculation

### Rate Table
| Ride Type | Rate/km | Minimum Fare |
|-----------|---------|--------------|
| Standard | R12.50 | R35 |
| Comfort | R18.00 | R50 |
| Premium | R25.00 | R70 |
| XL (6 seater) | R20.00 | R60 |
| Electric | R15.00 | R45 |

**Peak Hours:** 7-9am and 4-7pm (30% surcharge)

**Example:** 15 km Comfort ride at 8am = R351

---

## 🔒 Security & POPIA Compliance

| Control | Status |
|---------|--------|
| Data Minimization (128-point encoding only) | ✅ |
| Explicit Consent at sign-up | ✅ |
| API Key Security (.env + Secrets) | ✅ |
| Access Logging (rides & SOS events) | ✅ |
| Purpose Limitation (safety only) | ✅ |
| Zero Third-party Sharing | ✅ |
| AES-256 Encryption | 📋 Planned |
| 90-day Auto-Delete | 📋 Planned |

---

## ⚠️ Challenges Faced During Development

| Challenge | Resolution |
|-----------|------------|
| `face_recognition` fails on Windows (dlib/CMake) | Switched to DeepFace + TensorFlow |
| Gemini SDK deprecated | Migrated to `google-genai` SDK |
| Claude API not free | Switched to Gemini 2.5 Flash (free tier) |
| `libGL.so.1` missing on Streamlit Cloud | Added `packages.txt` with `libgl1-mesa-dri` |
| API key exposed in chat | Revoked key, moved to Secrets + `.env` |
| Streamlit not mobile-friendly | Created `run_mobile.py` with `0.0.0.0` |
| Poor lighting face recognition | Display confidence score + user guidance |
| No SA address search without paid API | Integrated OpenStreetMap Nominatim API |

---

## 🔮 Future Roadmap

### Short-term (3-6 months)
- ✅ Real SAPS API integration (actual police endpoint)
- ✅ Automated police dispatch on SOS
- ✅ Bolt South Africa partnership
- ✅ Real fingerprint sensor hardware

### Medium-term (6-12 months)
- ✅ Uber Safety API integration
- ✅ inDrive partnership
- ✅ AES-256 encryption for biometric data
- ✅ Native mobile app (React Native)

### Long-term (12+ months)
- ✅ National ride-hailing safety network (all platforms)
- ✅ AI predictive policing for high-risk rides
- ✅ Multi-country expansion (Kenya, Nigeria, Egypt)

**Vision:** Every ride-hailing trip in South Africa is verified by biometrics and monitored by SAPS in real-time.

---

## 📁 Database Structure

The app automatically creates these files in the `biometric_data/` folder:

| File | Purpose |
|------|---------|
| `users.json` | Registered user profiles with 128-point face encodings |
| `rides.json` | Complete ride history with pricing and routes |
| `sos_log.json` | SOS event logs with timestamps and locations |
| `saps_monitoring.json` | SAPS monitoring records with unique IDs |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit (Python) |
| Face Recognition | DeepFace + VGG-Face |
| AI Reports | Google Gemini 2.5 Flash |
| Backend | Python 3.11 |
| Data Storage | JSON (prototype) |
| Deployment | Streamlit Cloud |
| Maps | Streamlit `st.map` |

---

## 📞 Support

- **Live App:** [https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app](https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app)
- **GitHub:** [https://github.com/SANDILE19991111/saferide](https://github.com/SANDILE19991111/saferide)
- **Developer:** Bongimusa Sandile Khoza
- **Bootcamp:** CAPACITI x Clickatell AI Bootcamp 2026

---

## 🙏 Acknowledgments

- **CAPACITI** for the AI Bootcamp opportunity
- **Clickatell** for industry sponsorship
- **Google** for Gemini API free tier
- **Streamlit** for easy web app deployment

---

## 📄 License

MIT License

---

## 🎯 Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | May 2026 | Initial release – registration, biometric sign-in, ride request, SOS |
| v1.1.0 | May 2026 | Added SAPS monitoring framework, dynamic pricing, SA locations |

---

**Built with ❤️ for safer South African roads 🇿🇦**

*"SafeRide – Your Safety. Our Priority."*
