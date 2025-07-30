from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os
import subprocess

load_dotenv()

client = OpenAI()
SAFE_COMMANDS = [
    "echo",           # Safe printing
    "cd",             # Change directory
    "dir",            # List files (Windows)
    "ls",             # List files (Linux/macOS)
    "type",           # Read file (Windows)
    "cat",            # Read file (Linux/macOS)
    "python",         # Run Python scripts
    "pip install",    # Install Python packages
    "npm run dev"     # Start dev server
]

def run_command(command: str):
    global dev_server_process
    print("💻 Running command...")

    parts = [part.strip() for part in command.split("&&")] 
    working_dir = os.getcwd() 

    for part in parts:
        if part.startswith("cd"):
            path = part.replace("cd", "").strip()
            working_dir = os.path.join(working_dir, path)
            continue

        if not any(part.startswith(cmd) for cmd in SAFE_COMMANDS):
            return "Unsafe command blocked", ""
        if part.startswith("npm run dev"):
            print("Starting development server...")
            dev_server_process  = subprocess.Popen(part, shell=True, cwd=working_dir)
            return "Development server started in background.", ""

        result = subprocess.run(part, shell=True, capture_output=True, text=True, cwd=working_dir)

        if result.returncode != 0:
            print(f"Error running: {part}")
            return result.stdout.strip(), result.stderr.strip()

    return "All commands executed successfully.", "" 

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

"""

messages = [
  { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("> ")
    messages.append({ "role": "user", "content": query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({ "role": "assistant", "content": response.choices[0].message.content })
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break