import time
from typing import List

from pydantic import BaseModel

from copilot_openai import generate
from store import get_scenario_to_generate, update_scenario


class Dataset(BaseModel):
    issueDescription: str
    actionsTaken: str
    resolution: str
    rca: str


class DatasetList(BaseModel):
    datasets: List[Dataset]


system_prompt = """
    You are a synthetic data generator for telecom incident management analytics. For the provided scenario below, generate 20 synthetic datasets that capture realistic variations in customer-reported incidents. Each dataset must be formatted as a JSON object with the following keys:
    - "issueDescription": A concise description of the issue as provided by the customer. Vary the language style—sometimes the description may be vague or missing details. Include technical details when relevant (e.g., invoice numbers, MSISDN, order IDs, billing account numbers, PBX corporate numbers).
    - "actionsTaken": A description of the steps taken by the support team to diagnose or investigate the issue. This can include checking system logs, reviewing error messages, verifying account details, or providing initial customer guidance.
    - "resolution": A resolution message that is visible to the customer. It might include instructions such as system restarts, code fixes, data corrections, customer education (in cases of false positives), or remedial actions like sending replacement items (e.g., for duplicate delivery issues).
    - "rca": The internal root cause analysis that explains the underlying technical or process issue. This field should be detailed and may include technical specifics that are not visible to the customer.
    
    Important requirements:
    - Generate exactly 20 JSON objects and output them as a JSON array.
    - Ensure diversity by varying language styles (e.g., sometimes customers use formal language, sometimes slang or vague descriptions).
    - Some outputs should simulate false positive scenarios (where the issue is due to customer misunderstanding).
    - For technical or software-related issues, include details such as error messages displayed on webpages, usernames used during login, page URLs, browser details, etc.
    - Make sure to incorporate diverse technical details (e.g., random made-up invoice numbers, order IDs, MSISDN, billing account numbers) in some outputs.
    
    Your output must strictly be a valid JSON array following the format specified above.
"""


def main():
    total_requests = 0
    minute_requests = 0
    minute_start_time = time.time()

    while total_requests < 95:
        current_time = time.time()
        if current_time - minute_start_time >= 60:
            minute_requests = 0
            minute_start_time = current_time

        if minute_requests >= 10:
            sleep_time = 60 - (current_time - minute_start_time)
            if sleep_time > 0:
                print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                minute_requests = 0
                minute_start_time = time.time()

        scenario = get_scenario_to_generate()
        if scenario is None:
            print("No more scenarios to generate. Exiting.")
            break

        print(
            f"Generating datasets for scenario {scenario['scenario']} with id {scenario['id']}..."
        )

        try:
            prompt = f"Scenario: {scenario['scenario']}"
            datasets = generate(system_prompt, prompt, DatasetList)

            update_scenario(scenario, datasets)

            total_requests += 1
            minute_requests += 1

            print(
                f"Generated datasets for scenario {scenario['id']}. Total requests: {total_requests}"
            )

        except Exception as e:
            print(f"Error generating datasets for scenario {scenario['id']}: {str(e)}")
            total_requests += 1
            minute_requests += 1

    print(f"Completed with {total_requests} total requests.")


if __name__ == "__main__":
    main()
