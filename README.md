# sample-audio-transcription

A Streamlit web app that transcribes audio files to text using [OpenAI Whisper](https://github.com/openai/whisper).

## Features

- Upload audio files in common formats: MP3, WAV, M4A, OGG, FLAC, AAC, WebM
- Choose Whisper model size (tiny → large) for speed/accuracy trade-off
- Auto-detect language or specify manually (e.g. `vi`, `en`)
- Transcribe or translate audio to English
- View timestamped segments
- Copy transcript to clipboard or download as `.txt`

## Requirements

- Python 3.8+
- `ffmpeg` installed on the system

## Setup

```bash
# Install system dependency
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. Select a Whisper model size from the sidebar (default: `base`)
2. Optionally set the language code (leave blank for auto-detect)
3. Choose task: **transcribe** (keep original language) or **translate** (to English)
4. Upload an audio file
5. Click **Transcribe** and wait for the result
6. Copy or download the transcript

## Model sizes

| Model  | Parameters | Speed  | Accuracy |
|--------|-----------|--------|----------|
| tiny   | 39M       | Fastest | Lowest  |
| base   | 74M       | Fast    | Low     |
| small  | 244M      | Medium  | Medium  |
| medium | 769M      | Slow    | High    |
| large  | 1550M     | Slowest | Highest |

Models are downloaded automatically on first use.
