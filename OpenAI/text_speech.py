import os
from uuid import uuid4
import hashlib
import logging

from django.conf import settings
import httpx
from openai import OpenAI


logger = logging.getLogger(__name__)
SUPPORTED_VOICES = {'onyx', 'nova'}


def _build_openai_client():
    if not settings.OPENAI_API_KEY:
        raise ValueError('Missing OPENAI_KEY environment variable.')

    try:
        return OpenAI(api_key=settings.OPENAI_API_KEY)
    except TypeError as exc:
        if 'proxies' not in str(exc):
            raise
        logger.warning('OpenAI/httpx compatibility issue detected. Retrying with explicit httpx client.')
        return OpenAI(api_key=settings.OPENAI_API_KEY, http_client=httpx.Client())


def text_to_speech(text, voice):
    normalized_voice = (voice or '').lower()
    if normalized_voice not in SUPPORTED_VOICES:
        raise ValueError(f'Unsupported voice: {voice}')

    client = _build_openai_client()
    response = client.audio.speech.create(
        model="tts-1",
        voice=normalized_voice,
        input=text,
        response_format="opus"
    )
    unique_filename = f"{uuid4()}.opus"
    output_file = os.path.join(settings.MEDIA_ROOT, normalized_voice, unique_filename)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

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
