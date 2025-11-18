
import openai

client = openai.OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio endpoint
    api_key="sk-xxxxxx"
)

def generate_text(messages, model="openchat-3.6-8b-20240522", temperature=0.7, max_tokens=1024):
    
    # Ensure messages list is formatted correctly
    formatted_messages = []
    for msg in messages:
        if not isinstance(msg.get("content"), str) or not msg["content"].strip():
            raise ValueError(f"Invalid message content: {msg}")
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})

    completion = client.chat.completions.create(
        model=model,
        messages=formatted_messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return completion.choices[0].message.content

# import openai

# client = openai.OpenAI(
#     base_url="http://localhost:1234/v1",
#     api_key="dummy"  # LM Studio ignores but required field
# )

# def generate_text(messages, model="openchat-3.6-8b-20240522", temperature=0.7, max_tokens=1024):
    
#     if not isinstance(messages, list):
#         raise ValueError("generate_text now requires a list of chat messages.")

#     completion = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         max_tokens=max_tokens,
#         temperature=temperature
#     )

#     return completion.choices[0].message.content
