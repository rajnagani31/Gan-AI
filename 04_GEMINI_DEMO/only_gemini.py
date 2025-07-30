from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
       "what is genai"
    ]

)
print(response.text)

