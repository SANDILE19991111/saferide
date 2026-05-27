Here's the shortened, human-sounding README:

---

# SafeRide – Face Recognition for Ride-Hailing Safety

**Live app:** https://saferide-rrwv43c8efmxhtbmu2xgjr.streamlit.app  
**Code:** https://github.com/SANDILE19991111/saferide

---

## Why I built this

Uber and Bolt check drivers thoroughly. Passengers? Anyone with a phone can book a ride. Fake name? Fine. Stolen account? No problem.

That's scary for drivers. So I flipped it: **verify your face before you get a driver.** No match? No ride.

---

## What works right now

- **Sign up** – Upload a face photo, get a User ID
- **Sign in** – Take a live selfie, AI matches your face
- **Request a ride** – Pick pickup/dropoff, get a real price (R12-R25/km, extra during peak hours)
- **SOS button** – Big red button. One tap logs your location
- **Dashboard** – See your ride history and emergency contacts
- **AI safety report** – Gemini gives you a quick briefing (free tier)

**Demo vs Real mode toggle in sidebar:**
- Demo mode = fake responses (good for testing)
- Real mode = actual DeepFace + Gemini API calls

---

## Problems I hit

| Issue | Fix |
|-------|-----|
| Face recognition wouldn't install on Windows | Switched to DeepFace |
| API key committed to GitHub (dumb) | Revoked it, moved to Secrets |
| Buttons clicked but nothing happened | Added `st.rerun()` |
| App crashed on Streamlit Cloud | Added `libgl1-mesa-dri` to packages |
| Bad lighting breaks face match | Show confidence score so users know to retry |

---

## Run it locally

```bash
git clone https://github.com/SANDILE19991111/saferide.git
cd saferide
pip install -r requirements.txt
streamlit run app.py
```

Add your API keys to `.env` for real mode:

```
GEMINI_API_KEY=your_key
SAPS_API_KEY=your_key  # if you have one
```

---

## What's next

- Actually connect to SAPS API (waiting on them)
- Build a real mobile app (Streamlit on phone is okay but clunky)
- Pitch to Bolt for a pilot

---

## Built with

Streamlit, DeepFace, Gemini 2.5 Flash, Python

---

**SafeRide – drivers should know who's in their car.**

---

That's it. Short, real, no corporate fluff.
