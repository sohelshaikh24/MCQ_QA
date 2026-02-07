import streamlit as st
import requests

import os

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")



st.title("📚 MCQ Q&A Chatbot")

topic = st.selectbox("Choose a topic:", ["NLP", "RAG"])
# resp = requests.get(f"http://backend:8000/questions/{topic}")
resp = requests.get(f"{backend_url}/questions/{topic}")

for q in resp.json():
    st.subheader(q["question"])
    chosen = st.radio("Options", list(q["options"].items()), format_func=lambda x: f"{x[0]}: {x[1]}", key=q["id"])
    if st.button("Submit", key=f"btn_{q['id']}"):
        resp2 = requests.post(f"{backend_url}/answer", json={"mcq_id": q["id"], "chosen": chosen[0]})
        print(resp2.json())
        st.write(resp2.json()["result"])


st.subheader("📜 Your Attempts")
if st.button("Show"):
    resp = requests.get(f"{backend_url}/attempts")
    for item in resp.json():
        st.write(f"QID {item['mcq_id']} → Chosen: {item['chosen']} → {item['result']} ({item['timestamp']})")