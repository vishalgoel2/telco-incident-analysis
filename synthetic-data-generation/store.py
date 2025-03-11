from typing import List

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

collection_name = "telco-incident-data"

cred = credentials.Certificate("../secret/firestore_sa.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def insert_scenarios(scenarios: List[str]):
    story_collection = db.collection(collection_name)
    for scenario in scenarios:
        story_collection.add({"scenario": scenario})


def get_scenario_to_generate():
    query = db.collection(collection_name).where(
        filter=FieldFilter(field_path="generated", op_string="==", value=False)
    )
    scenarios = query.limit(1).stream()
    matching_scenarios = [
        {"id": scenario.id, **scenario.to_dict()} for scenario in scenarios
    ]
    return matching_scenarios[0] if matching_scenarios else None


def update_scenario(scenario, datasets):
    scenario["dataset"] = datasets.model_dump_json()
    scenario["generated"] = True
    db.collection(collection_name).document(scenario["id"]).update(scenario)


def get_all_scenario_datasets(limit: int = 200) -> List[str]:
    query = db.collection(collection_name).limit(limit)
    scenarios = query.stream()

    datasets = []
    for scenario in scenarios:
        scenario_data = scenario.to_dict()
        if "dataset" in scenario_data and scenario_data["dataset"]:
            datasets.append(scenario_data["dataset"])

    return datasets
