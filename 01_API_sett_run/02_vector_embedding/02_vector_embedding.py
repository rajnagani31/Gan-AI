
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


text='cat chase dog'

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print(response)
print("len:",len(response.data[0].embedding))#cheak lenthe of response

print("Model used:", response.model)
print("Usage info:", response.usage if hasattr(response, "usage") else "No usage info")
