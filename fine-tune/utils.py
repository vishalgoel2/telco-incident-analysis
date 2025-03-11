import gc
import getpass

import torch
from huggingface_hub import login


def clean_memory():
    gc.collect()
    torch.cuda.empty_cache()


def authenticate_huggingface():
    print("\n--- Hugging Face Authentication ---")
    print("Meta Llama models require authentication with Hugging Face.")
    print("Your token will not be displayed or stored in command history.")
    hf_token = getpass.getpass("Enter your Hugging Face token: ")

    if hf_token.strip():
        login(token=hf_token)
        print(
            "Authentication submitted. If the token is valid, model loading will proceed."
        )
    else:
        print("No token provided. Model loading may fail if the models are gated.")
    del hf_token


def get_output_paths(model_name, precision):
    results_path = f"{model_name}_{precision}_results.csv"
    lora_output_dir = f"./lora_finetuned_{model_name}_{precision}"
    return {"results": results_path, "lora_output_dir": lora_output_dir}
