import tiktoken #open ai made tiktoken pakage

enc=tiktoken.encoding_for_model("gpt-4o")
text='Hello my name is raj love'

tokens=enc.encode(text)

print("Tokens:",tokens)

Tokens= [13225, 922, 1308, 382, 46358]
decode=enc.decode(Tokens)
print("Decode Text:",decode)
