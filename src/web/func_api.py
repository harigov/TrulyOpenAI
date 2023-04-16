import json
from flask import Flask, request
from flask_restful import Resource, Api
from langchain.llms import OpenAIChat
import requests

import ai

class ChatCompletion(Resource):
    def post(self):
        req_data = request.get_json()
        response = ai.chat_completion(req_data.get('messages'))
        return json.loads(response)

class ImageGeneration(Resource):
    def post(self):
        req_data = request.get_json()
        response = ai.image_generation(req_data.get('prompt'), req_data.get('size', '512x512'))
        return json.loads(response)

class AudioTranscription(Resource):
    def post(self):
        # Extract request parameters
        req_data = request.get_json()

        # Prepare the file
        audio_url = req_data.get("file")
        audio_content = requests.get(audio_url).content

        return ai.voice_transcription(audio_content)

def register_api(api):
    # Add the chat completion endpoint
    api.add_resource(ChatCompletion, '/v1/chat/completions')

    # Add the image generation endpoint
    api.add_resource(ImageGeneration, '/v1/images/generations')

    # Add the audio transcription endpoint
    api.add_resource(AudioTranscription, '/v1/audio/transcriptions')

