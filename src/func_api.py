import json
from flask import Flask, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class ChatCompletion(Resource):
    def post(self):
        # Extract request parameters
        req_data = request.get_json()

        # Call OpenAI API with the request parameters
        response = openai.Completion.create(
            engine=req_data.get("model"),
            messages=req_data.get("messages"),
            n=req_data.get("n", 1),
            temperature=req_data.get("temperature", 1),
            top_p=req_data.get("top_p", 1),
            stream=req_data.get("stream", False),
            stop=req_data.get("stop", None),
            max_tokens=req_data.get("max_tokens", None),
            presence_penalty=req_data.get("presence_penalty", 0),
            frequency_penalty=req_data.get("frequency_penalty", 0),
            logit_bias=req_data.get("logit_bias", None),
            user=req_data.get("user", None),
        )

        # Return the response from OpenAI API
        return json.loads(response)

class ImageGeneration(Resource):
    def post(self):
        # Extract request parameters
        req_data = request.get_json()

        # Call OpenAI API with the request parameters
        response = openai.Image.create(
            prompt=req_data.get("prompt"),
            n=req_data.get("n", 1),
            size=req_data.get("size", "1024x1024"),
            response_format=req_data.get("response_format", "url"),
            user=req_data.get("user", None),
        )

        # Return the response from OpenAI API
        return json.loads(response)

class AudioTranscription(Resource):
    def post(self):
        # Extract request parameters
        req_data = request.get_json()

        # Prepare the file
        audio_url = req_data.get("file")
        audio_content = requests.get(audio_url).content

        # Call OpenAI API with the request parameters
        response = openai.Audio.create(
            file=audio_content,
            model=req_data.get("model", "whisper-1"),
            prompt=req_data.get("prompt", None),
            response_format=req_data.get("response_format", "json"),
            temperature=req_data.get("temperature", 0),
            language=req_data.get("language", None),
        )

        # Return the response from OpenAI API
        return json.loads(response)


def register_api(app):
    # Add the chat completion endpoint
    api.add_resource(ChatCompletion, '/v1/chat/completions')

    # Add the image generation endpoint
    api.add_resource(ImageGeneration, '/v1/images/generations')

    # Add the audio transcription endpoint
    api.add_resource(AudioTranscription, '/v1/audio/transcriptions')

