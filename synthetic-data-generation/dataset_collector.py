import json
from typing import List

from pydantic import BaseModel

from data_generator import DatasetList
from store import get_all_scenario_datasets


class PromptContent(BaseModel):
    issueDescription: str
    actionsTaken: List[str]


class CompletionContent(BaseModel):
    rca: str
    resolution: str


class TrainingExample(BaseModel):
    prompt: str
    completion: str


prompt_template = """
You are an AI assistant that helps with incident root-cause analysis.
Below is an incident with two fields: "issueDescription" and "actionsTaken."

**Your task**:
1. Read the issue description and actions taken.
2. Generate a probable root cause ("rca") and a recommended resolution ("resolution").
3. Return the result **only** as valid JSON with keys "rca" and "resolution."
"""


def main():
    training_examples = []
    datasets_raw = get_all_scenario_datasets()

    for dataset_raw in datasets_raw:
        dataset_list = DatasetList.model_validate_json(dataset_raw)
        for dataset in dataset_list.datasets:
            prompt_content = PromptContent(
                issueDescription=dataset.issueDescription,
                actionsTaken=dataset.actionsTaken,
            )
            completion_content = CompletionContent(
                rca=dataset.rca, resolution=dataset.resolution
            )
            training_examples.append(
                TrainingExample(
                    prompt=f"{prompt_template}\n{prompt_content.model_dump_json()}",
                    completion=completion_content.model_dump_json(),
                )
            )
    training_data = [example.model_dump() for example in training_examples]
    with open("../fine-tune/dataset.json", "w") as f:
        json.dump(training_data, f, indent=4)


if __name__ == "__main__":
    main()
