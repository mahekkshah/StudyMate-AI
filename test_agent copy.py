from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

agent = Agent(model=model)

response = agent("Explain cloud computing in one simple sentence.")

print(response)