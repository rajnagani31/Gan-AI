# LLM Adapters

This folder provides four class-based adapters with the same methods:

- `invoke(prompt)` returns the complete response.
- `stream(prompt)` yields text chunks as the model generates them.
- `set_system_instruction(text)` sets a default system instruction.
- `set_tools(tool_definitions)` attaches function tools.

## Available adapters

- `LangChainOpenAIAdapter` - LangChain with OpenAI
- `LangChainGroqAdapter` - LangChain with Groq
- `OpenAIAdapter` - direct OpenAI SDK
- `GroqAdapter` - direct Groq SDK

## Example

```python
from dotenv import load_dotenv
from adapter import OpenAIAdapter

load_dotenv()

llm = OpenAIAdapter()
llm.set_system_instruction("You are a concise product assistant.")
for token in llm.stream("Explain streaming in one sentence."):
    print(token, end="", flush=True)
```

Set `OPENAI_API_KEY` for the OpenAI adapters and `GROQ_API_KEY` for the Groq adapters. Run the example from the `15_llm_wiki.md` folder so Python can find the `adapter` package.

## Tools and system instructions

All adapters accept OpenAI-compatible tool definitions. Add defaults with `set_tools()` and `set_system_instruction()`, or send them for one request with `invoke(..., system_instruction=..., tools=...)` and `stream(..., system_instruction=..., tools=...)`.

```python
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}

llm.set_tools([weather_tool])
llm.invoke("What is the weather in Delhi?")
print(llm.last_tool_calls)  # Function name and arguments requested by the model
```

The adapter records requested function calls in `last_tool_calls`. Your application must execute the function and send its result to the model in a follow-up request.
