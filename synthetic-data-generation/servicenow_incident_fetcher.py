import getpass

import pandas as pd
import requests


def main():
    instance_url = input(
        "ServiceNow instance URL (e.g., https://yourinstance.service-now.com): "
    )
    username = input("ServiceNow username: ")
    password = getpass.getpass("ServiceNow password: ")
    incident_ids = input("Comma-separated list of incident IDs: ")

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update(
        {"Accept": "application/json", "Content-Type": "application/json"}
    )

    results = []
    for incident_id in incident_ids.split(","):
        print(f"Fetching data for incident: {incident_id}")
        response = session.get(
            f"{instance_url}/api/now/table/incident?sysparm_query=number={incident_id.strip()}&sysparm_display_value=true"
        )
        response.raise_for_status()
        data = response.json()
        if data["result"] and len(data["result"]) > 0:
            incident_data = data["result"][0]
            results.append(
                {
                    "incident_id": incident_id.strip(),
                    "short_description": incident_data.get("short_description"),
                    "description": incident_data.get("description"),
                    "comments_and_work_notes": incident_data.get(
                        "comments_and_work_notes"
                    ),
                    "close_notes": incident_data.get("close_notes"),
                    "u_root_cause": incident_data.get("u_root_cause"),
                }
            )
    rows = pd.DataFrame(results)
    with pd.ExcelWriter("incident_data.xlsx") as writer:
        rows.to_excel(writer, sheet_name="Incident Overview", index=False)


if __name__ == "__main__":
    main()
