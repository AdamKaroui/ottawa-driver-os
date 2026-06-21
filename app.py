import os
import time
import json
import requests
import streamlit as st

# =====================================================================
# 1. STREAMLIT FRONTEND & THEME CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Driver OS Split-Shift", page_icon="📈", layout="centered")

st.title("📈 Driver OS: Split-Shift Matrix")
st.subheader("Ottawa Strategic Dispatch Tracker")

current_location = st.selectbox(
    "Select Current Location Cell:", 
    ["Barrhaven", "Kanata North", "Downtown Core", "Orléans", "YOW Airport", "Gatineau"]
)

st.divider()

# =====================================================================
# 2. OPENROUTER SECURE RELAY ENGINE (Bypasses Data-Center IP Blocks)
# =====================================================================
if st.button("Generate Current Phase Optimization", type="primary"):
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("Error: API Key secret is not configured in your Streamlit Advanced settings panel.")
    else:
        input_time = time.strftime("%I:%M %p")
        
        with st.spinner("Routing parameters securely via OpenRouter Relay..."):
            system_prompt = (
                "You are the shift-coaching engine for an Ottawa ride-hailing driver.\n"
                "Vehicle Profile: Rented 2023 Polestar 2 via Weeve (Unlimited mileage, \$0/km depreciation).\n"
                "Fuel Profile: Always fully charged/fueled from home. Ignore battery metrics entirely.\n"
                "Driver Schedule Profile:\n"
                "- Shift 1 (Morning Block): 04:30 AM to 10:30 AM.\n"
                "  * 04:30 AM - 07:00 AM: Focus strictly on airport (YOW) runs from Barrhaven/Kanata.\n"
                "  * 07:00 AM - 10:30 AM: Focus on morning white-collar office commutes into Downtown/Tunney's Pasture.\n"
                "- Shift 2 (Afternoon/Evening Block): 02:30 PM to 08:30 PM.\n"
                "  * 02:30 PM - 05:30 PM: Reverse commute. Catch workers leaving the Core heading out to suburbs.\n"
                "  * 05:30 PM - 08:30 PM: Transition to late business travel and early dinner rushes.\n"
                "    By 07:30 PM, use destination filters to route back toward the Barrhaven home base.\n"
                "Operational Rules: Maximize \$/hr. Avoid crossing into Gatineau during peak traffic windows (07:30-09:00 AM and 03:30-05:30 PM).\n\n"
                "Return your response STRICTLY as a raw JSON object. Do not wrap it in markdown code blocks. "
                "The JSON must feature exactly these keys: \"shift_phase\", \"actionable_instruction\", \"target_zone\", and \"reasoning\"."
            )
            
            user_prompt = f"Evaluate current metrics:\n- Current Time: {input_time}\n- Current Location: {current_location}"
            
            # Swapping endpoint to OpenRouter's secure public endpoint
            url = "https://openrouter.ai"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-4o-mini", # Calls the exact same model via OpenRouter's wrapper
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    raw_text = response.json()['choices']['message']['content'].strip()
                    
                    if raw_text.startswith("```"):
                        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                        
                    data = json.loads(raw_text)
                    
                    st.write("### 🧠 Live Quantum Dispatch Instruction")
                    st.info(
                        f"⏱️ *Active Phase:* **{data.get('shift_phase', 'Active Shift')}**\n\n"
                        f"🎯 *DIRECTIVE:* {data.get('actionable_instruction', '')}\n\n"
                        f"📍 *Target Hub:* {data.get('target_zone', '')}\n\n"
                        f"🧠 *Strategy Matrix:* {data.get('reasoning', '')}"
                    )
                    st.caption(f"Calculated dynamically at: {time.strftime('%I:%M:%S %p')}")
                else:
                    st.error(f"OpenRouter Gateway Error: Code {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Execution Engine Fault: {str(e)}")
