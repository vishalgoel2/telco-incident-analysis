from typing import TypeVar, Type

from google import genai
from google.genai import types
from openai import OpenAI
from pydantic import BaseModel

with open("../secret/copilot_api_key", "r") as file:
    COPILOT_API_KEY = file.read()
copilot_client = OpenAI(
    api_key=COPILOT_API_KEY, base_url="https://models.inference.ai.azure.com"
)
with open("../secret/gemini_api_key", "r") as file:
    GEMINI_API_KEY = file.read()
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
PydanticSchema = TypeVar("PydanticSchema", bound=BaseModel)


def extract_json_from_response(response_text):
    import re

    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response_text)
    if json_match:
        response_text = json_match.group(1)
    if response_text.strip().startswith("["):
        response_text = '{"datasets":' + response_text.strip() + "}"
    return response_text


def generate_openai(
    system_prompt: str,
    prompt: str,
    response_format: Type[PydanticSchema],
) -> PydanticSchema:
    completion = copilot_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
        response_format=response_format,
    )
    return completion.choices[0].message.parsed


def generate_deepseek(
    system_prompt: str,
    prompt: str,
    response_format: Type[PydanticSchema],
) -> PydanticSchema:
    completion = copilot_client.beta.chat.completions.parse(
        model="deepseek-v3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
        response_format={"type": "json_object"},
    )
    response = extract_json_from_response(completion.choices[0].message.content)
    try:
        return response_format.model_validate_json(response)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response}")
        raise e


def generate_gemini(
    system_prompt: str,
    prompt: str,
    response_format: Type[PydanticSchema],
) -> PydanticSchema:
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_format,
            system_instruction=system_prompt,
        ),
    )
    return response.parsed
