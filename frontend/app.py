# frontend/app.py

import streamlit as st
import requests

st.set_page_config(page_title="Local LLM Chat", layout="centered")
st.title("🧠 Local LLM Chat (Ollama + FastAPI + Streamlit)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type your message...")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process new input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": user_input},
                    timeout=60
                )
                reply = res.json().get("response", "[Error]")
            except Exception as e:
                reply = f"[Connection error]: {str(e)}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
