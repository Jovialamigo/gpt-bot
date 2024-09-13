import logging

from openai import AsyncOpenAI

from data.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

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
    "gpt-4-turbo": 0.03,
}


async def ask_chat(text: str, model: str = "gpt-3.5-turbo"):
    """
    Returns model's response content and total price of request in rubles

    Parameters
    ----------
    text: str
        Question to ChatGPT
    model: str
        The model version

    """
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
    price = gpt_price.get(model, 0) / 1000
    if price is None:
        price = 0

    tokens = completion.usage.total_tokens * price
    content = completion.choices[0].message.content
    logging.info(f"Price is: {tokens} rubles")

    return (content, tokens)


async def generate_image(text: str, size: str = "1024x1024", quality: str = "standard"):
    """
    Returns image url with price in rubles

    Parameters
    ----------
    text: str
        image description
    size: str
         one of the following image sizes: "1024x1024", "1024x1792", "1792x1024"
    quality: str
        "standard" or "hd"

    """
    logging.info(f"Image description: {text}")
    response = await client.images.generate(
        model="dall-e-3",
        prompt=text,
        n=1,
        size=size,
        quality=quality,
    )

    price = image_price.get(quality).get(size, 0) * 100
    if price is None:
        price = 0

    url = response.data[0].url
    logging.info(f"Price is: {price} rubles")
    return url, price
