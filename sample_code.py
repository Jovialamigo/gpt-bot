# %%
from openai import OpenAI

client = OpenAI()

# %%
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        # {
        #     "role": "system",
        #     "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        # },
        {
            "role": "user",
            "content": "Напиши стих 4 строки",
        },
    ],
)
#  %%
image_price = {
    "standard": {
        "1024x1024": 0.04,
        "1024x1792": 0.08,
        "1792x1024": 0.08,
    },
    "hd": {
        "1024x1024": 0.08,
        "1024x1792": 0.12,
        "1792x1024": 0.12,
    },
}
gpt_price = {
    "gpt-3.5-turbo": 0.002,
    "gpt-4-1106-preview": 0.03,
}

print(completion.choices[0].message.content)
completion.usage.total_tokens
# %%
image = client.images.generate(
    model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
)
# %%
image.data[0].url
image
# %%
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for part in stream:
    print(part.choices[0].delta.content or "")
# %%
