import streamlit as st
import requests

st.title("📚 MCQ Q&A Chatbot")

topic = st.selectbox("Choose a topic:", ["NLP", "RAG"])
resp = requests.get(f"http://backend:8000/questions/{topic}")

for q in resp.json():
    st.subheader(q["question"])
    chosen = st.radio("Options", list(q["options"].items()), format_func=lambda x: f"{x[0]}: {x[1]}", key=q["id"])
    if st.button("Submit", key=f"btn_{q['id']}"):
        resp2 = requests.post("http://backend:8000/answer", json={"mcq_id": q["id"], "chosen": chosen[0]})
        print(resp2.json())
        st.write(resp2.json()["result"])


st.subheader("📜 Your Attempts")
if st.button("Show"):
    resp = requests.get("http://backend:8000/attempts")
    for item in resp.json():
        st.write(f"QID {item['mcq_id']} → Chosen: {item['chosen']} → {item['result']} ({item['timestamp']})")