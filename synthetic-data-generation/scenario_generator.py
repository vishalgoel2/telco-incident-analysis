from typing import List

from pydantic import BaseModel

from copilot_openai import generate
from store import insert_scenarios


class ScenarioList(BaseModel):
    root: List[str]


system_prompt = """
    You are a telecom incident scenario generator for an incident management analytics use case with root cause analysis (RCA). Your task is to generate 200 diverse incident scenarios in the telecom domain. Focus on creating realistic narrative descriptions that capture a wide range of incidents experienced by telecom customers (both B2B and B2C). 

    The scenarios should cover both IT-related issues and non-IT issues, including but not limited to:
    - IT-related incidents: login failures, incorrect or outdated contact details displayed, inability to place orders, wrong pricing information, sluggish website performance, self-service portal downtime, chatbot errors, and other software/application issues.
    - Non-IT incidents: service outages (mobile voice, mobile broadband, fixed line broadband, PBX for B2B, IoT, etc.), billing discrepancies, invoice errors, order processing failures, delivery anomalies (e.g., double delivery or "order failed" messages despite successful delivery), and issues with updating account or contract information.

    Consider various telecom services and applications such as:
    - Services: mobile voice, mobile broadband, fixed line broadband, PBX (B2B), IoT.
    - Applications: self-service portals, webshops, payment systems, order processing, order history, billing accounts, credit card payments, delivery systems, discounts, returns, and contract management.
    - Channels: websites, mobile apps, customer APIs, shopits, and chatbots.
    - Additional areas: network issues, security vulnerabilities (e.g., weak Content Security Policy), and GDPR breaches (e.g., exposure of another user's data in self-service).
    - Additionally, please refer to TMF API specs to understand the range of software systems and services typically used by telcos, ensuring your scenarios reflect real-world telecom operations.

    Your output must be a JSON array containing exactly 50 scenario strings. Each scenario string should describe an incident in clear, concise language, focusing on the nature of the issue and its impact. Do not include any explicit technical identifiers (such as invoice numbers, MSISDN, order IDs, billing account numbers, etc.) as these details will be added in a later step.

    Example scenario:
    "Telecom self-service portal outage affecting both B2B and B2C customers, leading to inability to update contact details and process payments across multiple channels, including mobile apps and websites."

    Generate exactly 200 such scenarios as a JSON array of strings.
"""
prompt = "Please generate telecom incident scenarios as specified."


def main():
    print("Starting scenario generation...")
    try:
        response = generate(system_prompt, prompt, ScenarioList)
        scenarios = response.root
        insert_scenarios(scenarios)
        print(f"Successfully generated and inserted {len(scenarios)} scenarios.")
    except Exception as e:
        print(f"Error generating scenarios: {str(e)}")


if __name__ == "__main__":
    main()
