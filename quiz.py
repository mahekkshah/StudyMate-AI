from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

quiz_agent = Agent(
    model=model,
    system_prompt="""
You are a quiz generator for college students.

Your job is to create a short self-check quiz from study material.

Rules:
- Create exactly 3 questions.
- Use multiple-choice questions.
- Give 4 options: A, B, C, D.
- Questions must be based ONLY on the provided study material.
- Mix conceptual and factual questions.
- Keep questions simple and exam-friendly.
- Clearly provide the correct answer after each question.
"""
)


def generate_quiz(text):

    prompt = f"""
Create a 3-question multiple-choice quiz from the study material below.

For each question use exactly this format:

Q1. Question

A. Option
B. Option
C. Option
D. Option

Answer: A/B/C/D

STUDY MATERIAL:
{text}
"""

    response = quiz_agent(prompt)

    return str(response)