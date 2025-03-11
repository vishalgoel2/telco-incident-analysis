from typing import TypeVar, Type

from openai import OpenAI
from pydantic import BaseModel

with open("../secret/copilot_api_key", "r") as file:
    API_KEY = file.read()

client = OpenAI(api_key=API_KEY, base_url="https://models.inference.ai.azure.com")
PydanticSchema = TypeVar("PydanticSchema", bound=BaseModel)


def generate(
    system_prompt: str,
    prompt: str,
    response_format: Type[PydanticSchema],
) -> PydanticSchema:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
        response_format=response_format,
    )
    return completion.choices[0].message.parsed
