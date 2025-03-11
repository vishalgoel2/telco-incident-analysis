from dataclasses import dataclass

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


MODEL_CONFIGS = {
    1: {
        "display_name": "Llama 3.2 3B (int8)",
        "model_id": "meta-llama/Llama-3.2-3B-Instruct",
        "model_name": "llama-3.2-3b",
        "precision": "int8",
        "lora_config": LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_llama_3.2_3b_int8",
            per_device_train_batch_size=32,
            per_device_eval_batch_size=32,
            gradient_accumulation_steps=1,
            learning_rate=5e-4,
            num_train_epochs=4,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=False,
            report_to="none",
        ),
    },
    2: {
        "display_name": "Llama 3.2 3B (fp16)",
        "model_id": "meta-llama/Llama-3.2-3B-Instruct",
        "model_name": "llama-3.2-3b",
        "precision": "fp16",
        "lora_config": LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_llama_3.2_3b_fp16",
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            gradient_accumulation_steps=1,
            learning_rate=5e-4,
            num_train_epochs=4,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=True,
            report_to="none",
        ),
    },
    3: {
        "display_name": "Llama 3.1 8B (int8)",
        "model_id": "meta-llama/Llama-3.1-8B-Instruct",
        "model_name": "llama-3.1-8b",
        "precision": "int8",
        "lora_config": LoraConfig(
            r=32,
            lora_alpha=64,
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_llama_3.1_8b_int8",
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            gradient_accumulation_steps=2,
            learning_rate=3e-4,
            num_train_epochs=3,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=False,
            report_to="none",
        ),
    },
    4: {
        "display_name": "Llama 3.1 8B (fp16)",
        "model_id": "meta-llama/Llama-3.1-8B-Instruct",
        "model_name": "llama-3.1-8b",
        "precision": "fp16",
        "lora_config": LoraConfig(
            r=32,
            lora_alpha=64,
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_llama_3.1_8b_fp16",
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            gradient_accumulation_steps=4,
            learning_rate=3e-4,
            num_train_epochs=3,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=True,
            report_to="none",
        ),
    },
    5: {
        "display_name": "Phi 4 Mini (int8)",
        "model_id": "microsoft/Phi-4-mini-instruct",
        "model_name": "phi-4-mini",
        "precision": "int8",
        "lora_config": LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_phi_4_mini_instruct_int8",
            per_device_train_batch_size=32,
            per_device_eval_batch_size=32,
            gradient_accumulation_steps=1,
            learning_rate=5e-4,
            num_train_epochs=4,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=False,
            report_to="none",
        ),
    },
    6: {
        "display_name": "Phi 4 Mini (fp16)",
        "model_id": "microsoft/Phi-4-mini-instruct",
        "model_name": "phi-4-mini",
        "precision": "fp16",
        "lora_config": LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        ),
        "training_args": TrainingArguments(
            output_dir="./lora_finetuned_phi_4_mini_instruct_fp16",
            per_device_train_batch_size=24,
            per_device_eval_batch_size=24,
            gradient_accumulation_steps=1,
            learning_rate=5e-4,
            num_train_epochs=4,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=100,
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False,
            fp16=True,
            report_to="none",
        ),
    },
}


def select_model() -> ModelConfig:
    print("Select model to use:")
    for choice, config in MODEL_CONFIGS.items():
        print(f"{choice}. {config['display_name']}")
    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if choice not in MODEL_CONFIGS:
                print("Invalid choice. Please enter a number between 1 and 6.")
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
    return model_name.startswith("llama")
