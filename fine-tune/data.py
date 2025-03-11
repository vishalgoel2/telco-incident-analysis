import json

import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import DataCollatorForLanguageModeling


def load_dataset(dataset_file):
    print(f"Loading dataset from {dataset_file}...")
    with open(dataset_file, "r") as f:
        data = json.load(f)
    dataset = Dataset.from_list(data)
    return dataset


def prepare_datasets(dataset):
    # 80% train, 16% validation, 4% test split
    split_dataset = dataset.train_test_split(test_size=0.2, seed=42)
    test_val = split_dataset["test"].train_test_split(test_size=0.2, seed=42)
    dataset_dict = DatasetDict(
        {
            "train": split_dataset["train"],
            "validation": test_val["test"],
            "test": test_val["train"],
        }
    )
    return dataset_dict


def get_inference_examples(dataset_dict):
    return dataset_dict["test"].select(range(10))


def tokenize_dataset(dataset_dict, tokenizer):
    def tokenize_function(examples):
        concatenated_texts = []
        for i in range(len(examples["prompt"])):
            prompt = examples["prompt"][i]
            completion = examples["completion"][i]
            full_text = prompt.strip() + "\n" + completion.strip()
            concatenated_texts.append(full_text)
        return tokenizer(concatenated_texts, truncation=True, max_length=512)

    print("Tokenizing datasets...")
    tokenized_datasets = dataset_dict.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset_dict["train"].column_names,
    )
    return tokenized_datasets


def create_data_collator(tokenizer):
    return DataCollatorForLanguageModeling(tokenizer, mlm=False)


def save_results(results, filename):
    pd.DataFrame(results).to_csv(filename, index=False)
    print(f"Results saved to {filename}")
