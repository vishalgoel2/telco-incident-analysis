import torch
from peft import get_peft_model, prepare_model_for_kbit_training, PeftModel
from tqdm import tqdm
from transformers import (
    BitsAndBytesConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
)
from transformers import Trainer


def load_tokenizer(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer


def load_model(model_id: str, use_8bit: bool):
    if use_8bit:
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_compute_dtype=torch.float16,
            bnb_8bit_use_double_quant=True,
            bnb_8bit_quant_type="nf4",
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
        )
        return prepare_model_for_kbit_training(model)
    else:
        return AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=torch.float16, device_map="auto"
        )


def apply_lora_config(model, lora_config):
    model = get_peft_model(model, lora_config)
    return model


def load_finetuned_model(base_model, adapter_path):
    return PeftModel.from_pretrained(base_model, adapter_path)


def train_and_save_adapter(
    model, tokenized_datasets, training_args, data_collator, output_dir
):
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
    )
    print("Starting fine-tuning...")
    trainer.train()
    print(f"Saving model adapters to {output_dir}...")
    model.save_pretrained(output_dir)


def generate_output(model, tokenizer, input_prompt, max_new_tokens=100):
    inputs = tokenizer(input_prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False,
        )
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if output_text.startswith(input_prompt):
        return output_text[len(input_prompt) :].strip()
    else:
        return output_text


def run_inference(model, tokenizer, datasets, model_name="Base Model"):
    results = []
    print(f"\n--- Running inference with {model_name} ---")
    for i, dataset in enumerate(tqdm(datasets)):
        input_text = dataset["prompt"]
        expected_output = dataset["completion"]
        generated_text = generate_output(model, tokenizer, input_text)
        results.append(
            {
                "example_id": i + 1,
                "prompt": input_text,
                "expected": expected_output,
                "generated": generated_text,
                "model": model_name,
            }
        )
    return results
