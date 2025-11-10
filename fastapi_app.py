from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
import edge_tts
import asyncio
import tempfile
import os
import json
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="Edge TTS API", description="Text-to-Speech API using Microsoft Edge TTS")

# Cache for voices
voices_cache = None

class TextInput(BaseModel):
    text: str

class VoiceSettings(BaseModel):
    voice: str
    rate: int = 0
    volume: int = 0
    pitch: int = 0

async def get_voices():
    global voices_cache
    if voices_cache is None:
        voices = await edge_tts.list_voices()
        voices_cache = {f"{v['ShortName']} - {v['Locale']} ({v['Gender']})": v['ShortName'] for v in voices}
    return voices_cache

@app.get("/")
async def root():
    return {
        "message": "Edge TTS API",
        "endpoints": {
            "POST /tts": "Convert text to speech (accepts JSON file)",
            "GET /voices": "List available voices",
            "GET /voices/{voice_name}": "Get specific voice details"
        }
    }

@app.get("/voices")
async def list_voices():
    """Get list of all available voices"""
    voices = await edge_tts.list_voices()
    return {
        "count": len(voices),
        "voices": [
            {
                "name": v['Name'],
                "short_name": v['ShortName'],
                "locale": v['Locale'],
                "gender": v['Gender'],
                "suggested_codec": v.get('SuggestedCodec', 'audio-24khz-48kbitrate-mono-mp3')
            }
            for v in voices
        ]
    }

@app.get("/voices/{voice_short_name}")
async def get_voice_info(voice_short_name: str):
    """Get information about a specific voice"""
    voices = await edge_tts.list_voices()
    for v in voices:
        if v['ShortName'] == voice_short_name:
            return {
                "name": v['Name'],
                "short_name": v['ShortName'],
                "locale": v['Locale'],
                "gender": v['Gender'],
                "suggested_codec": v.get('SuggestedCodec', 'audio-24khz-48kbitrate-mono-mp3')
            }
    raise HTTPException(status_code=404, detail="Voice not found")

@app.post("/tts")
async def text_to_speech_from_json(
    file: UploadFile = File(..., description="JSON file containing text and voice settings"),
    voice: Optional[str] = Query(None, description="Voice short name (overrides JSON)"),
    rate: Optional[int] = Query(None, ge=-50, le=50, description="Speech rate adjustment % (overrides JSON)"),
    volume: Optional[int] = Query(None, ge=-50, le=50, description="Volume adjustment % (overrides JSON)"),
    pitch: Optional[int] = Query(None, ge=-20, le=20, description="Pitch adjustment Hz (overrides JSON)")
):
    """
    Convert text to speech. Accepts a JSON file with the following structure:
    {
        "text": "Text to convert",
        "voice": "en-US-AriaNeural",  // optional
        "rate": 0,  // optional, range: -50 to 50
        "volume": 0,  // optional, range: -50 to 50
        "pitch": 0  // optional, range: -20 to 20
    }
    
    Query parameters override JSON values if provided.
    """
    # Validate file type
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    
    # Read and parse JSON
    try:
        content = await file.read()
        data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    
    # Extract parameters from JSON
    text = data.get('text', '')
    json_voice = data.get('voice', 'en-US-AriaNeural')
    json_rate = data.get('rate', 0)
    json_volume = data.get('volume', 0)
    json_pitch = data.get('pitch', 0)
    
    # Override with query parameters if provided
    final_voice = voice if voice is not None else json_voice
    final_rate = rate if rate is not None else json_rate
    final_volume = volume if volume is not None else json_volume
    final_pitch = pitch if pitch is not None else json_pitch
    
    # Validate parameters
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text field is required and cannot be empty")
    
    if final_rate < -50 or final_rate > 50:
        raise HTTPException(status_code=400, detail="Rate must be between -50 and 50")
    
    if final_volume < -50 or final_volume > 50:
        raise HTTPException(status_code=400, detail="Volume must be between -50 and 50")
    
    if final_pitch < -20 or final_pitch > 20:
        raise HTTPException(status_code=400, detail="Pitch must be between -20 and 20")
    
    # Verify voice exists
    voices = await edge_tts.list_voices()
    voice_exists = any(v['ShortName'] == final_voice for v in voices)
    if not voice_exists:
        raise HTTPException(status_code=400, detail=f"Voice '{final_voice}' not found. Use /voices endpoint to see available voices.")
    
    # Convert to speech
    rate_str = f"{final_rate:+d}%"
    volume_str = f"{final_volume:+d}%"
    pitch_str = f"{final_pitch:+d}Hz"
    
    communicate = edge_tts.Communicate(text, final_voice, rate=rate_str, volume=volume_str, pitch=pitch_str)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    
    # Return the audio file
    return FileResponse(
        tmp_path,
        media_type="audio/mpeg",
        filename="output.mp3",
        background=lambda: os.unlink(tmp_path)  # Delete file after sending
    )

@app.post("/tts/text")
async def text_to_speech_direct(
    text: str = Query(..., description="Text to convert to speech"),
    voice: str = Query("en-US-AriaNeural", description="Voice short name"),
    rate: int = Query(0, ge=-50, le=50, description="Speech rate adjustment %"),
    volume: int = Query(0, ge=-50, le=50, description="Volume adjustment %"),
    pitch: int = Query(0, ge=-20, le=20, description="Pitch adjustment Hz")
):
    """
    Convert text to speech using query parameters (alternative to JSON upload).
    """
    # Validate text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Verify voice exists
    voices = await edge_tts.list_voices()
    voice_exists = any(v['ShortName'] == voice for v in voices)
    if not voice_exists:
        raise HTTPException(status_code=400, detail=f"Voice '{voice}' not found. Use /voices endpoint to see available voices.")
    
    # Convert to speech
    rate_str = f"{rate:+d}%"
    volume_str = f"{volume:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, volume=volume_str, pitch=pitch_str)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    
    # Return the audio file
    return FileResponse(
        tmp_path,
        media_type="audio/mpeg",
        filename="output.mp3",
        background=lambda: os.unlink(tmp_path)  # Delete file after sending
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
