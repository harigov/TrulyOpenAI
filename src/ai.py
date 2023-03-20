import os
from diffusers import StableDiffusionPipeline
from langchain.llms import OpenAIChat
import torch
import whisper

CHAT_MODEL_NAME = "gpt-3.5-turbo"
CHAT_PROMPT = """
"""

def chat_completion(messages):
    prefix_messages = [
        {"role": "system", "content": CHAT_PROMPT},
    ]
    prefix_messages.extend(messages[:-1])
    chat_llm = OpenAIChat(model_name=CHAT_MODEL_NAME,
                          prefix_messages=prefix_messages,
                          openai_api_key=os.environ.get("OPENAI_API_KEY"))
    return chat_llm(messages[-1]['content'])

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
