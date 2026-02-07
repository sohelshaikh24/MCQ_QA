import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
import guardrails as gr
from pathlib import Path
from fastapi.responses import JSONResponse
app = FastAPI()

conn = sqlite3.connect("qa.db", check_same_thread=False)
cursor = conn.cursor()

class Answer(BaseModel):
    mcq_id: int
    chosen: str

@app.get("/questions/{topic}")
def get_questions(topic: str):
    cursor.execute("SELECT id, question, option_a, option_b, option_c, option_d FROM mcq WHERE topic=?", (topic,))
    rows = cursor.fetchall()
    return [
        {"id": r[0], "question": r[1], "options": {"A": r[2], "B": r[3], "C": r[4], "D": r[5]}}
        for r in rows
    ]

@app.post("/answer")
def check_answer(ans: Answer):
    cursor.execute("SELECT correct FROM mcq WHERE id=?", (ans.mcq_id,))
    row = cursor.fetchone()
    if not row:
        return {"result": "Invalid question ID"}
    correct = row[0]

    raw_result = "Correct!" if ans.chosen.upper() == correct else f"Wrong. Correct answer is {correct}"

     # Save attempt in DB
    cursor.execute(
        "INSERT INTO attempts(mcq_id, chosen, result) VALUES (?, ?, ?)",
        (ans.mcq_id, ans.chosen.upper(), raw_result)
    )
    conn.commit()


    return {"result": raw_result}


@app.get("/attempts")
def get_attempts():
    cursor.execute("SELECT mcq_id, chosen, result, timestamp FROM attempts ORDER BY id DESC")
    rows = cursor.fetchall()
    return [
        {"mcq_id": r[0], "chosen": r[1], "result": r[2], "timestamp": r[3]}
        for r in rows
    ]
