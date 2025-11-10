---
title: Edge TTS WebUI - Terms and conditions
emoji: 🏃
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: 5.21.0
app_file: app.py
pinned: false
license: mit
---

# Edge TTS API - Terms and Conditions Voice Generator 🎙️

> "Because reading terms and conditions is lekker boring, but listening to them? That's a whole different story, boet!"

## What's This Then, Aweh? 🤙

Ja nee, so basically this is a proper FastAPI application that converts your text into speech using Microsoft Edge TTS. Perfect for when you need to make those mind-numbing terms and conditions sound more human - like when your oom explains rugby rules after a few Castle Lagers.

We've built this specifically for South African companies who need to make their T&Cs sound less like a lawyer wrote them after too much Klippies and Coke, and more like a friendly conversation over a braai.

## Features (The Good Stuff) 🔥

- **300+ Voices**: More voices than Load Shedding schedules (and they actually work!)
- **40+ Languages**: From English to Afrikaans, and everything in between
- **Full Control**: Adjust rate, volume, and pitch like you're tuning your bakkie's radio
- **RESTful API**: Clean endpoints that won't make you want to emigrate
- **FastAPI Documentation**: Interactive docs that are easier to understand than SARS tax returns

## Quick Start (Faster than a taxi in Cape Town) 🚕

### Installation

```bash
# Clone this repo
git clone https://github.com/shawn-wandelbots/Edge-TTS-WebUI---Terms-and-conditions.git
cd Edge-TTS-WebUI---Terms-and-conditions

# Set up your venv (like setting up a new braai stand)
python3 -m venv venv
source venv/bin/activate

# Install the goods
pip install -r requirements.txt
pip install requests  # Because pip dependencies are like load shedding - unexpected
```

### Running the API

```bash
# Activate your venv if you haven't already
source venv/bin/activate

# Start the server (it'll run on port 8080)
python fastapi_app.py
```

**Boom!** Your API is now live at `http://localhost:8080` 🎉

Visit `http://localhost:8080/docs` for the interactive Swagger docs - it's like Google Maps but for APIs.

## API Endpoints (The Menu) 📋

### 1. List All Voices

```bash
GET /voices
```

Get all available voices. More options than a Steers menu!

### 2. Get Specific Voice Info

```bash
GET /voices/{voice_short_name}
```

Example: `/voices/en-US-AriaNeural`

### 3. Convert Text to Speech (JSON Upload)

```bash
POST /tts
```

Upload a JSON file and get back an MP3. Easy as pie (or should we say, easy as a koeksister?).

**Example JSON:**

```json
{
  "text": "Please listen carefully to your Vodacom contract terms...",
  "voice": "en-US-AriaNeural",
  "rate": 0,
  "volume": 0,
  "pitch": 0
}
```

**Try it:**

```bash
curl -X POST http://localhost:8080/tts \
  -F "file=@example_input.json" \
  --output terms_and_conditions.mp3
```

### 4. Convert Text to Speech (Direct)

```bash
POST /tts/text
```

No JSON file needed - just send parameters directly!

```bash
curl -X POST "http://localhost:8080/tts/text?text=Howzit%20my%20china&voice=en-US-AriaNeural" \
  --output greeting.mp3
```

## Parameters Explained (For the Okes Who Like Details) 🎛️

- **voice**: Voice short name (e.g., `en-US-AriaNeural`)
  - Tip: Use `/voices` to see all options
- **rate**: Speech speed (-50 to 50)
  - `-50` = Talking like you've had too much brandy
  - `0` = Normal speed (like a news anchor)
  - `+50` = Faster than a Pretoria commuter in traffic
- **volume**: Volume adjustment (-50 to 50)
  - `-50` = Whispering like you're hiding from your boss
  - `0` = Normal volume
  - `+50` = Loud like a vuvuzela at Soccer City
- **pitch**: Pitch adjustment (-20 to 20)
  - `-20` = Deep like Barry White
  - `0` = Normal
  - `+20` = High like you just saw a spider

## Popular Voices (The Squad) 🎤

- `en-US-AriaNeural` - Female, American English (sounds smart, hey?)
- `en-US-GuyNeural` - Male, American English (proper formal, bru)
- `en-GB-SoniaNeural` - Female, British English (sounds posh)
- `en-ZA-LeahNeural` - Female, South African English (finally, someone who gets us!)
- `af-ZA-AdriNeural` - Female, Afrikaans (lekker!)
- `af-ZA-WillemNeural` - Male, Afrikaans (sounds like your oom at a braai)

## Use Cases (When to Use This) 💡

1. **Terms & Conditions**: Make legal jargon sound less scary
2. **Customer Service**: Pre-recorded messages that don't sound like robots
3. **E-Learning**: Create voiceovers for training materials
4. **Accessibility**: Help visually impaired users
5. **Call Centers**: Automated messages that actually sound human
6. **Audiobooks**: Convert text to speech for storytelling

## Project Structure (What's in the Lunchbox) 📦

```
Edge-TTS-WebUI/
├── fastapi_app.py          # Main FastAPI application (the braai master)
├── app.py                  # Original Gradio UI (still works, nogal)
├── example_input.json      # Sample Vodacom T&Cs (ja nee)
├── requirements.txt        # Dependencies (the spice mix)
├── API_README.md          # Detailed API docs (for the keen beans)
├── README.md              # You are here! (X marks the spot)
└── venv/                  # Virtual environment (don't commit this, china)
```

## Contributing (Join the Team) 🤝

Found a bug? Want to add features? Contributions are welcome like a cold beer on a hot day!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/lekker-feature`)
3. Commit your changes (`git commit -m 'Add some lekker feature'`)
4. Push to the branch (`git push origin feature/lekker-feature`)
5. Open a Pull Request

## Troubleshooting (When Things Go Pear-Shaped) 🔧

**Problem**: `ModuleNotFoundError: No module named 'requests'`
**Solution**: `pip install requests` (Some dependencies are as reliable as Eskom)

**Problem**: Port 8080 already in use
**Solution**: Edit `fastapi_app.py` and change the port number. Easy peasy lemon squeezy!

**Problem**: API is slow
**Solution**: Check your internet connection. Edge TTS needs to connect to Microsoft's servers (they're probably overseas, so it might take longer than a Telkom installation)

## License 📄

MIT License - Free as a sunset over Table Mountain!

## Credits 🙏

- Built with [FastAPI](https://fastapi.tiangolo.com/) - The web framework that doesn't make you want to rage quit
- Powered by [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - Because even Microsoft does some things right
- Inspired by every South African who's ever had to read T&Cs out loud and thought "there must be a better way"

## Support 💬

Having trouble? Open an issue on GitHub. We'll help you out faster than you can say "Eish!"

---

**Made with ❤️ in South Africa** (During load shedding, obviously)

_Remember: Life is too short to read boring terms and conditions. Let the robots do it!_ 🤖
