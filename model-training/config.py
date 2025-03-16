from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from peft import LoraConfig
from transformers import TrainingArguments


@dataclass
class ModelConfig:
    model_id: str
    model_name: str
    precision: str
    use_8bit: bool
    lora_config: LoraConfig
    training_args: TrainingArguments


DEFAULT_SMALL_MODEL_LORA = {
    "r": 16,
    "lora_alpha": 32,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM",
}

DEFAULT_LARGE_MODEL_LORA = {
    "r": 32,
    "lora_alpha": 64,
    "target_modules": [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    "lora_dropout": 0.1,
    "bias": "none",
    "task_type": "CAUSAL_LM",
}

DEFAULT_TRAINING_ARGS = {
    "logging_steps": 50,
    "evaluation_strategy": "steps",
    "eval_steps": 100,
    "save_steps": 100,
    "save_total_limit": 3,
    "load_best_model_at_end": True,
    "metric_for_best_model": "loss",
    "greater_is_better": False,
    "report_to": "none",
}


def create_model_config(
    display_name: str,
    model_id: str,
    model_name: str,
    precision: str,
    is_large_model: bool = False,
    lora_overrides: Optional[Dict[str, Any]] = None,
    training_args_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    base_lora = DEFAULT_LARGE_MODEL_LORA if is_large_model else DEFAULT_SMALL_MODEL_LORA
    lora_params = {**base_lora}
    if lora_overrides:
        lora_params.update(lora_overrides)
    is_fp16 = precision == "fp16"
    if is_large_model:
        batch_size = 8 if is_fp16 else 16
        grad_accum = 4 if is_fp16 else 2
        lr = 3e-4
        epochs = 3 if is_fp16 else 4
    else:
        batch_size = 16 if is_fp16 else 32
        grad_accum = 1
        lr = 5e-4
        epochs = 6
    base_training_args = {
        **DEFAULT_TRAINING_ARGS,
        "output_dir": f"./lora_finetuned_{model_name}_{precision}",
        "per_device_train_batch_size": batch_size,
        "per_device_eval_batch_size": batch_size,
        "gradient_accumulation_steps": grad_accum,
        "learning_rate": lr,
        "num_train_epochs": epochs,
        "fp16": is_fp16,
    }
    if training_args_overrides:
        base_training_args.update(training_args_overrides)
    return {
        "display_name": display_name,
        "model_id": model_id,
        "model_name": model_name,
        "precision": precision,
        "lora_config": LoraConfig(**lora_params),
        "training_args": TrainingArguments(**base_training_args),
    }


MODEL_CONFIGS = {
    1: create_model_config(
        display_name="Llama 3.2 3B (int8)",
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        model_name="llama-3.2-3b",
        precision="int8",
    ),
    2: create_model_config(
        display_name="Llama 3.2 3B (fp16)",
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        model_name="llama-3.2-3b",
        precision="fp16",
        training_args_overrides={
            "per_device_train_batch_size": 16,
            "per_device_eval_batch_size": 16,
        },
    ),
    3: create_model_config(
        display_name="Llama 3.1 8B (int8)",
        model_id="meta-llama/Llama-3.1-8B-Instruct",
        model_name="llama-3.1-8b",
        precision="int8",
        is_large_model=True,
    ),
    4: create_model_config(
        display_name="Llama 3.1 8B (fp16)",
        model_id="meta-llama/Llama-3.1-8B-Instruct",
        model_name="llama-3.1-8b",
        precision="fp16",
        is_large_model=True,
    ),
    5: create_model_config(
        display_name="Phi 4 Mini (int8)",
        model_id="microsoft/Phi-4-mini-instruct",
        model_name="phi-4-mini",
        precision="int8",
    ),
    6: create_model_config(
        display_name="Phi 4 Mini (fp16)",
        model_id="microsoft/Phi-4-mini-instruct",
        model_name="phi-4-mini",
        precision="fp16",
        training_args_overrides={
            "per_device_train_batch_size": 24,
            "per_device_eval_batch_size": 24,
        },
    ),
    7: create_model_config(
        display_name="Mistral Nemo Instruct (int8)",
        model_id="mistralai/Mistral-Nemo-Instruct-2407",
        model_name="mistral-nemo",
        precision="int8",
        is_large_model=True,
    ),
    8: create_model_config(
        display_name="Mistral Nemo Instruct (fp16)",
        model_id="mistralai/Mistral-Nemo-Instruct-2407",
        model_name="mistral-nemo",
        precision="fp16",
        is_large_model=True,
    ),
    9: create_model_config(
        display_name="Gemma 3 12B (int8)",
        model_id="google/gemma-3-12b-it",
        model_name="gemma-3-12b",
        precision="int8",
        is_large_model=True,
        training_args_overrides={
            "per_device_train_batch_size": 8,
            "per_device_eval_batch_size": 8,
            "gradient_accumulation_steps": 4,
        },
    ),
    10: create_model_config(
        display_name="Gemma 3 12B (fp16)",
        model_id="google/gemma-3-12b-it",
        model_name="gemma-3-12b",
        precision="fp16",
        is_large_model=True,
        training_args_overrides={
            "per_device_train_batch_size": 4,
            "per_device_eval_batch_size": 4,
            "gradient_accumulation_steps": 8,
        },
    ),
}


def select_model() -> ModelConfig:
    print("Select model to use:")
    for choice, config in MODEL_CONFIGS.items():
        print(f"{choice}. {config['display_name']}")

    max_choice = max(MODEL_CONFIGS.keys())
    while True:
        try:
            choice = int(input(f"Enter your choice (1-{max_choice}): "))
            if choice not in MODEL_CONFIGS:
                print(
                    f"Invalid choice. Please enter a number between 1 and {max_choice}."
                )
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    config = MODEL_CONFIGS[choice]
    return ModelConfig(
        model_id=config["model_id"],
        model_name=config["model_name"],
        precision=config["precision"],
        use_8bit=config["precision"] == "int8",
        lora_config=config["lora_config"],
        training_args=config["training_args"],
    )


def requires_auth(model_name: str) -> bool:
    return (
        model_name.startswith("llama")
        or model_name == "mistral-nemo"
        or model_name == "gemma-3-12b"
    )
