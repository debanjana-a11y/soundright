import os
import numpy as np
from backend.score import score_recording
import soundfile as sf


def make_tone(path, freq=440, sr=16000, dur=1.0):
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    y = 0.3 * np.sin(2 * np.pi * freq * t)
    sf.write(path, y, sr)


def test_score_similar(tmp_path):
    ref = tmp_path / 'ref.wav'
    rec = tmp_path / 'rec.wav'
    make_tone(str(ref), freq=440)
    make_tone(str(rec), freq=440)
    score, details = score_recording(str(ref), str(rec))
    assert score > 70


def test_score_different(tmp_path):
    ref = tmp_path / 'ref.wav'
    rec = tmp_path / 'rec.wav'
    make_tone(str(ref), freq=440)
    make_tone(str(rec), freq=880)
    score, details = score_recording(str(ref), str(rec))
    assert score < 50
