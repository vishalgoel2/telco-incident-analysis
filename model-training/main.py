from config import select_model, requires_auth
from data import (
    load_dataset,
    prepare_datasets,
    get_inference_examples,
    tokenize_dataset,
    create_data_collator,
    save_results,
)
from models import (
    load_tokenizer,
    load_model,
    apply_lora_config,
    load_finetuned_model,
    train_and_save_adapter,
    run_inference,
)
from utils import authenticate_huggingface, clean_memory, get_output_paths


def main():
    model_config = select_model()
    print(
        f"Selected model: {model_config.model_id} with {model_config.precision} precision"
    )

    if requires_auth(model_config.model_name):
        authenticate_huggingface()

    dataset = load_dataset("dataset.json")
    dataset_dict = prepare_datasets(dataset)
    inference_examples = get_inference_examples(dataset_dict)

    tokenizer = load_tokenizer(model_config.model_id)

    paths = get_output_paths(model_config.model_name, model_config.precision)

    print("Loading base model for initial inference...")
    base_model = load_model(model_config.model_id, model_config.use_8bit)
    base_results = run_inference(
        base_model, tokenizer, inference_examples, f"{model_config.model_name} - Base"
    )
    save_results(base_results, paths["results"])

    del base_model
    clean_memory()

    print("Loading model for fine-tuning...")
    model = load_model(model_config.model_id, model_config.use_8bit)
    print("Applying LoRA configuration...")
    model = apply_lora_config(model, model_config.lora_config)
    print("LoRA model configuration:")
    model.print_trainable_parameters()
    tokenized_datasets = tokenize_dataset(dataset_dict, tokenizer)
    data_collator = create_data_collator(tokenizer)
    train_and_save_adapter(
        model,
        tokenized_datasets,
        model_config.training_args,
        data_collator,
        paths["lora_output_dir"],
    )

    del model
    clean_memory()

    print("Loading fine-tuned model for inference...")
    base_model = load_model(model_config.model_id, model_config.use_8bit)
    lora_model = load_finetuned_model(base_model, paths["lora_output_dir"])
    lora_results = run_inference(
        lora_model,
        tokenizer,
        inference_examples,
        f"{model_config.model_name} - Fine-tuned",
    )
    all_results = base_results + lora_results
    save_results(all_results, paths["results"])


if __name__ == "__main__":
    main()
