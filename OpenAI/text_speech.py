import os
from uuid import uuid4
import hashlib

from django.conf import settings
from openai import OpenAI


def text_to_speech(text, voice):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="opus"
    )
    unique_filename = f"{uuid4()}.opus"
    output_file = os.path.join(settings.MEDIA_ROOT, voice, unique_filename)

    with open(output_file, 'wb') as f:
        f.write(response.read())

    return unique_filename


def check_existing_audio(description, voice):
    voice_directory = os.path.join(settings.MEDIA_ROOT, voice.lower())
    if not os.path.exists(voice_directory):
        os.makedirs(voice_directory)

    description_hash = hashlib.md5(description.encode()).hexdigest()
    existing_file = os.path.join(voice_directory, f"{description_hash}.opus")

    if os.path.exists(existing_file):
        return os.path.join(settings.MEDIA_URL, voice.lower(), f"{description_hash}.opus")
    else:
        return None
