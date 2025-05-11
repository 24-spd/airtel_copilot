import streamlit as st

# === INTENT DETECTION ===
def identify_intent(text):
    if "router" in text.lower():
        return "router_issue"
    elif "dth" in text.lower() or "set-top" in text.lower():
        return "dth_issue"
    return "unknown"

# === MOCK CLASSIFICATION ===
def classify_image(image_file):
    return "Red blinking power light – firmware failure"

# === KNOWLEDGE BASE ===
def retrieve_from_kb(query, intent):
    router_kb = {
        "Red blinking power light – firmware failure": 
        "1. Power cycle the router\n2. Wait 2 minutes\n3. If blinking continues, press reset for 10 seconds."
    }
    dth_kb = {
        "No signal": 
        "1. Check dish alignment\n2. Inspect cable connection\n3. Restart set-top box."
    }
    return router_kb.get(query) if intent == "router_issue" else dth_kb.get(query)

# === ESCALATION ===
def escalate_to_manager(context):
    return f"🚨 Escalated to manager with issue: '{context['image_issue']}' and input: '{context['raw_input']}'"

# === STREAMLIT UI ===
st.title("🛠️ Airtel Agentic AI Copilot")

# Use only text input (Cloud-safe)
user_input = st.text_input("💬 Describe the issue you're facing (e.g., router not working, DTH no signal):")

if user_input:
    intent = identify_intent(user_input)

    if intent in ["router_issue", "dth_issue"]:
        st.success(f"✅ Detected {intent.replace('_', ' ')}. Please upload an image if available.")
        image_file = st.file_uploader("📸 Upload image", type=["jpg", "png", "jpeg"])

        if image_file:
            error_label = classify_image(image_file)
            st.info(f"🧠 Detected issue: **{error_label}**")

            resolution = retrieve_from_kb(error_label, intent)
            if resolution:
                st.success("🧰 Try the following steps:")
                st.code(resolution)
            else:
                escalation_msg = escalate_to_manager({
                    "intent": intent,
                    "image_issue": error_label,
                    "raw_input": user_input
                })
                st.warning(escalation_msg)
        else:
            st.info("Image not uploaded yet. Some diagnoses might be limited.")
    else:
        st.error("❌ Sorry, I can only help with router or DTH issues currently.")
