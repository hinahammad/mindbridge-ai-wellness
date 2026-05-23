import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
GROQ_API_KEY =
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(system_prompt, user_message):
    if not GROQ_API_KEY:
        return "Error: API key not configured. Check your .env file."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
          "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        
        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text[:200]}"
        
        result = response.json()
        
        if "choices" not in result:
            return f"Unexpected response. Keys: {list(result.keys())}"
        
        return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"Error: {str(e)}"

# ============ PROMPTS ============

DREAM_PROMPT = """You are Dream Weaver, a mystical dream interpreter. 
Analyze dreams using symbolism, psychology, creative storytelling, and reflection.

Format EXACTLY like this:

🌟 SYMBOLISM
[Explain 2-3 key symbols]

🧠 PSYCHOLOGICAL INSIGHT
[What might this reveal about their subconscious]

✨ CREATIVE INTERPRETATION
[A short poetic or story-like interpretation]

💡 REFLECTION
[One question for the dreamer to ponder]

Keep each section 2-3 sentences."""

MOOD_PROMPT = """You are Mood Mirror, an empathetic AI wellness companion. 
Analyze the user's emotional state and provide supportive guidance.

Format EXACTLY like this:

🎭 EMOTION DETECTED
[Primary and secondary emotions]

📊 MOOD BREAKDOWN
- Stress level: X/10
- Energy level: X/10  
- Optimism level: X/10

💡 INSIGHT
[Why they might be feeling this way]

🌿 SUGGESTED ACTIVITIES
[3 practical activities to improve mood]

Keep it warm, supportive, and actionable."""

MINDFUL_PROMPT = """You are Mindful Mentor, a calming meditation and wellness guide.
Provide personalized mindfulness exercises based on user needs.

Format EXACTLY like this:

🧘 GUIDED EXERCISE
[Step-by-step breathing or meditation technique]

🌱 MINDFULNESS TIP
[A practical tip for daily life]

💭 REFLECTION
[A thought-provoking question]

Keep instructions clear and soothing."""

CRISIS_PROMPT = """You are Crisis Companion, a supportive mental health first responder.
Provide immediate comfort, validation, and resources.

Format EXACTLY like this:

💙 VALIDATION
[Acknowledge their feelings without judgment]

🤝 IMMEDIATE SUPPORT
[3 grounding techniques or coping strategies]

🚨 RESOURCES
[Encourage professional help with warm, non-clinical language]

If user mentions self-harm or suicide, strongly urge them to contact emergency services immediately.

Keep tone calm, caring, and non-judgmental."""

# ============ STREAMLIT UI ============

st.set_page_config(page_title="MindBridge AI Wellness", page_icon="🧠", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🧠 MindBridge")
    st.write("Your AI Wellness Companion")
    st.divider()
    
    st.subheader("👤 Your Profile")
    name = st.text_input("Your name:", value="Friend")
    st.write(f"Welcome, {name}!")
    
    st.divider()
    st.subheader("📊 Wellness Stats")
    st.metric("Total Check-ins", "5")
    st.metric("Avg Mood", "5.0/10")
    
    if st.button("🗑️ Clear History"):
        st.session_state.clear()
        st.rerun()

# Main content
st.title("🌙 MindBridge AI Wellness Agent")
st.caption("An AI-powered companion for mental wellness through dreams, mood, mindfulness, and crisis support.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌙 Dream Weaver", "🤯 Mood Mirror", "🧘 Mindful Mentor", "💬 Crisis Companion"])

# ============ TAB 1: DREAM WEAVER ============
with tab1:
    st.header("🌙 Dream Weaver")
    st.write("Share your dream and uncover its hidden meanings through symbolism, psychology, and creative storytelling.")
    
    dream = st.text_area("Describe your dream:", height=150, placeholder="I was flying over a vast ocean...")
    
    if st.button("✨ Interpret My Dream", type="primary", key="dream_btn"):
        if dream:
            with st.spinner("🌙 Weaving your interpretation..."):
                result = call_groq(DREAM_PROMPT, f"Interpret this dream: {dream}")
                st.markdown(result)
        else:
            st.error("Please describe your dream first.")

# ============ TAB 2: MOOD MIRROR ============
with tab2:
    st.header("🤯 Mood Mirror")
    st.write("Tell me how you're feeling, and I'll analyze your mood + suggest personalized activities.")
    
    feeling = st.text_area("How are you feeling right now?", height=100, placeholder="I feel overwhelmed with work...")
    
    mood_rating = st.slider("Rate your mood (1-10):", 1, 10, 5)
    
    if st.button("🎭 Analyze My Mood", type="primary", key="mood_btn"):
        if feeling:
            with st.spinner("🎭 Analyzing your mood..."):
                result = call_groq(MOOD_PROMPT, f"I'm feeling: {feeling}. On a scale of 1-10, my mood is {mood_rating}.")
                st.markdown(result)
        else:
            st.error("Please describe how you feel.")

# ============ TAB 3: MINDFUL MENTOR ============
with tab3:
    st.header("🧘 Mindful Mentor")
    st.write("Get personalized guided meditation, breathing exercises, and mindfulness tips.")
    
    need = st.text_area("What do you need help with?", height=100, placeholder="I need help sleeping better...")
    
    if st.button("🌿 Guide Me", type="primary", key="mindful_btn"):
        if need:
            with st.spinner("🧘 Finding your path to calm..."):
                result = call_groq(MINDFUL_PROMPT, f"I need help with: {need}")
                st.markdown(result)
        else:
            st.error("Please share what you need help with.")

# ============ TAB 4: CRISIS COMPANION ============
with tab4:
    st.header("💬 Crisis Companion")
    st.warning("🚨 If you're in immediate danger, please call emergency services: 112 or 15")
    
    situation = st.text_area("Share what's on your mind:", height=150, placeholder="I'm here to listen without judgment...")
    
    if st.button("🤝 Get Support", type="primary", key="crisis_btn"):
        if situation:
            with st.spinner("💙 Sending support your way..."):
                result = call_groq(CRISIS_PROMPT, f"I'm struggling with: {situation}")
                st.markdown(result)
        else:
            st.error("Please share what's happening.")

# Footer
st.divider()
st.caption("🧠 MindBridge AI Wellness Agent | Built with 💜 for mental health")
st.caption("⚠️ This is a wellness support tool, not a substitute for professional mental health care.")
