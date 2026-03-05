from http import client
from fastapi import FastAPI
from ollama import Client   


app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

client.pull("gemma3:1b")  # Pull the fine-tuned model from Ollama

@app.get("/")
def read_root(Query: str): 
    response = client.chat(
        model="gemma3:1b",      
        messages=[
            {"role": "system", "content": "you are helpful assistant "},
            {"role": "user", "content": Query}
        ] 
    )
    print(response)
    return {"response": response, "llm_answers": response.message.content}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/login")
def login(username: str, password: str):
    # Implement your authentication logic here
    if username == "admin" and password == "password":
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}, 401
    
    