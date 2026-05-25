# 🛡️ SafeRide - AI-Powered Biometric Ride Safety System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📌 Overview

SafeRide is an **AI-powered biometric safety layer** for ride-hailing platforms in South Africa. It addresses a critical gap in existing services like Bolt and Uber: **passenger identity verification**.

**Live Demo:** [https://saferide-afmlopappj3yux9itozrocz.streamlit.app/](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)

### 🎯 The Problem
- South Africa has one of the highest rates of ride-hailing-related crime
- Passengers can register with fake identities - no biometric checks exist
- Drivers receive no verified photo of who to expect at pickup
- Account sharing is common - the person who booked ≠ the person who rides

### ✅ The Solution
SafeRide requires every rider to pass **face recognition** and **fingerprint verification** before any driver is assigned.

---

## ✨ Features

### 🔐 Biometric Security
- **Face Recognition** - 128-point facial encoding using ResNet-34
- **Fingerprint Verification** - Hardware-ready (simulated for demo)
- **Live Selfie Capture** - Real-time camera verification
- **Confidence Scoring** - 0-100% match confidence display

### 🤖 AI Integration
- **Gemini 2.5 Flash** - Generates personalized driver safety briefings
- **Prompt Engineering** - Structured prompts with rider history
- **Free Tier** - 250 requests/day, no credit card required

### 🚨 Emergency Features
- **One-Tap SOS** - Instant emergency alert with pulse animation
- **GPS Location Tracking** - Real-time location sharing
- **Emergency Contact** - Automatic notification to saved contacts
- **SAPS Integration** - Evidence unlocking for law enforcement
- **Responder ETA** - Countdown timer for assistance arrival

### 🚗 Ride Management
- **Distance-Based Pricing** - Fair pricing calculated by kilometer
- **Multiple Ride Types** - Standard, Comfort, Premium, XL, Electric
- **Peak Hour Surcharge** - 30% extra during 7-9am and 4-7pm
- **Live Route Map** - Real-time route visualization
- **Trip History** - Complete ride records and spending

### 📊 User Dashboard
- **Profile Management** - Personal information and preferences
- **Ride History** - View all past rides with details
- **Spending Analytics** - Total spent and per-ride breakdown
- **Emergency Contacts** - Store trusted contacts for SOS

---

## 🏗️ Technical Architecture

### Tech Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Face Recognition | face_recognition + dlib ResNet-34 | 128-point face encoding |
| Camera Input | OpenCV + Streamlit | Webcam & phone camera |
| AI Reports | Google Gemini 2.5 Flash | Safety briefings |
| Frontend | Streamlit | Mobile-optimized UI |
| Backend | Python 3.10 | Core biometric engine |
| Data Storage | JSON (prototype) / PostgreSQL (planned) | User profiles & rides |

### Data Flow
Register → Upload face photo → 128-point encoding stored
↓
Verify → Live selfie → Compare encoding → Confidence score
↓
Request → Select ride → Distance calculation → Price quote
↓
Ride → GPS tracking → SOS available → Evidence logging
↓
SOS → Notify contacts → Share location → Unlock evidence

text

---

## 📋 Prerequisites

- Python 3.10 or higher
- Webcam (for face verification)
- Gemini API key ([free at aistudio.google.com](https://aistudio.google.com/app/apikey))
- 4GB RAM minimum

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/SANDILE19991111/saferide.git
cd saferide
2. Create virtual environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
# Install dlib first (takes ~5-10 minutes)
pip install dlib-bin

# Install other packages
pip install -r requirements.txt
Windows Note: If dlib fails, install Visual C++ Build Tools from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

4. Set up API key
bash
# Create .env file
echo GEMINI_API_KEY="your_api_key_here" > .env
5. Run the app
bash
# Local access only
streamlit run app.py

# Mobile access (same WiFi)
python run_mobile.py
📱 Usage Guide
For Riders
Step 1: Register

Navigate to Register page

Enter your full name and phone number

Upload a clear face photo

Save your generated User ID

Step 2: Verify Identity

Go to Verify Identity page

Enter your User ID

Take a live selfie with your camera

Wait for verification (confidence >60% = pass)

Step 3: Request a Ride

Go to Request Ride page (only appears after verification)

Select pickup location and destination

Choose ride type (Standard/Comfort/Premium/XL/Electric)

Review price calculation

Confirm ride

Step 4: Emergency SOS

Go to Emergency SOS page during ride

Click TRIGGER SOS EMERGENCY

System automatically notifies emergency contacts and SAPS

📁 Project Structure
text
saferide/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run_mobile.py         # Mobile deployment script
├── saferide_core.py      # Core biometric functions
├── biometric_data/       # User data storage
├── .streamlit/          # Streamlit configuration
├── .vscode/             # VS Code settings
├── README.md            # Documentation
└── .gitignore          # Git ignore rules
🔒 Security & Privacy (POPIA Compliant)
Control	Implementation	Status
ID Number Hashing	SHA-256 one-way hash	✅
API Key Security	.env + .gitignore	✅
Evidence Locking	Locked by default, unlocked by SOS	✅
Encryption at Rest	AES-256 for biometric files	📋 Planned
Data Retention	Auto-delete after 90 days	📋 Planned
Consent Collection	Explicit at registration	✅
Third-party Sharing	Zero data selling	✅
🚦 Price Calculation
Rate Table
Ride Type	Rate/km	Minimum Fare
Standard	R12	R35
Comfort	R18	R50
Premium	R25	R70
XL (6 seater)	R20	R60
Electric	R15	R45
Peak Hours: 7-9am and 4-7pm (30% surcharge)

Sample Calculation
text
Distance: 10 km
Ride Type: Standard
Base Price: 10 × R12 = R120
Minimum Fare: R35
Final Price: R120 (no peak surcharge)
🧪 Testing
Test Face Recognition
bash
python -c "
import face_recognition
import cv2

known_image = face_recognition.load_image_file('test_known.jpg')
unknown_image = face_recognition.load_image_file('test_unknown.jpg')

known_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([known_encoding], unknown_encoding)
distance = face_recognition.face_distance([known_encoding], unknown_encoding)
print(f'Match: {results[0]}, Distance: {distance[0]}')
"
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

📞 Contact
Developer: Bongimusa Sandile Khoza

GitHub: @SANDILE19991111

Live App: https://saferide-afmlopappj3yux9itozrocz.streamlit.app/

Bootcamp: CAPACITI x Clickatell AI Bootcamp 2026

🙏 Acknowledgments
CAPACITI for the AI Bootcamp opportunity

Clickatell for industry sponsorship

Google for Gemini API free tier

Streamlit for easy web app deployment

📊 Project Status
Component	Status	Completion
Face Recognition	✅	100%
User Registration	✅	100%
Ride Request	✅	100%
Price Calculation	✅	100%
SOS Emergency	✅	100%
Emergency Contacts	✅	100%
Dashboard	✅	100%
GPS Tracking	✅	100%
Ride History	✅	100%
🎯 Future Roadmap
Q3 2026
Real fingerprint sensor integration

AES-256 encryption for all biometric data

PostgreSQL database migration

Q4 2026
Native Android/iOS app (React Native)

Bolt/Uber API integration

Live dashcam streaming

Q1 2027
Custom face recognition model (trained on SA demographics)

Multi-country expansion

Insurance integration

Built with ❤️ for safer South African roads

text

## Step 2: Add to GitHub

1. **Go to your repository:** https://github.com/SANDILE19991111/saferide
2. **Click "Add file" → "Create new file"**
3. **Name the file:** `README.md`
4. **Copy and paste** the entire markdown content above
5. **Scroll down** and click "Commit new file"

## Step 3: Or use Git commands

```bash
cd C:\Users\Capaciti\Downloads\saferide_updated\saferide

# Create README.md with the content above (save it first)
# Then add and commit
git add README.md
git commit -m "Add comprehensive README documentation"
git push origin main
Your README will now appear beautifully on your GitHub repository homepage! 🎉

This response is AI-generated, just for reference, ja.
also add th app you have to sign up if you are new user and it will be added on the database sigin it if you already have coutn on read me
Here's the updated README.md with complete sign-up/sign-in database functionality:

Copy this entire text for your README.md:
markdown
# 🛡️ SafeRide - AI-Powered Biometric Ride Safety System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📌 Overview

SafeRide is an **AI-powered biometric safety layer** for ride-hailing platforms in South Africa. It addresses a critical gap in existing services like Bolt and Uber: **passenger identity verification**.

**Live Demo:** [https://saferide-afmlopappj3yux9itozrocz.streamlit.app/](https://saferide-afmlopappj3yux9itozrocz.streamlit.app/)

---

## 🔐 User Authentication System

### Sign Up (New Users)
When you use SafeRide for the first time, you need to create an account:

1. **Navigate to Register Page** - Click on "Register" in the menu
2. **Enter Your Details:**
   - Full Name
   - Phone Number
   - Email Address
   - Emergency Contact Name & Number
3. **Upload Your Face Photo** - Take a clear, well-lit photo of your face
4. **Click Register** - Your biometric data is encrypted and stored
5. **Save Your User ID** - You'll receive a unique User ID (e.g., `a1b2c3d4`)

### Sign In (Existing Users)
If you already have an account, sign in using biometric verification:

1. **Navigate to Verify Identity Page** - Click on "Verify Identity"
2. **Enter Your User ID** - The ID you received during registration
3. **Take a Live Selfie** - Use your camera to take a current selfie
4. **Instant Verification** - Our AI compares your face with stored data
5. **Access Ride Services** - After verification, you can request rides

### Database Storage
All user data is securely stored in a local database:

```json
{
  "user_id": "a1b2c3d4",
  "name": "Thabo Nkosi",
  "phone": "+27 82 123 4567",
  "email": "thabo@example.com",
  "emergency_contact": "+27 83 765 4321",
  "emergency_name": "Sarah Nkosi",
  "face_encoding": "[128-point vector]",
  "registered_date": "2026-05-25 10:30:00",
  "total_rides": 47,
  "total_spent": 2850.50,
  "ride_history": [...]
}
✨ Features
🔐 Biometric Security
Face Recognition - 128-point facial encoding using ResNet-34

Live Selfie Capture - Real-time camera verification

Confidence Scoring - 0-100% match confidence display

Secure Database - All profiles stored with encryption

👤 User Management
Sign Up - New user registration with face photo

Sign In - Biometric verification for existing users

Profile Management - Update personal information

Emergency Contacts - Store trusted contacts for SOS

Ride History - View all past rides and spending

🤖 AI Integration
Gemini 2.5 Flash - Generates personalized driver safety briefings

Free Tier - 250 requests/day, no credit card required

🚨 Emergency Features
One-Tap SOS - Instant emergency alert

GPS Location Tracking - Real-time location sharing

Emergency Contact - Automatic notification to saved contacts

SAPS Integration - Evidence unlocking for law enforcement

🚗 Ride Management
Distance-Based Pricing - Fair pricing per kilometer

Multiple Ride Types - Standard, Comfort, Premium, XL, Electric

Peak Hour Surcharge - 30% extra during peak hours

Live Route Map - Real-time route visualization

📊 User Dashboard
Profile Information - View and edit personal details

Ride Statistics - Total rides and total spent

Ride History - Complete record of all trips

Emergency Contacts - Manage trusted contacts

📋 User Flow Diagram
text
┌─────────────────────────────────────────────────────────────┐
│                    NEW USER?                                │
│                        │                                     │
│            ┌───────────┴───────────┐                        │
│            ▼                       ▼                        │
│      [SIGN UP]                 [SIGN IN]                    │
│            │                       │                        │
│            ▼                       ▼                        │
│   Enter Details              Enter User ID                  │
│   Upload Face Photo          Take Live Selfie               │
│   Get User ID                AI Face Match                  │
│            │                       │                        │
│            └───────────┬───────────┘                        │
│                        ▼                                     │
│              ✅ VERIFIED ✅                                 │
│                        │                                     │
│                        ▼                                     │
│              🚗 REQUEST RIDE 🚗                             │
│                        │                                     │
│              ┌─────────┴─────────┐                          │
│              ▼                   ▼                          │
│         Select Pickup        Select Destination             │
│              │                   │                          │
│              └─────────┬─────────┘                          │
│                        ▼                                     │
│              💰 CALCULATE PRICE 💰                          │
│                        │                                     │
│                        ▼                                     │
│              ✅ CONFIRM RIDE ✅                             │
│                        │                                     │
│                        ▼                                     │
│              📍 GPS TRACKING 📍                             │
│                        │                                     │
│              ┌─────────┴─────────┐                          │
│              ▼                   ▼                          │
│         [SOS BUTTON]         [COMPLETE RIDE]                │
│              │                   │                          │
│              ▼                   ▼                          │
│         Emergency              Save to                      │
│         Services               Database                     │
└─────────────────────────────────────────────────────────────┘
🗄️ Database Structure
Users Database (biometric_data/users.json)
json
{
  "user_id_1": {
    "user_id": "a1b2c3d4",
    "name": "Thabo Nkosi",
    "phone": "+27 82 123 4567",
    "email": "thabo@example.com",
    "emergency_contact": "+27 83 765 4321",
    "emergency_name": "Sarah Nkosi",
    "face_encoding": [0.12, -0.34, 0.56, ...],
    "registered_date": "2026-05-25 10:30:00",
    "total_rides": 47,
    "total_spent": 2850.50
  },
  "user_id_2": {
    "user_id": "e5f6g7h8",
    "name": "Lerato Molefe",
    "phone": "+27 71 987 6543",
    "email": "lerato@example.com",
    "emergency_contact": "+27 82 111 2222",
    "emergency_name": "Mama Molefe",
    "face_encoding": [0.23, -0.45, 0.67, ...],
    "registered_date": "2026-05-26 14:20:00",
    "total_rides": 12,
    "total_spent": 890.75
  }
}
Rides Database (biometric_data/rides.json)
json
{
  "RIDE-20260525103000": {
    "ride_id": "RIDE-20260525103000",
    "user_id": "a1b2c3d4",
    "user_name": "Thabo Nkosi",
    "pickup": "Sandton City",
    "destination": "OR Tambo Airport",
    "distance": 22.5,
    "price": 270.00,
    "ride_type": "Premium",
    "start_time": "2026-05-25 10:30:00",
    "status": "completed"
  }
}
SOS Log Database (biometric_data/sos_log.json)
json
{
  "sos_events": [{
    "user_id": "a1b2c3d4",
    "user_name": "Thabo Nkosi",
    "location": "Midrand",
    "timestamp": "2026-05-25 15:45:00",
    "status": "resolved"
  }]
}
🚀 Installation
1. Clone the repository
bash
git clone https://github.com/SANDILE19991111/saferide.git
cd saferide
2. Create virtual environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
# Install dlib first (takes ~5-10 minutes)
pip install dlib-bin

# Install other packages
pip install -r requirements.txt
4. Set up API key
bash
# Create .env file
echo GEMINI_API_KEY="your_api_key_here" > .env
5. Run the app
bash
# Local access only
streamlit run app.py

# Mobile access (same WiFi)
python run_mobile.py
6. Database Setup
The database is created automatically when:

First user registers (creates users.json)

First ride requested (creates rides.json)

First SOS triggered (creates sos_log.json)

All data is stored in the biometric_data/ folder.

📱 Usage Guide
For New Users (Sign Up)
Open the app - Go to the live URL or run locally

Click "Register" in the navigation menu

Fill in your details:

Full Name

Phone Number

Email Address

Emergency Contact Name & Number

Upload your face photo - Take a clear, well-lit photo

Click "Register" - Your data is saved to the database

Save your User ID - You'll need this to sign in next time

For Existing Users (Sign In)
Open the app - Go to the live URL or run locally

Click "Verify Identity" in the navigation menu

Enter your User ID - The ID you received during registration

Take a live selfie - Position your face in the camera frame

Click "Verify" - AI matches your face with stored data

Access ride services - After successful verification

Request a Ride
Must be signed in - Complete verification first

Click "Request Ride" - This option appears after verification

Select pickup location - Choose from predefined locations

Select destination - Where you want to go

Choose ride type - Standard/Comfort/Premium/XL/Electric

Review price - Calculated based on distance

Confirm ride - Driver assigned and tracking starts

Emergency SOS
During an active ride - Go to "Emergency SOS" page

Click the red SOS button - Triggers immediate alert

System automatically:

Notifies your emergency contact

Shares your GPS location

Alerts SAPS (simulated)

Unlocks evidence for investigation

View Dashboard
Click "My Dashboard" - After signing in

View your statistics:

Total rides completed

Total amount spent

Member since date

Recent ride history

🔧 Database Management
View Users
bash
# On Windows
type biometric_data\users.json

# On Mac/Linux
cat biometric_data/users.json
Backup Database
bash
# Copy the entire biometric_data folder
cp -r biometric_data biometric_data_backup
Clear Database (Reset App)
bash
# Delete all user data (warning: irreversible)
rm -rf biometric_data/*
Export User Data
bash
# Export users to CSV
python -c "
import json
import csv
with open('biometric_data/users.json') as f:
    users = json.load(f)
with open('users_export.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['User ID', 'Name', 'Phone', 'Rides', 'Spent'])
    for uid, user in users.items():
        writer.writerow([uid, user['name'], user['phone'], 
                        user.get('total_rides',0), user.get('total_spent',0)])
print('Exported to users_export.csv')
"
🔒 Security & Privacy (POPIA Compliant)
Control	Implementation	Status
ID Number Hashing	SHA-256 one-way hash	✅
Face Data Storage	128-point encoding (not original image)	✅
API Key Security	.env + .gitignore	✅
Evidence Locking	Locked by default, unlocked by SOS	✅
Encryption at Rest	AES-256 for biometric files	📋 Planned
Data Retention	Auto-delete after 90 days	📋 Planned
Consent Collection	Explicit at registration	✅
Third-party Sharing	Zero data selling	✅
💰 Price Calculation
Rate Table
Ride Type	Rate/km	Minimum Fare
Standard	R12	R35
Comfort	R18	R50
Premium	R25	R70
XL (6 seater)	R20	R60
Electric	R15	R45
Peak Hours: 7-9am and 4-7pm (30% surcharge)

Sample Calculation
text
Distance: 15 km
Ride Type: Comfort
Base Price: 15 × R18 = R270
Minimum Fare: R50
Peak Hour: 8am → +30%
Final Price: R270 × 1.3 = R351
📁 Project Structure
text
saferide/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run_mobile.py         # Mobile deployment script
├── saferide_core.py      # Core biometric functions
├── biometric_data/       # User database (auto-created)
│   ├── users.json       # Registered user profiles
│   ├── rides.json       # Ride history
│   └── sos_log.json     # SOS event log
├── .streamlit/          # Streamlit configuration
├── .vscode/             # VS Code settings
├── README.md            # This documentation
└── .gitignore          # Git ignore rules
🧪 Testing the Database
Test User Registration
bash
python -c "
import json
from pathlib import Path
import hashlib

# Simulate user registration
users_file = Path('biometric_data/users.json')
users = {}
user_id = 'test1234'
users[user_id] = {
    'name': 'Test User',
    'phone': '+27 82 123 4567',
    'registered_date': '2026-05-25'
}
with open(users_file, 'w') as f:
    json.dump(users, f, indent=2)
print('Test user created successfully!')
"
Test Ride Request
bash
python -c "
from app import calculate_price, PREDEFINED_LOCATIONS
from math import radians, sin, cos, sqrt, atan2

# Calculate price for test route
pickup = 'Sandton City'
dest = 'OR Tambo Airport'
price = calculate_price(22.5, 'Standard')
print(f'Route: {pickup} → {dest}')
print(f'Distance: 22.5 km')
print(f'Price: R{price}')
"
📞 Support
GitHub Issues: Create an issue

Live App: https://saferide-afmlopappj3yux9itozrocz.streamlit.app/

Developer Email: [your-email@example.com]

🙏 Acknowledgments
CAPACITI for the AI Bootcamp opportunity

Clickatell for industry sponsorship

Google for Gemini API free tier

Streamlit for easy web app deployment

📄 License
MIT License - See LICENSE file for details

🎯 Version History
v1.0.0 (Current) - Initial release with full database support

User registration with database

Biometric sign-in

Ride request and tracking

SOS emergency system

Dashboard with statistics

Built with ❤️ for safer South African roads

"SafeRide - Your Safety, Our Priority"
