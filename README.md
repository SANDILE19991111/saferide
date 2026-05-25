# 🛡️ SafeRide - AI-Powered Biometric Ride Safety System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Live Deployment

**Access the app here:** [https://saferide-afmlopappj3yux9itozrocz.streamlit.app/](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)

---

## 📌 Overview

SafeRide is an **AI-powered biometric safety layer** for ride-hailing platforms in South Africa. It addresses a critical gap in existing services like Bolt and Uber: **passenger identity verification**.

---

## 🔐 User Authentication System

### Sign Up (New Users)
When you use SafeRide for the first time:

1. Navigate to **Register Page**
2. Enter your Full Name, Phone Number, Email
3. Add Emergency Contact Name & Number
4. Upload a clear face photo
5. Click Register
6. Save your unique **User ID**

### Sign In (Existing Users)
If you already have an account:

1. Navigate to **Verify Identity Page**
2. Enter your User ID
3. Take a live selfie with your camera
4. AI matches your face with stored data
5. Access ride services after verification

### Database Storage
All user data is securely stored including:
- User profiles with encrypted face encodings
- Complete ride history
- SOS event logs
- Emergency contact information

---

## ✨ Features

### 🔐 Biometric Security
- Face Recognition (128-point encoding using ResNet-34)
- Live Selfie Capture for verification
- Confidence Scoring (0-100% match display)
- Secure database storage

### 👤 User Management
- Sign Up with face photo registration
- Sign In with biometric verification
- Profile Management
- Emergency Contacts storage
- Ride History tracking

### 🤖 AI Integration
- Google Gemini 2.5 Flash for safety reports
- Free tier: 250 requests/day

### 🚨 Emergency Features
- One-Tap SOS button
- GPS Location Tracking
- Automatic Emergency Contact notification
- SAPS evidence unlocking

### 🚗 Ride Management
- Distance-Based Pricing (per kilometer)
- Multiple Ride Types: Standard, Comfort, Premium, XL, Electric
- Peak Hour Surcharge (30% during 7-9am & 4-7pm)
- Live Route Map

### 📊 User Dashboard
- Profile Information
- Ride Statistics (total rides & spending)
- Ride History
- Emergency Contacts management

---

## 📱 Usage Guide

### New User Registration
1. Open the app → Click "Register"
2. Fill in your personal details
3. Upload your face photo
4. Save your User ID

### Existing User Sign In
1. Click "Verify Identity"
2. Enter your User ID
3. Take a live selfie
4. Get verified instantly

### Request a Ride
1. Sign in first
2. Click "Request Ride"
3. Select pickup and destination
4. Choose ride type
5. Review price calculation
6. Confirm ride

### Emergency SOS
1. During an active ride
2. Click the SOS button
3. System notifies emergency contacts and SAPS

### View Dashboard
1. Click "My Dashboard"
2. View your ride statistics and history

---

## 💰 Price Calculation

### Rate Table

| Ride Type | Rate/km | Minimum Fare |
|-----------|---------|--------------|
| Standard | R12 | R35 |
| Comfort | R18 | R50 |
| Premium | R25 | R70 |
| XL (6 seater) | R20 | R60 |
| Electric | R15 | R45 |

**Peak Hours:** 7-9am and 4-7pm (30% surcharge)

---

## 🔒 Security & Privacy (POPIA Compliant)

| Control | Status |
|---------|--------|
| ID Number Hashing (SHA-256) | ✅ |
| Face Data as 128-point encoding | ✅ |
| API Key Security (.env) | ✅ |
| Evidence Locking | ✅ |
| Consent Collection | ✅ |
| Zero Third-party Sharing | ✅ |

**Planned:** AES-256 Encryption, 90-day Auto-Delete

---

## 📁 Database Structure

The app automatically creates these files in the `biometric_data/` folder:

- **users.json** - Registered user profiles with face encodings
- **rides.json** - Complete ride history
- **sos_log.json** - SOS event logs

---

## 📞 Support

- **Live App:** [https://saferide-afmlopappj3yux9itozrocz.streamlit.app/](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)
- **GitHub:** [github.com/SANDILE19991111/saferide](https://github.com/SANDILE19991111/saferide)
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

**v1.0.0** (Current) - Initial release
- User registration with database
- Biometric sign-in
- Ride request and tracking
- SOS emergency system
- Dashboard with statistics

---

**Built with ❤️ for safer South African roads**

*"SafeRide - Your Safety, Our Priority"*
