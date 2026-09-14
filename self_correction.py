from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

correction_agent = Agent(
    model=model,
    system_prompt="""
You are a patient study coach.

Your job is to evaluate a student's answer against the provided
study material.

If the answer is correct:
- Say it is correct.
- Give a short positive explanation.

If the answer is incorrect:
- Clearly say that it needs correction.
- Explain the concept in simpler language.
- Use a small analogy or example when useful.
- End with one short retry question.

Always base your evaluation on the provided study material.
"""
)


def evaluate_answer(topic, question, student_answer, study_material):

    prompt = f"""
Evaluate the student's answer.

TOPIC:
{topic}

QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

STUDY MATERIAL:
{study_material}

Decide whether the answer is correct.

If CORRECT:
Give a short explanation of why.

If INCORRECT:
1. Explain the mistake simply.
2. Rewrite the exact concept in easier language.
3. Give a small example or analogy.
4. 4. Ask ONE short retry question that tests the same concept the student got 
5. Do not introduce a new topic.
"""

    response = correction_agent(prompt)

    return str(response)
if __name__ == "__main__":

    material = """
    Cloud computing provides computing resources such as servers,
    storage and software over the internet instead of requiring
    users to own physical infrastructure.
    """

    result = evaluate_answer(
        topic="Cloud Computing",
        question="What is cloud computing?",
        student_answer="Cloud computing means buying your own physical servers.",
        study_material=material
    )

    print(result)