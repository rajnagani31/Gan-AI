from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


# query ='HI'
query = 'my name is raj'
query ='what is my name?'
query = "what is my last question?"

response = client.responses.create(
    model="gpt-5.6",
    input=query,
    store=True
)

print(response.output_text)
print(response)


# response = client.responses.create(
#     model="gpt-5.6",
#     input=query,
# )
# print(response.output_text)
# print('[R1]', response)

# second_response = client.responses.create(
#     model="gpt-5.6",
#     previous_response_id=response.id,
#     input=[{"role": "user", "content": "query2"}],
# )
# print(second_response.output_text)
# print('[R2]', second_response)