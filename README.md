# SoundRight — Pronunciation correction prototype

Local prototype that compares a user's recorded pronunciation to a reference audio using MFCC features + DTW (dynamic time warping).

This is an MVP to demonstrate the idea: the server computes a similarity score between the user's audio and a selected reference (one audio file per target word/IPA) and returns feedback.

Quick start (Windows PowerShell):

1. Create and activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Add reference pronunciations (one file per target) into `references/` named like `word.wav` (16 kHz/mono recommended). You can create references using any TTS or by recording.

4. Run the backend:

```powershell
python backend/app.py
```

5. Open `frontend/index.html` in a browser (or serve it with a static server). Use the UI to record and upload audio for scoring.

Files added:

- `backend/app.py` — Flask server receiving uploads and returning score.
- `backend/score.py` — audio processing and DTW scoring helpers.
- `backend/requirements.txt` — Python dependencies.
- `frontend/index.html` — minimal UI to record audio and POST to the server.
- `tests/test_score.py` — unit test for the scoring function using generated audio.
- `references/.gitkeep` — folder for reference audio files.

Notes and next steps:

- This prototype uses a distance metric; it does not perform phoneme-level alignment to IPA yet. To support IPA-level feedback, integrate a forced-alignment tool (e.g., Montreal Forced Aligner, Gentle, or a phoneme recognizer such as Vosk with phoneme models) and provide phoneme error highlighting.
- You can generate reference audio automatically with offline TTS (e.g., `pyttsx3`) or upload curated native-speaker recordings.
