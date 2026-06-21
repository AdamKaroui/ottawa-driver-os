import os
import time
from typing import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import streamlit as st

# 1. State Definition
class DriverState(TypedDict):
    current_time: str
    current_location: str
    recommendation: str

# 2. Schema for Structured Outputs
class StrategyOutput(BaseModel):
    shift_phase: str = Field(description="Name of the active split-shift phase.")
    actionable_instruction: str = Field(description="Clear, 1-sentence driving instruction.")
    target_zone: str = Field(description="The specific hub or corridor to target.")
    tier_filter: str = Field(description="Which ride tiers to accept (e.g., Comfort Only, All).")
    reasoning: str = Field(description="Brief reason for this decision based on the shift time.")

# 3. Time-Aware Optimization Logic
def evaluate_split_shift_strategy(state: DriverState) -> DriverState:
    system_prompt = (
        "You are the shift-coaching engine for an Ottawa ride-hailing driver. "
        "Vehicle Profile: Rented 2023 Polestar 2 via Weeve (Unlimited mileage, $0/km depreciation). "
        "Fuel Profile: Always fully charged/fueled from home. Ignore battery metrics entirely. "
        "Driver Schedule Profile: "
        "- Shift 1 (Morning Block): 04:30 AM to 10:30 AM. "
        "  * 04:30 AM - 07:00 AM: Focus strictly on airport (YOW) runs from Barrhaven/Kanata. "
        "  * 07:00 AM - 10:30 AM: Focus on morning white-collar office commutes into Downtown/Tunney's Pasture. "
        "- Shift 2 (Afternoon/Evening Block): 02:30 PM to 08:30 PM. "
        "  * 02:30 PM - 05:30 PM: Reverse commute. Catch workers leaving the Core heading out to suburbs. "
        "  * 05:30 PM - 08:30 PM: Transition to late business travel and early dinner rushes. "
        "    By 07:30 PM, use destination filters to route back toward the Barrhaven home base. "
        "Operational Rules: Maximize $/hr. Avoid crossing into Gatineau during peak traffic windows (07:30-09:00 AM and 03:30-05:30 PM)."
    )
    
    user_prompt = f"""
    Evaluate current metrics:
    - Current Time: {state['current_time']}
    - Current Location: {state['current_location']}
    """
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    structured_llm = llm.with_structured_output(StrategyOutput)
    
    response = structured_llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    
    state['recommendation'] = (
        f"⏱️ *Active Phase:* **{response.shift_phase}**\n\n"
        f"🎯 *DIRECTIVE:* {response.actionable_instruction}\n\n"
        f"📍 *Target Hub:* {response.target_zone}\n"
        f"💎 *Ride Filter:* {response.tier_filter}\n"
        f"🧠 *Strategy Matrix:* {response.reasoning}"
    )
    return state

# 4. Compile the LangGraph Flow
workflow = StateGraph(DriverState)
workflow.add_node("optimize_yield", evaluate_split_shift_strategy)
workflow.set_entry_point("optimize_yield")
workflow.add_edge("optimize_yield", END)
langgraph_app = workflow.compile()

# =====================================================================
# 5. STREAMLIT FRONTEND
# =====================================================================
st.set_page_config(page_title="Driver OS Split-Shift", page_icon="📈", layout="centered")

st.title("📈 Driver OS: Split-Shift Matrix")
st.subheader("Ottawa Strategic Dispatch Tracker")

# Current Location manual override drop-down
current_location = st.selectbox(
    "Select Current Location Cell:", 
    ["Barrhaven", "Kanata North", "Downtown Core", "Orléans", "YOW Airport", "Gatineau"]
)

st.divider()

if st.button("Generate Current Phase Optimization", type="primary"):
    # Generate input payload dynamically on click
    input_payload = {
        "current_time": time.strftime("%I:%M %p"),
        "current_location": current_location,
        "recommendation": ""
    }
    
    with st.spinner("Processing timeframe parameters..."):
        final_state = langgraph_app.invoke(input_payload)
        st.write("### 🧠 Live Quantum Dispatch Instruction")
        st.info(final_state['recommendation'])
        st.caption(f"Calculated dynamically at: {time.strftime('%I:%M:%S %p')}")
