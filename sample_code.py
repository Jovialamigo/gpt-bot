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
print(completion.choices[0].message.content)

# %%
completion
# %%
image = client.images.generate(
    model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
)
# %%
image.data[0].url
# %%
