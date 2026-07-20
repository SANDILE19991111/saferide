# SafeRide – Face Recognition for Ride-Hailing Safety

**Live app:** https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app  
**Code:** https://github.com/SANDILE19991111/saferide

---

## The Problem

Uber and Bolt verify drivers thoroughly. Passengers? Anyone with a phone can book a ride. Fake name, stolen account, no questions asked.

That's a real risk for drivers. So I flipped the script: **verify your face before you get a driver.** No match? No ride.

---

## What Works Now

- **Sign up** – Upload a face photo, receive a User ID
- **Sign in** – Take a live selfie, AI matches your face
- **Request a ride** – Pick pickup/dropoff, get real pricing (R12-R25/km, peak hour surcharge)
- **SOS button** – Big red button. One tap logs your location
- **Dashboard** – View ride history and emergency contacts
- **AI safety report** – Gemini generates a quick briefing (free tier)

**Demo vs Real mode** (toggle in sidebar):
- Demo = fake responses (good for testing)
- Real = actual DeepFace + Gemini API calls

---

## Issues I Hit & Fixed

| Problem | Solution |
|---------|----------|
| Face recognition wouldn't install on Windows | Switched from FaceNet to DeepFace |
| API key committed to GitHub (rookie mistake) | Revoked it, moved to Streamlit Secrets |
| Buttons clicked but nothing happened | Added `st.rerun()` to trigger updates |
| App crashed on Streamlit Cloud | Added `libgl1-mesa-dri` to packages.yml |
| Bad lighting breaks face match | Show confidence score so users know to retry |

---

## Local Setup

```bash
git clone https://github.com/SANDILE19991111/saferide.git
cd saferide
pip install -r requirements.txt
streamlit run app.py
```

For real mode, add API keys to `.env`:

```
GEMINI_API_KEY=your_key
SAPS_API_KEY=your_key  # optional
```

---

## Next Steps

- Connect to SAPS API (waiting on their side)
- Build a native mobile app (Streamlit on phone is functional but clunky)
- Pitch to Bolt for a pilot program

---

## Tech Stack

Streamlit · DeepFace · Gemini 2.5 Flash · Python

---

**SafeRide – drivers deserve to know who's in their car.**
