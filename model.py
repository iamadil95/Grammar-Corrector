import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer

MODEL_NAME = "vennify/t5-base-grammar-correction"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading grammar model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = T5ForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
)

model.to(device)
model.eval()

@torch.inference_mode()
def correct_grammar(text: str):

    if not text.strip():
        return text

    input_text = "grammar: " + text

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    ).to(device)

    outputs = model.generate(
        **inputs,
        max_length=256,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected