import streamlit as st
import google.generativeai as genai

# 1. THE CONNECTION (Replace with your actual key from Google AI Studio)
genai.configure(api_key="AIzaSyCkUT7zP9kzY-ljDehXJMDy8NJqh4KgUfE")
# 2. SMART SEARCH (This fixes the 404 error automatically)
try:
    # This finds the first working model on your account
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = available_models[0] if available_models else 'gemini-pro'
    model = genai.GenerativeModel(model_name)
except Exception:
 model = genai.GenerativeModel('gemini-pro')

# 2. THE INTERFACE
st.set_page_config(page_title="MediMind Hyderabad", page_icon="🏥")
st.title("🏥 Medical Diagnosis Assistant")
st.markdown("---")

# 3. PATIENT DATA SIDEBAR
with st.sidebar:
    st.header("Patient History")
    age = st.number_input("Age", 0, 120, 25)
    history = st.text_area("Previous Conditions", "None")

# 4. SYMPTOM ANALYSIS
symptoms = st.text_area("Describe Symptoms:", placeholder="e.g., Shortness of breath and fatigue...")

if st.button("Analyze Now"):
    if symptoms:
        import time
        success = False
        retries = 3
        while retries > 0 and not success:
            try:
                with st.spinner(f"Analyzing... (Attempt {4-retries}/3)"):
                    prompt = f"Analyze for a {age}yo with history of {history}: {symptoms}. Provide 3 possible conditions and next steps. Add medical disclaimer."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    success = True
            except Exception as e:
                retries -= 1
                if "429" in str(e):
                    st.warning("Google is busy. Retrying in 5 seconds...")
                    time.sleep(5) # Wait 5 seconds before trying again
                else:
                    st.error(f"Error: {e}")
                    break
    else:
        st.error("Please enter symptoms.")