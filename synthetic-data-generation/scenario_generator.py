from typing import List

from pydantic import BaseModel

from llm import generate_openai
from store import insert_scenarios


class ScenarioList(BaseModel):
    root: List[str]


system_prompt = """
    You are a telecom incident scenario generator for an incident management analytics use case with root cause analysis (RCA). Your task is to generate 250 diverse incident scenarios in the telecom domain. Focus on creating realistic narrative descriptions that capture a wide range of incidents experienced by telecom customers (both B2B and B2C).

    The scenarios should cover both IT-related issues and non-IT issues, including but not limited to:
    - IT-related incidents: 
      * Login failures to customer portals (SSO failures, permission problems)
      * Incorrect or outdated contact details displayed
      * Inability to place orders in self-service portals
      * Wrong pricing information displayed
      * Sluggish website performance
      * Self-service portal downtime
      * Chatbot errors
      * UI inconsistencies (data showing in one view but not another)
      * Missing features in customer portals
      * Error messages when performing routine operations
      * Integration issues between different systems (Salesforce, Self-Service, Customer facing APIs, etc.)
    
    - Non-IT incidents: 
      * Service outages (mobile voice, mobile broadband, fixed line broadband, PBX for B2B, IoT)
      * Billing discrepancies and invoice errors
      * Order processing failures
      * Device delivery anomalies (wrong delivery locations, missing collection point information, double delivery, system shows "order failed" but device still delivered)
      * Issues with updating account or contract information
      * Problems with subscription management (terminations not reflecting properly, transfers between users)
    
    Consider various telecom services and applications such as:
    - Services: mobile voice, mobile broadband, fixed line broadband, PBX (B2B), IoT, eSim (multisim service), Devices
    - Applications: self-service portals, webshops, payment systems, order processing systems
    - Features: order history, billing accounts, invoice viewing, credit card payments, delivery systems, discounts, returns, contract management, device catalogs
    - Channels: websites, mobile apps, customer APIs, shopits, chatbots
    - Additional areas: network issues, security vulnerabilities, GDPR breaches (e.g., exposure of another user's data in self-service).
    - Additionally, please refer to TMF API specs to understand the range of software systems and services typically used by telcos, ensuring your scenarios reflect real-world telecom operations.
    
    Other common error scenarios:
    - Specific UI error messages like Oops, something went wrong
    - Data synchronization issues between different interfaces
    - Feature flags and version mismatch problems
    - Incorrect permission assignments
    - Work queue routing issues
    - Impersonation and user switching problems
    
    Your output must be a JSON array containing exactly 250 scenario strings. Each scenario string should describe an incident in clear, concise language, focusing on the nature of the issue and its impact. Do not include any explicit technical identifiers (such as invoice numbers, MSISDN, order IDs, billing account numbers, etc.) as these details will be added in a later step.
    
    Example scenarios:
    1. "Telecom self-service portal outage affecting both B2B and B2C customers, leading to inability to update contact details and process payments across multiple channels, including mobile apps and websites."
    2. "Corporate customer unable to manage Device catalog in self-service portal, with accessories and cases not displaying correctly across multiple device catalogs, preventing employees from ordering approved devices."
    3. "Invoices not appearing in customer's self-service portal despite being generated correctly in billing system, causing payment delays and customer confusion about outstanding balances."
"""
prompt = "Please generate telecom incident scenarios as specified."


def main():
    print("Starting scenario generation...")
    try:
        response = generate_openai(system_prompt, prompt, ScenarioList)
        scenarios = response.root
        insert_scenarios(scenarios)
        print(f"Successfully generated and inserted {len(scenarios)} scenarios.")
    except Exception as e:
        print(f"Error generating scenarios: {str(e)}")


if __name__ == "__main__":
    main()
