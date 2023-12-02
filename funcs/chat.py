import logging

from openai import AsyncOpenAI

from data.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def ask_chat(text: str, model: str = "gpt-3.5-turbo") -> str:
    logging.info(f"Asking {model} for: {text}")
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return completion.choices[0].message.content


async def generate_image(text: str) -> str:
    logging.info(f"Image description: {text}")
    response = await client.images.generate(
        model="dall-e-3", prompt=text, n=1, size="1024x1024"
    )
    return response.data[0].url
