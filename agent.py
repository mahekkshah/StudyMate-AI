from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)


def generate_notes(text):

    notes_agent = Agent(
        model=model,
        system_prompt="""
You are a study assistant for college students.

Your job is to turn difficult study material into simple,
clear and exam-friendly notes.

Rules:
- Use simple English.
- Explain concepts clearly.
- Keep important technical terms.
- Use headings and bullet points.
- Give small examples when useful.
- Do not add information that is not supported by the provided material.
- Keep the notes concise.
"""
    )

    prompt = f"""
Convert the following study material into simple,
exam-friendly notes.

Organize the notes with:
1. Topic headings
2. Simple explanations
3. Important points
4. Examples where useful

Do not repeat information.

STUDY MATERIAL:
{text}
"""

    response = notes_agent(prompt)

    return str(response)


def generate_notes(text):

    # Create a fresh agent for every request.
    # This prevents Strands concurrency errors in Streamlit.
    notes_agent = Agent(
        model=model,
        system_prompt="""
You are a study assistant for college students.

Your job is to turn difficult study material into simple,
clear and exam-friendly notes.

Rules:
- Use simple English.
- Explain concepts clearly.
- Keep important technical terms.
- Use headings and bullet points.
- Give small examples when useful.
- Do not add information that is not supported by the provided material.
- Keep the notes concise.
"""
    )

    prompt = f"""
Convert the following study material into simple,
exam-friendly notes.

Organize the notes with:
1. Topic headings
2. Simple explanations
3. Important points
4. Examples where useful

Do not repeat information.

STUDY MATERIAL:
{text}
"""

    response = notes_agent(prompt)

    return str(response)