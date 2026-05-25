"""
SafeRide — Modernised Streamlit UI
New features: Pickup PIN, Trip Sharing, Audio Recording, Women for Women, Route Alerts
"""

import streamlit as st
import json, os, time, datetime, random, string
from pathlib import Path


# Initialize session state
if 'verified' not in st.session_state:
    st.session_state.verified = False
if 'rider_id' not in st.session_state:
    st.session_state.rider_id = None
if 'rider_name' not in st.session_state:
    st.session_state.rider_name = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="SafeRide",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Modern CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
  }

  .block-container {
    padding: 0 1rem 4rem;
    max-width: 500px;
    margin: auto;
  }

  /* ── Top header bar ── */
  .sr-topbar {
    background: linear-gradient(135deg, #0f1b2e 0%, #1a3050 100%);
    border-radius: 0 0 24px 24px;
    padding: 20px 20px 24px;
    margin: -1rem -1rem 1.5rem;
    text-align: center;
    position: relative;
  }
  .sr-topbar-logo {
    font-size: 36px;
    line-height: 1;
    margin-bottom: 4px;
  }
  .sr-topbar-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.3px;
  }
  .sr-topbar-sub {
    font-size: 12px;
    color: #7aafdc;
    margin-top: 2px;
  }
  .sr-topbar-badge {
    position: absolute;
    top: 16px;
    right: 16px;
    background: rgba(29,158,117,0.2);
    border: 1px solid #1D9E75;
    color: #4fd1a5;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
  }

  /* ── Buttons ── */
  div[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 14px;
    font-size: 15px;
    font-weight: 600;
    padding: 13px 0;
    min-height: 50px;
    margin: 4px 0;
    transition: all 0.2s ease;
    border: none;
  }
  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0f1b2e, #1e3a5f);
    color: #fff;
    box-shadow: 0 4px 15px rgba(15,27,46,0.3);
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(15,27,46,0.45);
    transform: translateY(-1px);
  }
  div[data-testid="stButton"] > button[kind="secondary"] {
    background: #f5f7fa;
    color: #1a2d4a;
    border: 1.5px solid #e2e8f0;
  }

  /* ── Inputs ── */
  input, textarea, select {
    font-size: 15px !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #fafbfc !important;
    transition: border-color 0.2s !important;
  }
  input:focus, textarea:focus {
    border-color: #1D9E75 !important;
    box-shadow: 0 0 0 3px rgba(29,158,117,0.1) !important;
  }

  /* ── Cards ── */
  .sr-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 18px;
    border: 1.5px solid #eef0f3;
    margin: 10px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  }
  .sr-card-dark {
    background: #0f1b2e;
    border-radius: 18px;
    padding: 18px;
    margin: 10px 0;
  }

  /* ── Status banners ── */
  .sr-verified {
    background: linear-gradient(135deg, #e8f8f1, #d1f5e4);
    border-left: 4px solid #1D9E75;
    border-radius: 0 16px 16px 0;
    padding: 16px 18px;
    margin: 12px 0;
  }
  .sr-failed {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border-left: 4px solid #ef4444;
    border-radius: 0 16px 16px 0;
    padding: 16px 18px;
    margin: 12px 0;
  }
  .sr-info {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border-left: 4px solid #3b82f6;
    border-radius: 0 14px 14px 0;
    padding: 14px 16px;
    margin: 10px 0;
    font-size: 13px;
    color: #1e40af;
  }
  .sr-warning {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border-left: 4px solid #f59e0b;
    border-radius: 0 14px 14px 0;
    padding: 14px 16px;
    margin: 10px 0;
    font-size: 13px;
    color: #92400e;
  }

  /* ── Rider ID box ── */
  .sr-rider-id {
    font-family: 'Courier New', monospace;
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 6px;
    color: #0f1b2e;
    background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
    border: 2px dashed #c7d2fe;
  }

  /* ── PIN display ── */
  .sr-pin {
    font-family: 'Courier New', monospace;
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 12px;
    color: #0f1b2e;
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    border: 2px solid #86efac;
  }

  /* ── Badges ── */
  .sr-badge {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px 2px;
  }
  .sr-badge-green { background: #dcfce7; color: #15803d; }
  .sr-badge-blue  { background: #dbeafe; color: #1d4ed8; }
  .sr-badge-red   { background: #fee2e2; color: #b91c1c; }
  .sr-badge-amber { background: #fef3c7; color: #92400e; }
  .sr-badge-purple{ background: #ede9fe; color: #6d28d9; }

  /* ── Feature cards ── */
  .sr-feat {
    background: #fff;
    border: 1.5px solid #eef0f3;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
  }
  .sr-feat-icon {
    font-size: 24px;
    margin-bottom: 6px;
    display: block;
  }
  .sr-feat-title {
    font-size: 14px;
    font-weight: 600;
    color: #0f1b2e;
  }
  .sr-feat-desc {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
    line-height: 1.4;
  }

  /* ── Toggle switch ── */
  .sr-toggle-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
  }
  .sr-toggle-row:last-child { border-bottom: none; }
  .sr-toggle-label { font-size: 13px; font-weight: 500; color: #1e293b; }
  .sr-toggle-desc  { font-size: 11px; color: #94a3b8; margin-top: 1px; }

  /* ── Trip row ── */
  .sr-trip-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
  }
  .sr-trip-row:last-child { border-bottom: none; }

  /* ── Section titles ── */
  .sr-section {
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 20px 0 10px;
  }

  /* ── Metric grid ── */
  .sr-metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 12px 0;
  }
  .sr-metric {
    background: #f8fafc;
    border-radius: 14px;
    padding: 12px;
    text-align: center;
    border: 1.5px solid #eef0f3;
  }
  .sr-metric-val { font-size: 24px; font-weight: 700; color: #0f1b2e; }
  .sr-metric-lbl { font-size: 11px; color: #64748b; margin-top: 2px; }

  /* ── SOS button ── */
  .sr-sos {
    background: linear-gradient(135deg, #dc2626, #991b1b);
    color: #fff;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(220,38,38,0.4);
    margin: 10px 0;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 4px 20px rgba(220,38,38,0.4); }
    50%       { box-shadow: 0 4px 30px rgba(220,38,38,0.7); }
  }

  /* ── Progress bar ── */
  .sr-progress-track {
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    margin: 10px 0 16px;
    overflow: hidden;
  }

  /* ── Avatar circle ── */
  .sr-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    flex-shrink: 0;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }

  /* Selectbox nav pill */
  div[data-testid="stSelectbox"] > div > div {
    border-radius: 14px !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #fff !important;
    font-weight: 500 !important;
  }

  /* Expander */
  details { border-radius: 14px !important; border: 1.5px solid #eef0f3 !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

  /* Divider */
  hr { border-color: #f1f5f9; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Import core ────────────────────────────────────────────────────────────────
try:
    from saferide_core import (
        register_rider, verify_rider, register_driver, trigger_sos,
        load_db, RIDERS_DB, DRIVERS_DB, TRIPS_DB, EVIDENCE_DIR,
        DATA_DIR, PHOTOS_DIR
    )
    CORE_OK = True
except ImportError as e:
    CORE_OK = False
    IMPORT_ERR = str(e)

# ── Helper: generate pickup PIN ────────────────────────────────────────────────
def generate_pin():
    return str(random.randint(1000, 9999))

# ── Helper: save safety prefs per rider ───────────────────────────────────────
PREFS_FILE = Path("saferide_data/safety_prefs.json")

def load_prefs():
    if PREFS_FILE.exists():
        with open(PREFS_FILE) as f:
            return json.load(f)
    return {}

def save_prefs(data):
    PREFS_FILE.parent.mkdir(exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_rider_prefs(rider_id):
    prefs = load_prefs()
    return prefs.get(rider_id, {
        "trip_sharing": True,
        "share_contact": "",
        "audio_recording": False,
        "women_for_women": False,
        "route_alerts": True,
        "alert_contact": "",
    })

def set_rider_prefs(rider_id, new_prefs):
    prefs = load_prefs()
    prefs[rider_id] = new_prefs
    save_prefs(prefs)

# ── Top bar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sr-topbar">
  <div class="sr-topbar-badge">🟢 System online</div>
  <div class="sr-topbar-logo">🛡️</div>
  <div class="sr-topbar-title">SafeRide</div>
  <div class="sr-topbar-sub">Biometric · AI · Encrypted</div>
</div>
""", unsafe_allow_html=True)

# ── Navigation ─────────────────────────────────────────────────────────────────
page = st.selectbox("Navigate", [
    "🏠  Home",
    "👤  Register Rider",
    "🔐  Verify for Ride",
    "🚗  Request Ride",
    "🚘  Safety Settings",
    "🚗  Driver Dashboard",
    "📡  Surveillance Server",
    "⚙️  Settings",
], label_visibility="collapsed")

st.divider()

if not CORE_OK and page not in ["⚙️  Settings", "🏠  Home"]:
    st.error(f"Missing packages. Run:\n```\npip install -r requirements.txt\n```\nError: {IMPORT_ERR}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    if CORE_OK:
        riders = load_db(RIDERS_DB)
        trips  = load_db(TRIPS_DB)
        sos_count = sum(1 for t in trips.values() if t.get("sos_triggered"))
        st.markdown('<div class="sr-metric-grid">'
            f'<div class="sr-metric"><div class="sr-metric-val">{len(riders)}</div><div class="sr-metric-lbl">Riders</div></div>'
            f'<div class="sr-metric"><div class="sr-metric-val">{len(trips)}</div><div class="sr-metric-lbl">Trips</div></div>'
            f'<div class="sr-metric"><div class="sr-metric-val" style="color:#1D9E75">AI</div><div class="sr-metric-lbl">Gemini</div></div>'
            '</div>', unsafe_allow_html=True)

    st.markdown('<div class="sr-section">How it works</div>', unsafe_allow_html=True)

    steps = [
        ("📋", "Register once", "Upload SA ID + selfie. Face & fingerprint enrolled securely."),
        ("🤳", "Verify every ride", "Live biometric check before driver is assigned."),
        ("🔢", "Get your pickup PIN", "4-digit code confirms you're in the right vehicle."),
        ("🚗", "Driver gets AI report", "Gemini writes a verified safety briefing automatically."),
        ("📍", "Trip shared live", "Trusted contact tracks your ride in real time."),
        ("🎙️", "Audio protection", "Discreet in-app recording if you feel unsafe."),
        ("🆘", "SOS one tap", "Alerts SAPS + security with full trip evidence."),
    ]
    for emoji, title, desc in steps:
        st.markdown(f'''
        <div class="sr-feat">
          <span class="sr-feat-icon">{emoji}</span>
          <div class="sr-feat-title">{title}</div>
          <div class="sr-feat-desc">{desc}</div>
        </div>''', unsafe_allow_html=True)

    st.markdown('<div class="sr-info">📱 Use the dropdown above to navigate between sections.</div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# REGISTER RIDER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👤  Register Rider":
    st.markdown("### 👤 Register Rider")
    st.markdown('<div class="sr-info">One-time setup. You\'ll need your SA ID document photo and a selfie.</div>',
                unsafe_allow_html=True)

    name      = st.text_input("Full name (as on SA ID)")
    phone     = st.text_input("Phone number", placeholder="+27 82 000 0000")
    id_number = st.text_input("SA ID number (13 digits)", placeholder="9001015009087")

    # Women for Women opt-in at registration
    women_for_women = st.checkbox("🚺 Enable Women for Women — match me only with female drivers")

    st.markdown("**📄 Upload ID document photo**")
    id_photo = st.camera_input("Take photo of your ID") or st.file_uploader(
        "Or upload from gallery", type=["jpg","jpeg","png"], key="id_upload"
    )

    st.markdown("**🤳 Take a live selfie**")
    selfie = st.camera_input("Take selfie now") or st.file_uploader(
        "Or upload selfie", type=["jpg","jpeg","png"], key="selfie_upload"
    )

    if id_photo:
        st.image(id_photo, caption="ID photo ✓", width=200)
    if selfie:
        st.image(selfie, caption="Selfie ✓", width=200)

    if st.button("✅ Register & Enroll Biometrics", type="primary"):
        if not all([name, phone, id_number, id_photo]):
            st.error("Please fill in all fields and provide your ID photo.")
        elif len(id_number.replace(" ", "")) != 13:
            st.error("SA ID number must be exactly 13 digits.")
        else:
            DATA_DIR.mkdir(exist_ok=True)
            PHOTOS_DIR.mkdir(exist_ok=True)

            id_path = str(PHOTOS_DIR / f"id_{name.replace(' ','_')}.jpg")
            with open(id_path, "wb") as f:
                f.write(id_photo.getvalue() if hasattr(id_photo,'getvalue') else id_photo.read())

            selfie_path = None
            if selfie:
                selfie_path = str(PHOTOS_DIR / f"selfie_{name.replace(' ','_')}.jpg")
                with open(selfie_path, "wb") as f:
                    f.write(selfie.getvalue() if hasattr(selfie,'getvalue') else selfie.read())

            with st.spinner("Enrolling biometrics..."):
                result = register_rider(name, phone, id_number, id_path, selfie_path)

            if result["success"]:
                rid = result["rider_id"]
                # Save default prefs with Women for Women setting
                prefs = get_rider_prefs(rid)
                prefs["women_for_women"] = women_for_women
                set_rider_prefs(rid, prefs)

                st.balloons()
                st.markdown('<div class="sr-verified"><b>✅ Registration complete!</b><br>Save your Rider ID below — you need it every ride.</div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="sr-rider-id">{rid}</div>', unsafe_allow_html=True)
                badges = '<span class="sr-badge sr-badge-green">Face enrolled ✓</span>'
                badges += '<span class="sr-badge sr-badge-green">Fingerprint ✓</span>'
                badges += '<span class="sr-badge sr-badge-blue">ID verified ✓</span>'
                if women_for_women:
                    badges += '<span class="sr-badge sr-badge-purple">Women for Women ✓</span>'
                st.markdown(badges, unsafe_allow_html=True)
                st.info("📸 Screenshot your Rider ID — you'll need it to verify for every ride.")
                st.markdown('<div class="sr-section">Next step</div>', unsafe_allow_html=True)
                st.markdown('<div class="sr-warning">⚙️ Head to <b>Safety Settings</b> to configure trip sharing, audio recording, and route alerts.</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="sr-failed"><b>❌ Registration failed</b><br>{result["error"]}</div>',
                            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VERIFY FOR RIDE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔐  Verify for Ride":
    st.markdown("### 🔐 Verify for Ride")
    st.markdown('<div class="sr-info">Required <b>every ride</b>. Face + fingerprint must both match.</div>',
                unsafe_allow_html=True)

    rider_id    = st.text_input("Your Rider ID", placeholder="e.g. A1B2C3D4").strip().upper()
    driver_name = st.text_input("Driver name", placeholder="Moses Khumalo")

    st.markdown("**🤳 Verification selfie**")
    selfie_cam = st.camera_input("Look straight at camera and tap") or st.file_uploader(
        "Or upload selfie", type=["jpg","jpeg","png"], key="verify_selfie"
    )
    if selfie_cam:
        st.image(selfie_cam, caption="Selfie captured ✓", width=180)

    if st.button("🔐 Verify My Identity", type="primary"):
        if not rider_id:
            st.error("Enter your Rider ID.")
        elif not selfie_cam:
            st.error("Take a selfie to verify.")
        else:
            DATA_DIR.mkdir(exist_ok=True)
            selfie_path = str(DATA_DIR / f"verify_{rider_id}_{int(time.time())}.jpg")
            with open(selfie_path, "wb") as f:
                f.write(selfie_cam.getvalue() if hasattr(selfie_cam,'getvalue') else selfie_cam.read())

            with st.spinner("Verifying identity..."):
                bar = st.progress(0)
                time.sleep(0.4); bar.progress(20, "Detecting face...")
                time.sleep(0.5); bar.progress(45, "Matching biometric profile...")
                time.sleep(0.5); bar.progress(70, "Fingerprint check...")
                time.sleep(0.4); bar.progress(90, "Generating AI safety report...")
                report = verify_rider(rider_id, live_selfie_path=selfie_path,
                                      use_webcam=False,
                                      driver_name=driver_name or "Driver")
                bar.progress(100, "Done.")

            if report.get("verified"):
                st.balloons()
                
                # Set session state for ride request
                st.session_state.verified = True
                st.session_state.rider_id = rider_id
                st.session_state.rider_name = report.get("rider_name", "Rider")

                # Generate pickup PIN
                pin = generate_pin()

                # Save PIN to trip record
                trips = load_db(TRIPS_DB)
                if report.get("trip_id") and report["trip_id"] in trips:
                    trips[report["trip_id"]]["pickup_pin"] = pin
                    from saferide_core import save_db
                    save_db(TRIPS_DB, trips)

                # Load rider prefs
                prefs = get_rider_prefs(rider_id)

                st.markdown(f'<div class="sr-verified"><b>✅ Identity Verified — {report["rider_name"]}</b><br>Details sent to driver automatically.</div>',
                            unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                col1.metric("Face match", f"{report['face_confidence']}%")
                col2.metric("Fingerprint", f"{report['fp_confidence']}%")

                # ── Pickup PIN ──
                st.markdown('<div class="sr-section">🔢 Your pickup PIN</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sr-pin">{pin}</div>', unsafe_allow_html=True)
                st.markdown('<div class="sr-warning">Show this to your driver to confirm pickup. Do not read it aloud — let them see your screen.</div>',
                            unsafe_allow_html=True)

                # ── AI report ──
                if report.get("ai_driver_report"):
                    st.markdown('<div class="sr-section">🤖 AI report sent to driver</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="sr-info">{report["ai_driver_report"]}</div>',
                                unsafe_allow_html=True)

                # ── Active safety features ──
                active = []
                if prefs.get("trip_sharing"):
                    contact = prefs.get("share_contact","your contact")
                    active.append(f'<span class="sr-badge sr-badge-blue">📍 Sharing with {contact or "contact"}</span>')
                if prefs.get("audio_recording"):
                    active.append('<span class="sr-badge sr-badge-purple">🎙️ Audio protection on</span>')
                if prefs.get("route_alerts"):
                    active.append('<span class="sr-badge sr-badge-amber">🗺️ Route monitoring on</span>')
                if prefs.get("women_for_women"):
                    active.append('<span class="sr-badge sr-badge-purple">🚺 Women for Women</span>')

                if active:
                    st.markdown('<div class="sr-section">Active safety features</div>', unsafe_allow_html=True)
                    st.markdown(" ".join(active), unsafe_allow_html=True)

                st.caption(f"Trip: `{report['trip_id']}`")
            else:
                st.markdown(f'<div class="sr-failed"><b>❌ Verification Failed</b><br>{report.get("reason","Biometric mismatch.")}</div>',
                            unsafe_allow_html=True)
                st.error("Ride blocked. Contact SafeRide support.")

# ══════════════════════════════════════════════════════════════════════════════
# REQUEST RIDE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚗  Request Ride":
    st.markdown("### 🚗 Request a Ride")
    
    if not st.session_state.verified:
        st.warning("⚠️ Please verify your identity first.")
        st.info("Go to **Verify for Ride** and complete verification before requesting a ride.")
        st.stop()
    
    st.success(f"✅ Verified as: {st.session_state.get('rider_name', 'Rider')}")
    
    col1, col2 = st.columns(2)
    with col1:
        pickup = st.text_input("📍 Pickup location", placeholder="Enter your current address")
    with col2:
        destination = st.text_input("🎯 Destination", placeholder="Where are you going?")
    
    ride_type = st.radio(
        "Ride type",
        ["🚗 Standard", "👩 Women for Women", "⭐ Premium"],
        horizontal=True
    )
    
    if st.button("🚀 Request Ride Now", type="primary"):
        if pickup and destination:
            ride_id = f"RIDE-{random.randint(10000, 99999)}"
            st.balloons()
            st.success(f"✅ Ride requested successfully!")
            st.markdown(f"""
            <div class='sr-card'>
                <b>Ride ID:</b> {ride_id}<br>
                <b>Driver:</b> Thabo Molefe<br>
                <b>Vehicle:</b> Toyota Corolla (ABC-123-GP)<br>
                <b>ETA:</b> 5-7 minutes<br>
                <b>Estimated fare:</b> R65 - R85<br>
                <b>Status:</b> Driver assigned ✅
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📍 Live Tracking")
            st.map({"lat": [-26.2041], "lon": [28.0473]})
            st.info("📱 Your trip is being shared with your emergency contact")
        else:
            st.error("Please enter both pickup location and destination")

# ══════════════════════════════════════════════════════════════════════════════
# SAFETY SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚘  Safety Settings":
    st.markdown("### 🚘 Safety Settings")
    st.markdown('<div class="sr-info">Configure your personal safety features. Settings are saved per Rider ID.</div>',
                unsafe_allow_html=True)

    rider_id = st.text_input("Your Rider ID", placeholder="e.g. A1B2C3D4").strip().upper()

    if not rider_id:
        st.info("Enter your Rider ID above to load your settings.")
        st.stop()

    if CORE_OK:
        riders = load_db(RIDERS_DB)
        if rider_id not in riders:
            st.error("Rider ID not found. Please register first.")
            st.stop()
        rider_name = riders[rider_id]["name"]
        st.markdown(f'<div class="sr-card"><b>👤 {rider_name}</b> &nbsp; <span class="sr-badge sr-badge-green">Active</span></div>',
                    unsafe_allow_html=True)

    prefs = get_rider_prefs(rider_id)

    # ── 1. Trip Sharing ──────────────────────────────────────────────────────
    st.markdown('<div class="sr-section">📍 Trip Sharing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sr-card">', unsafe_allow_html=True)
    trip_sharing = st.toggle("Share my live trip with a trusted contact",
                             value=prefs.get("trip_sharing", True),
                             key="ts_toggle")
    if trip_sharing:
        share_contact = st.text_input("Contact name or phone number",
                                      value=prefs.get("share_contact",""),
                                      placeholder="+27 82 000 0000 or Mom",
                                      key="ts_contact")
        st.markdown('<div class="sr-info" style="font-size:12px">Your contact will receive your live location, vehicle registration, and driver details for every ride.</div>',
                    unsafe_allow_html=True)
    else:
        share_contact = prefs.get("share_contact","")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 2. Audio Recording ───────────────────────────────────────────────────
    st.markdown('<div class="sr-section">🎙️ Audio Recording</div>', unsafe_allow_html=True)
    st.markdown('<div class="sr-card">', unsafe_allow_html=True)
    audio_rec = st.toggle("Enable discreet audio recording during rides",
                          value=prefs.get("audio_recording", False),
                          key="ar_toggle")
    if audio_rec:
        st.markdown('<div class="sr-warning" style="font-size:12px">🎙️ Recording activates automatically when you feel uncomfortable. Audio is encrypted and only sent to the SafeRide safety team if you trigger SOS or report an incident.</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 3. Women for Women ───────────────────────────────────────────────────
    st.markdown('<div class="sr-section">🚺 Women for Women</div>', unsafe_allow_html=True)
    st.markdown('<div class="sr-card">', unsafe_allow_html=True)
    w4w = st.toggle("Only match me with female drivers",
                    value=prefs.get("women_for_women", False),
                    key="w4w_toggle")
    if w4w:
        st.markdown('<div class="sr-info" style="font-size:12px">🚺 When enabled, your ride requests will only be matched to verified female drivers. This may increase wait times slightly.</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 4. Route Anomaly Alerts ──────────────────────────────────────────────
    st.markdown('<div class="sr-section">🗺️ Route Anomaly Alerts</div>
                # ══════════════════════════════════════════════════════════════════════════════
# SAFETY SETTINGS (continued)
# ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sr-card">', unsafe_allow_html=True)
    route_alerts = st.toggle("Alert my contact on unexpected stops or detours",
                             value=prefs.get("route_alerts", True),
                             key="ra_toggle")
    if route_alerts:
        alert_contact = st.text_input("Alert contact (can be same as trip sharing)",
                                      value=prefs.get("alert_contact",""),
                                      placeholder="+27 82 000 0000",
                                      key="ra_contact")
        st.markdown('<div class="sr-warning" style="font-size:12px">⚠️ Triggers if your driver stops unexpectedly for more than 3 minutes or deviates significantly from the route.</div>',
                    unsafe_allow_html=True)
    else:
        alert_contact = prefs.get("alert_contact","")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Save ─────────────────────────────────────────────────────────────────
    if st.button("💾 Save Safety Settings", type="primary"):
        new_prefs = {
            "trip_sharing":    trip_sharing,
            "share_contact":   share_contact if trip_sharing else prefs.get("share_contact",""),
            "audio_recording": audio_rec,
            "women_for_women": w4w,
            "route_alerts":    route_alerts,
            "alert_contact":   alert_contact if route_alerts else prefs.get("alert_contact",""),
        }
        set_rider_prefs(rider_id, new_prefs)
        st.success("✅ Safety settings saved!")

        summary = []
        if trip_sharing: summary.append("📍 Trip sharing")
        if audio_rec:    summary.append("🎙️ Audio recording")
        if w4w:          summary.append("🚺 Women for Women")
        if route_alerts: summary.append("🗺️ Route alerts")
        if summary:
            badges = "".join(f'<span class="sr-badge sr-badge-green">{s}</span>' for s in summary)
            st.markdown(f"<b>Active features:</b><br>{badges}", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DRIVER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚗  Driver Dashboard":
    st.markdown("### 🚗 Driver Dashboard")
    st.markdown('<div class="sr-info">Passenger verification reports — drivers only.</div>',
                unsafe_allow_html=True)

    trips = load_db(TRIPS_DB) if CORE_OK else {}

    if not trips:
        st.info("No trips yet. A rider must verify first.")
    else:
        recent = sorted(trips.values(), key=lambda x: x["timestamp"], reverse=True)[:10]
        for t in recent:
            icon = "✅" if t["verified"] else "❌"
            sos  = " 🆘" if t.get("sos_triggered") else ""
            pin  = t.get("pickup_pin","—")
            with st.expander(f"{icon} {t['rider_name']}{sos}  ·  {str(t['timestamp'])[:16]}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Face", f"{t['face_confidence']}%")
                c2.metric("Fingerprint", f"{t['fp_confidence']}%")
                c3.metric("Pickup PIN", pin)

                # Show Women for Women flag if applicable
                prefs = get_rider_prefs(t.get("rider_id",""))
                if prefs.get("women_for_women"):
                    st.markdown('<span class="sr-badge sr-badge-purple">🚺 Women for Women rider</span>',
                                unsafe_allow_html=True)

                if t.get("ai_driver_report"):
                    st.markdown(f'<div class="sr-info">🤖 {t["ai_driver_report"]}</div>',
                                unsafe_allow_html=True)

                if t["verified"]:
                    st.markdown(f'<div class="sr-warning">🔢 Ask the rider to show PIN: <b>{pin}</b> — do not ask them to read it aloud.</div>',
                                unsafe_allow_html=True)
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ Confirm pickup", key=f"c_{t['trip_id']}"):
                            st.success("Pickup confirmed!")
                    with col_b:
                        if st.button("⚠️ Flag mismatch", key=f"f_{t['trip_id']}"):
                            st.error("Flagged. Ops notified.")
                else:
                    st.error("❌ DO NOT pick up this passenger — verification failed.")

    st.divider()
    st.markdown('<div class="sr-section">Driver registration</div>', unsafe_allow_html=True)
    with st.expander("Register as a driver"):
        d_name  = st.text_input("Full name", key="dn")
        d_phone = st.text_input("Phone", key="dp")
        d_lic   = st.text_input("License number", key="dl")
        d_vreg  = st.text_input("Vehicle registration", key="dv")
        d_gender= st.selectbox("Gender", ["Male", "Female", "Prefer not to say"], key="dg")
        d_photo = st.camera_input("Driver photo") or st.file_uploader(
            "Upload photo", type=["jpg","jpeg","png"], key="dph"
        )
        if st.button("Register Driver", type="primary", key="dreg"):
            if d_photo and d_name and d_phone and d_lic and d_vreg:
                PHOTOS_DIR.mkdir(exist_ok=True)
                pp = str(PHOTOS_DIR / f"driver_{d_name.replace(' ','_')}.jpg")
                with open(pp, "wb") as f:
                    f.write(d_photo.getvalue() if hasattr(d_photo,'getvalue') else d_photo.read())
                res = register_driver(d_name, d_phone, d_lic, d_vreg, pp)
                if res["success"]:
                    st.success(f"Driver registered! ID: `{res['driver_id']}`")
                    if d_gender == "Female":
                        st.markdown('<span class="sr-badge sr-badge-purple">🚺 Eligible for Women for Women rides</span>',
                                    unsafe_allow_html=True)
                else:
                    st.error(res["error"])
            else:
                st.warning("Fill in all fields and provide a photo.")

# ══════════════════════════════════════════════════════════════════════════════
# SURVEILLANCE SERVER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📡  Surveillance Server":
    st.markdown("### 📡 Surveillance Server")
    st.caption("AES-256 encrypted · POPIA compliant · 90-day retention")

    trips   = load_db(TRIPS_DB)
    riders  = load_db(RIDERS_DB)
    drivers = load_db(DRIVERS_DB)
    sos_count = sum(1 for t in trips.values() if t.get("sos_triggered"))

    st.markdown(f'<div class="sr-metric-grid">'
        f'<div class="sr-metric"><div class="sr-metric-val">{len(trips)}</div><div class="sr-metric-lbl">Trips</div></div>'
        f'<div class="sr-metric"><div class="sr-metric-val">{len(riders)}</div><div class="sr-metric-lbl">Riders</div></div>'
        f'<div class="sr-metric"><div class="sr-metric-val" style="color:#dc2626">{sos_count}</div><div class="sr-metric-lbl">SOS</div></div>'
        '</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔒 Evidence", "📋 Records", "🆘 SOS"])

    with tab1:
        st.markdown("**Evidence Vault** — locked by default")
        ev_files = sorted(EVIDENCE_DIR.glob("*.json"), reverse=True) if EVIDENCE_DIR.exists() else []
        if not ev_files:
            st.info("No evidence yet.")
        for ef in ev_files[:15]:
            with open(ef) as f: ev = json.load(f)
            locked = ev.get("evidence_locked", True)
            sos    = ev.get("sos_triggered", False)
            icon   = "🔴" if sos else ("🔒" if locked else "🔓")
            status = "✅" if ev["verified"] else "❌"
            pin    = ev.get("pickup_pin","—")
            st.markdown(f'<div class="sr-card" style="font-size:13px;">'
                f'<b>{icon} {ev["trip_id"]}</b> · {ev["rider_name"]}<br>'
                f'{str(ev["timestamp"])[:16]} · Face {ev["face_confidence"]}% · FP {ev["fp_confidence"]}% · PIN {pin} · {status}'
                '</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("**All trip records**")
        if not trips:
            st.info("No trips yet.")
        else:
            rows = [{"Trip": t["trip_id"], "Rider": t["rider_name"],
                     "Time": str(t["timestamp"])[:16],
                     "Face%": t["face_confidence"], "FP%": t["fp_confidence"],
                     "PIN": t.get("pickup_pin","—"),
                     "OK": "✅" if t["verified"] else "❌",
                     "SOS": "🆘" if t.get("sos_triggered") else "—"}
                    for t in sorted(trips.values(), key=lambda x: x["timestamp"], reverse=True)]
            st.dataframe(rows, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("**Emergency SOS**")
        st.markdown('<div class="sr-failed">Only use in a genuine emergency. SAPS will be notified immediately.</div>',
                    unsafe_allow_html=True)
        trip_ids = list(trips.keys())
        if trip_ids:
            sos_trip = st.selectbox("Select your trip", trip_ids)
            sos_gps  = st.text_input("Your GPS coordinates (optional)", placeholder="-26.2041, 28.0473")
            st.markdown('<div class="sr-sos">🆘 EMERGENCY SOS</div>', unsafe_allow_html=True)
            if st.button("🆘 TRIGGER SOS NOW", type="primary"):
                res = trigger_sos(sos_trip, gps=sos_gps or "Not provided")
                if res["success"]:
                    st.error("🆘 SOS TRIGGERED. Evidence unlocked. SAPS + private security notified.")
                    st.markdown('<div class="sr-failed"><b>What happens now:</b><br>'
                                '• SAPS have been alerted with your trip evidence<br>'
                                '• Private security dispatched to your last GPS<br>'
                                '• Your trip-sharing contact has been notified<br>'
                                '• Evidence vault unlocked for law enforcement</div>',
                                unsafe_allow_html=True)
                else:
                    st.warning(res.get("error"))
        else:
            st.info("No trips to select.")

# ══════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️  Settings":
    st.markdown("### ⚙️ Settings")

    st.markdown('<div class="sr-section">Gemini API Key</div>', unsafe_allow_html=True)
    current_key = os.environ.get("GEMINI_API_KEY", "")
    if current_key:
        st.success(f"✅ Key loaded: {current_key[:8]}...")
    else:
        st.warning("⚠️ No API key set. AI reports will use fallback text.")

    st.markdown('<div class="sr-info">Get your FREE key at:<br><b>aistudio.google.com/app/apikey</b><br>No credit card needed.</div>',
                unsafe_allow_html=True)
    st.markdown("Add to your `.env` file:")
    st.code("GEMINI_API_KEY=your_key_here")

    st.divider()
    st.markdown('<div class="sr-section">Mobile access</div>', unsafe_allow_html=True)
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        st.markdown(f'<div class="sr-info">📱 Open on your phone:<br><b>http://{ip}:8501</b><br>Same WiFi required.</div>',
                    unsafe_allow_html=True)
        st.code(f"http://{ip}:8501")
    except:
        st.info("Could not detect local IP.")

    st.divider()
    st.markdown('<div class="sr-section">Data management</div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear trip records"):
        if CORE_OK:
            if TRIPS_DB.exists(): TRIPS_DB.unlink()
            for f in EVIDENCE_DIR.glob("*.json"): f.unlink()
        st.success("Trips cleared.")
    if st.button("⚠️ Factory reset — delete ALL data"):
        if CORE_OK:
            for db in [RIDERS_DB, DRIVERS_DB, TRIPS_DB]:
                if db.exists(): db.unlink()
            if PREFS_FILE.exists(): PREFS_FILE.unlink()
            for folder in [EVIDENCE_DIR, PHOTOS_DIR]:
                if folder.exists():
                    for f in folder.glob("*"): f.unlink()
        st.success("All data deleted.")