import json
from typing import List

from pydantic import BaseModel

from data_generator import DatasetList
from store import get_all_scenario_datasets


def main():
    insert_queries = []
    datasets_raw = get_all_scenario_datasets()
    for dataset_raw in datasets_raw:
        dataset_list = DatasetList.model_validate_json(dataset_raw)
        for dataset in dataset_list.datasets:
            issueDescription = dataset.issueDescription.replace("'", "''")
            actionsTaken = (
                (
                    "\n".join(dataset.actionsTaken)
                    if isinstance(dataset.actionsTaken, list)
                    else dataset.actionsTaken
                )
                .replace("'", "''")
                .replace('"', "")
            )
            rca = dataset.rca.replace("'", "''")
            resolution = dataset.resolution.replace("'", "''")
            insert_queries.append(
                f"INSERT INTO INCIDENT (description, actions_taken, rca, resolution, status) VALUES ('{issueDescription}', '{actionsTaken}', '{rca}', '{resolution}', 'CLOSED');"
            )
    with open("../service-now/backend/init.sql", "w") as f:
        f.write("\n".join(insert_queries))


if __name__ == "__main__":
    main()
