import numpy as np
import librosa
from scipy.spatial.distance import cdist
from scipy.signal import resample


def load_mono(path, sr=16000):
    y, _ = librosa.load(path, sr=sr, mono=True)
    return y


def mfcc(y, sr=16000, n_mfcc=13):
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)


def dtw_distance(a, b):
    # a, b: (n_features, T)
    # use cosine distance between feature vectors
    A = a.T
    B = b.T
    D = cdist(A, B, metric='cosine')
    # classic dynamic programming
    L1, L2 = D.shape
    acc = np.full((L1 + 1, L2 + 1), np.inf)
    acc[0, 0] = 0.0
    for i in range(1, L1 + 1):
        for j in range(1, L2 + 1):
            cost = D[i - 1, j - 1]
            acc[i, j] = cost + min(acc[i-1, j], acc[i, j-1], acc[i-1, j-1])
    return acc[L1, L2] / (L1 + L2)


def score_recording(reference_path, recording_path):
    # loads audio, computes MFCCs, returns a normalized similarity score (0-100)
    sr = 16000
    ref = load_mono(reference_path, sr=sr)
    rec = load_mono(recording_path, sr=sr)

    # ensure minimal length
    if len(ref) < 100 or len(rec) < 100:
        raise ValueError('audio too short')

    m_ref = mfcc(ref, sr=sr)
    m_rec = mfcc(rec, sr=sr)

    dist = dtw_distance(m_ref, m_rec)

    # convert distance to similarity: lower dist -> higher score
    # tune scaling: assume cosine dist in [0,2]; map to 0..100
    score = max(0.0, 100.0 * (1.0 - dist / 1.5))

    details = {'dtw_distance': float(dist)}
    return score, details
