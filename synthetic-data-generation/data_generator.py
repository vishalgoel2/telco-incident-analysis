import time
from typing import List

from pydantic import BaseModel

from llm import generate_deepseek, generate_gemini, generate_openai
from store import get_scenario_to_generate, update_scenario


class Dataset(BaseModel):
    issueDescription: str
    actionsTaken: List[str]
    resolution: str
    rca: str


class DatasetList(BaseModel):
    datasets: List[Dataset]


system_prompt = """
    You are a synthetic data generator for telecom incident management analytics. For the provided scenario below, generate 5 synthetic datasets that capture realistic variations in customer-reported incidents. Each dataset must be formatted as a JSON object with the following keys:

    - "issueDescription": A concise but detailed description of the issue as provided by the customer. This should closely match real customer submissions in style and content - often brief, sometimes technical, and occasionally vague. Include specific details like error messages, device models, service types, and technical identifiers (phone numbers, invoice references, subscription IDs like SUB123xxxx, order numbers like ON123xxxxx, etc.). Don't be too verbose - match the real examples provided.
    
    - "actionsTaken": An array of support staff comments documenting investigation steps, formatted as separate entries to simulate a chronological work log. Include:
        * Updates between different support team members
        * Technical investigation steps (system checks, data verification)
        * References to related tickets (like "INCE12345" or "DER-12345")
        * Team communications ("Forwarding to backend team to check...")
        * Status updates throughout the resolution process
        * Details about attempted fixes or workarounds
        * Sometimes include staff names/identities like "Hi Tom, I checked the customer's account and..."
    
    - "resolution": The final resolution message visible to the customer. This should be technical when appropriate but understandable. Include:
        * Specific fix details (e.g., "Fix was deployed to production on 23.4)
        * Root cause explanation suitable for customer communication (system restarts, code fixes, data corrections)
        * Occasionally note it's "working as designed" for cases that aren't actual bugs
        * Sometimes include statement about closing the ticket
        * Sometimes include "if you have further issues, please reopen this ticket"
        * Include remedial actions, if applicable, like sending replacement items for delivery issues
    
    - "rca": The internal, detailed root cause analysis not visible to customers. This should be highly technical and explain:
        * The exact technical problem found (code issues, database errors, configuration problems)
        * Which systems were affected (specific references to Online Self-service, Salesforce, etc.)
        * How the issue was fixed (code changes, data correction, configuration update)
        * References to specific classes, functions, or database tables where relevant
        * Categorization (e.g., "RCA Category: Code Issue", "RCA Category: Data Synchronization")

    Important requirements:
        - Generate exactly 5 JSON objects and output them as a JSON array.
        - Ensure diversity in issue types, language styles, and complexity.
        - Make the data realistic - brief when appropriate, detailed when necessary.
        - Some outputs should simulate false positive scenarios (where the issue is user error or misunderstanding).
        - For technical issues, include plausible UI errors, system details, and user environments.
        - Use realistic telecom-specific terminology and systems
        - Some incidents should reference multiple systems and integration points.
        - Vary the complexity of resolution - some simple fixes, some complex investigations.
        
    EXAMPLE JSON OUTPUT:
    
    {
        "datasets":
        [
            {
                "issueDescription": "Customer reported that they cannot redeem their Device in Employee's self-service portal. When they click 'Confirm' in the redemption flow, they get error 'Something went wrong'. Device info: Samsung Galaxy S22, IMEI: 123451234512345, SUB123455783.",
                "actionsTaken":
                [
                    "Initial assessment: Verified customer details in Salesforce. Subscription SUB123455783 is active and user should be able to redeem device. Will try to reproduce issue by impersonating.",
                    "Reproduced the issue when impersonating customer. After clicking 'Confirm' in redemption flow, system throws HTTP 500 error. Will escalate to SELF-SERVICE development team.",
                    "Hi John, I checked the logs and found that the redemption API is failing because the device status in database doesn't match expected state. The extension period record was duplicated during last night's batch run. Jira ticket created: DER-12345.",
                    "Development team has deployed fix to UAT for testing. Will verify tomorrow after deployment."
                ],
                "resolution": "Issue with device redemption has been resolved. There was a technical error in the system where your device had duplicate extension period records, which prevented the redemption from completing. The database has been corrected and you should now be able to complete the redemption successfully. If you encounter any further issues, please contact customer service.",
                "rca": "RCA Category: Data Integrity Issue. Duplicate extension period order was created during nightly batch processing (OrderExtensionBatchJob), causing duplicate subscription records in the subscription_extension table. This made the redemption API fail with a constraint violation when attempting to update the device status. Fix involved removing the duplicate record and adding a unique constraint to prevent future occurrences. Root batch job issue being addressed in separate ticket DER-45678."
            },
            {
                "issueDescription": "Main user can't update Device as a Service catalog for ABC Corp (1234569-7). When trying to add accessories to device list, over 1800 accessories appear and when selecting options, the bottom navigation bar disappears making it impossible to save changes.",
                "actionsTaken":
                [
                    "Checked the customer's account in Salesforce. Customer has 4 device catalogs with correct permissions.",
                    "Attempted to reproduce by impersonating the main user. Problem confirmed - when accessing accessories section, UI loads 1800+ accessories and selecting/deselecting makes the navigation bar disappear.",
                    "Hi Maria, I checked with the Employee self-service development team. This appears to be a UI rendering issue when too many items are displayed. There's a known limit of 500 items before pagination should be enabled.",
                    "Escalating to front-end development team with priority medium as there's a workaround (creating a new list instead of modifying existing one).",
                    "Development has acknowledged issue as bug DER-12345 and will implement pagination for accessory selection in next sprint."
                ],
                "resolution": "We identified the issue with the Device as a Service catalog management. When a catalog contains too many accessories (in this case over 1800), the user interface has difficulty handling the display. As a temporary workaround, you can create a new device list with only the accessories you need rather than modifying the existing one. Our development team is implementing a permanent fix that will be deployed in the next system update scheduled for next week.",
                "rca": "RCA Category: UI Performance Limitation. The accessories selection component in EOE does not implement pagination and attempts to load all available accessories at once (1800+ in this case). This causes browser rendering issues, particularly with the floating action button (FAB) which disappears due to DOM re-rendering when selections change. Fix involves implementing pagination with max 100 items per page and keeping the FAB in a fixed position regardless of content changes. Change deployed in PR #456 to deviceCatalogSelectionComponent.js."
            },
            {
                "issueDescription": "Invoices are not visible in OmaOrange (both new and classic versions). Company: Tammer Industries Oy, Business ID: 1234567-8, Billing Account: 123451234. Last invoice sent 3.3.2025 and should be visible by now. Checked with multiple admin users with same result.",
                "actionsTaken":
                [
                    "Verified customer details in Salesforce. Billing Account 123451234 is active and has 12 invoices issued in the last 6 months that should be visible.",
                    "Checked invoice delivery settings in CRM - electronic invoice delivery is enabled. Verified that PDF versions of invoices exist in document storage system.",
                    "Checked the DOC API logs and found that when trying to fetch invoice data for this customer, API returns HTTP 500 error. The error seems related to special characters in customer name field. Escalating to billing integration team.",
                    "Billing team confirms there's an issue with the DOC invoice retrieval endpoint failing for customers with scandic characters in certain fields. Related to recent character encoding change in API.",
                    "Tested fix in UAT environment by adding proper UTF-8 encoding handling. Invoice data now retrievable for test accounts with scandic characters.",
                    "Fix deployed to production on 10.3.2025. Verified customer can now see invoices by impersonating admin user."
                ],
                "resolution": "Issue related to invoice visibility is now resolved and fix is deployed to production. The problem was related to special characters in company information that were not being correctly processed by our system. We have implemented proper character encoding handling, and you should now be able to view all your invoices in both the new and classic OmaOrange portals. If you continue experiencing any issues with invoice visibility, please contact customer service.",
                "rca": "RCA Category: Integration Error. The issue was caused by improper character encoding handling in the DOC invoice retrieval API. When company data contained non-ASCII characters (scandic characters like 'ä', 'ö'), the API request header was set as 'Accept: application/json' but without proper UTF-8 encoding specification. This caused the backend system to fail with HTTP 500 when trying to process these characters. Fix implemented in PR #789 to online-ui-api module, adding proper Content-Type header with charset=UTF-8 specification. Root cause was recent migration of backend system that changed default character encoding behavior."
            },
            {
                "issueDescription": "Mobile service outage affecting multiple users in our company since 10:15 AM. Users unable to make or receive calls, but data services working normally. Approximately 15 subscriptions affected, all on corporate plan. Example number: 1234567890.",
                "actionsTaken":
                [
                    "Checked network status - no reported outages in customer's area. Verified subscription statuses in billing system - all active and paid.",
                    "Confirmed issue affects only voice services on specific number range. All affected numbers are in the range 12345xxxxx and on the same corporate account.",
                    "Traced issue to recent bulk service change applied to customer's account yesterday at 18:00. Voice service package 'Corporate Voice Max' was incorrectly deactivated during routine upgrade.",
                    "Contacted network operations team to restore voice services without requiring individual subscription updates.",
                    "Network team has identified the affected service profile in HLR and is implementing emergency fix to restore voice capabilities without changing subscription records.",
                    "Service restored at 14:45. All test calls successful. Will monitor for next 24 hours to ensure stability."
                ],
                "resolution": "The mobile voice service outage affecting your corporate subscriptions has been resolved. The issue was caused by an incorrect service configuration change applied during yesterday's scheduled system maintenance. Voice services have been fully restored to all affected numbers, and we have implemented additional verification steps to prevent similar incidents in the future. We apologize for the inconvenience this caused your business operations.",
                "rca": "RCA Category: Provisioning Error. During scheduled maintenance on 10.3.2025, an automated batch job (ServicePackageUpdater) incorrectly identified the customer's Corporate Voice Max service package for deactivation due to an error in the upgrade path configuration. The deactivation command was sent to the HLR but the corresponding activation of the replacement service failed due to a timeout. This left approximately 15 subscriptions with active data services but no voice capability. Fix involved direct HLR service profile restoration rather than subscription-level changes to minimize recovery time. Long-term fix implemented in ServicePackageUpdater to require validation of service continuity before applying bulk changes and adding automatic rollback on partial failures. Maintenance procedure also updated to include explicit verification of voice services after similar upgrades."
            }
        ]
    }
"""

generator = "gemini"  # Options: "openai", "deepseek", "gemini"


def main():
    total_requests = 0
    minute_requests = 0
    minute_start_time = time.time()

    while total_requests < 100:
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

        scenario = get_scenario_to_generate("DESC" if generator == "gemini" else "ASC")
        if scenario is None:
            print("No more scenarios to generate. Exiting.")
            break

        print(
            f"Generating datasets for scenario {scenario['scenario']} with id {scenario['id']}..."
        )

        try:
            prompt = f"Scenario: {scenario['scenario']}"
            match generator:
                case "openai":
                    datasets = generate_openai(system_prompt, prompt, DatasetList)
                case "deepseek":
                    datasets = generate_deepseek(system_prompt, prompt, DatasetList)
                case "gemini":
                    datasets = generate_gemini(system_prompt, prompt, DatasetList)
                case _:
                    raise ValueError(f"Unknown generator: {generator}")

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
