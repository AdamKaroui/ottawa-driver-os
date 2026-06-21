import os
import time
from datetime import datetime
import streamlit as st

# =====================================================================
# 1. STREAMLIT FRONTEND & THEME CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Driver OS Split-Shift", page_icon="📈", layout="centered")

st.title("📈 Driver OS: Split-Shift Matrix")
st.subheader("Ottawa Strategic Local Engine Tracker")

current_location = st.selectbox(
    "Select Current Location Cell:", 
    ["Barrhaven", "Kanata North", "Downtown Core", "Orléans", "YOW Airport", "Gatineau"]
)

st.divider()

# =====================================================================
# 2. LOCAL LOGIC MATRIX (Free, 0ms Latency, Bypasses Network Blocks)
# =====================================================================
if st.button("Generate Current Phase Optimization", type="primary"):
    
    # Get local current time object parameters
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    time_str = now.strftime("%I:%M %p")
    
    # Initialize default fallbacks for off-shift periods
    shift_phase = "Mid-Day Downtime / Maintenance"
    directive = "Keep vehicle parked at home. Avoid burning unnecessary energy assets."
    target_hub = "Barrhaven Level 2 Hub Base"
    reasoning = "You are currently outside your peak split-shift parameters. Conserve energy for the next rush."
    
    # --- PHASE 1: MORNING SPLIT-SHIFT (04:30 AM to 10:30 AM) ---
    if (current_hour == 4 and current_minute >= 30) or (5 <= current_hour <= 6):
        shift_phase = "Morning Block: Early Airport Rush"
        directive = "Prioritize premium Comfort / Comfort Electric airport runs. Ignore mileage parameters due to Weeve subscription terms."
        target_hub = "YOW Airport / Commuter Corridors"
        reasoning = f"It is {time_str}. Early corporate travelers are departing from residential grids like {current_location} toward early business flights."
        
    elif 7 <= current_hour <= 10:
        if current_hour == 10 and current_minute > 30:
            pass # Move to downtime logic post 10:30 AM
        else:
            shift_phase = "Morning Block: White-Collar Office Commute"
            directive = "Accept outbound suburb commuter strings heading toward central office grids. Auto-reject Gatineau pings to avoid bridge traffic."
            target_hub = "Downtown Core / Tunney's Pasture"
            reasoning = f"Peak office traffic window active from {current_location}. Federal and tech workers are moving toward main downtown core hubs."

    # --- PHASE 2: AFTERNOON SPLIT-SHIFT (02:30 PM to 08:30 PM) ---
    elif (current_hour == 14 and current_minute >= 30) or (15 <= current_hour <= 17):
        shift_phase = "Afternoon Block: Corporate Office Exodus"
        directive = "Position your vehicle inside corporate grids. Filter strictly for premium outbound trips delivering passengers back to peripheral suburbs."
        target_hub = "Downtown Core ➔ Suburb Corridors"
        reasoning = f"It is {time_str}. Workers are clearing out of central workspaces heading back home to suburbs like Barrhaven and Orléans."
        
    elif 18 <= current_hour <= 20:
        if current_hour == 20 and current_minute > 30:
            pass # Shift ends at 8:30 PM
        else:
            shift_phase = "Afternoon Block: Dinner / Return Vector"
            directive = "Activate your native Barrhaven destination filter app matrix. Drop your filter thresholds to capture any final local neighborhood runs."
            target_hub = "Barrhaven Home Base Grid"
            reasoning = f"Shift wrap-up window active. The destination alignment safeguards against late long-distance runs to Orléans or Gatineau, bringing you home on a paying fare."

    # Output highly structural UI card results immediately
    st.write("### 🧠 Live Strategic Dispatch Instruction")
    st.info(
        f"⏱️ *Active Phase:* **{shift_phase}**\n\n"
        f"🎯 *DIRECTIVE:* {directive}\n\n"
        f"📍 *Target Hub:* {target_hub}\n\n"
        f"🧠 *Strategy Matrix:* {reasoning}"
    )
    st.caption(f"Calculated instantly via Local Matrix Engine at: {time_str}")

