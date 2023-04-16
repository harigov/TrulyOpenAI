from diffusers import StableDiffusionPipeline
from langchain.llms import OpenAIChat
import llamacpp
import os
import sys
import torch
import whisper

CHAT_MODEL_NAME = "gpt-3.5-turbo"
CHAT_PROMPT = """
"""
LLAMA_MODEL_PATH = ""

def chat_completion(messages):
    prefix_messages = [
        {"role": "system", "content": CHAT_PROMPT},
    ]
    prefix_messages.extend(messages[:-1])
    chat_llm = OpenAIChat(model_name=CHAT_MODEL_NAME,
                          prefix_messages=prefix_messages,
                          openai_api_key=os.environ.get("OPENAI_API_KEY"))
    return chat_llm(messages[-1]['content'])

def alpaca_chat_completion(messages):
    params = llamacpp.gpt_params(
        LLAMA_MODEL_PATH,  # llama_model,
        512,  # ctx_size
        100,  # n_predict
        40,  # top_k
        0.95,  # top_p
        0.85,  # temp
        1.30,  # repeat_penalty
        -1,  # seed
        8,  # threads
        64,  # repeat_last_n
        8,  # batch_size
    )
    model = llamacpp.PyLLAMA(params)
    model.add_bos()     # Adds "beginning of string" token
    model.update_input("A llama is a")
    model.print_startup_stats()
    model.prepare_context()

    model.ingest_all_pending_input(True)
    while not model.is_finished():
        text, is_finished = model.infer_text()
        print(text, end="")

        if is_finished:
            break

    # Flush stdout
    sys.stdout.flush()

    model.print_end_stats()

def image_generation(prompt, size="512x512"):
    # Load the pre-trained stable diffusion model from Hugging Face
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
    pipe.to("cuda")
    return pipe(prompt).images[0]

def voice_transcription(prompt, model="whisper-1", temperature=0, language=None):
    # Load the pre-trained whisper model from Hugging Face
    whisper_model = whisper.Whisper.from_pretrained(model, revision="fp16", torch_dtype=torch.float16)
    whisper_model.to("cuda")
    return whisper_model(prompt, temperature=temperature, language=language)
