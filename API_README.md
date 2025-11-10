# Edge TTS FastAPI

A FastAPI-based REST API for text-to-speech conversion using Microsoft Edge TTS.

## Running the API

```bash
# Activate virtual environment
source venv/bin/activate

# Run the FastAPI server
python fastapi_app.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Endpoints

### 1. GET `/voices`

List all available voices with their details.

**Example:**

```bash
curl http://localhost:8000/voices
```

### 2. GET `/voices/{voice_short_name}`

Get details about a specific voice.

**Example:**

```bash
curl http://localhost:8000/voices/en-US-AriaNeural
```

### 3. POST `/tts`

Convert text to speech by uploading a JSON file.

**JSON Structure:**

```json
{
  "text": "Your text here",
  "voice": "en-US-AriaNeural",
  "rate": 0,
  "volume": 0,
  "pitch": 0
}
```

**Parameters:**

- `text` (required): Text to convert to speech
- `voice` (optional): Voice short name (default: en-US-AriaNeural)
- `rate` (optional): Speech rate adjustment % (-50 to 50, default: 0)
- `volume` (optional): Volume adjustment % (-50 to 50, default: 0)
- `pitch` (optional): Pitch adjustment Hz (-20 to 20, default: 0)

**Example:**

```bash
# Upload JSON file
curl -X POST http://localhost:8000/tts \
  -F "file=@example_input.json" \
  --output output.mp3

# Override settings with query parameters
curl -X POST "http://localhost:8000/tts?rate=10&volume=5" \
  -F "file=@example_input.json" \
  --output output.mp3
```

### 4. POST `/tts/text`

Convert text to speech using query parameters (no file upload needed).

**Example:**

```bash
curl -X POST "http://localhost:8000/tts/text?text=Hello%20world&voice=en-US-AriaNeural&rate=0&volume=0&pitch=0" \
  --output output.mp3
```

## Query Parameters for `/tts` and `/tts/text`

- `voice`: Voice short name (e.g., "en-US-AriaNeural")
- `rate`: Speech rate adjustment (-50 to 50) - negative is slower, positive is faster
- `volume`: Volume adjustment (-50 to 50) - negative is quieter, positive is louder
- `pitch`: Pitch adjustment (-20 to 20) - negative is lower, positive is higher

## Popular Voices

- `en-US-AriaNeural` - Female, US English
- `en-US-GuyNeural` - Male, US English
- `en-GB-SoniaNeural` - Female, British English
- `en-GB-RyanNeural` - Male, British English
- `es-ES-ElviraNeural` - Female, Spanish (Spain)
- `fr-FR-DeniseNeural` - Female, French
- `de-DE-KatjaNeural` - Female, German
- `ja-JP-NanamiNeural` - Female, Japanese

Use the `/voices` endpoint to see all available voices.

## Python Client Example

```python
import requests

# Using JSON file
with open('example_input.json', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/tts',
        files={'file': f},
        params={'rate': 10, 'volume': 5}
    )

with open('output.mp3', 'wb') as f:
    f.write(response.content)

# Using text directly
response = requests.post(
    'http://localhost:8000/tts/text',
    params={
        'text': 'Hello, world!',
        'voice': 'en-US-AriaNeural',
        'rate': 0,
        'volume': 0,
        'pitch': 0
    }
)

with open('output.mp3', 'wb') as f:
    f.write(response.content)
```
