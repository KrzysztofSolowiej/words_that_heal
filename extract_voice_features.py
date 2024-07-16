# Python script for extractring voice features from audio files in wav format.

import os
import parselmouth
import numpy as np
import pandas as pd

audio_dir = '/home/user/audio_files'
batch_file = '/home/user/audio_files/batch_0.txt'

with open(batch_file, 'r') as f:
    batch_filenames = f.read().splitlines()

audio_files = [f for f in os.listdir(audio_dir) if f in batch_filenames and f.endswith('.wav')]

def extract_features(audio_path):
    try:
        sound = parselmouth.Sound(audio_path)

        pitch = sound.to_pitch()
        pitch_values = pitch.selected_array['frequency']

        intensity = sound.to_intensity()
        intensity_values = intensity.values.T

        formant = sound.to_formant_burg()
        formant_values = [formant.get_value_at_time(1, t) for t in formant.ts()]

        point_process = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 500)
        jitter_local = parselmouth.praat.call(point_process, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)
        jitter_local_absolute = parselmouth.praat.call(point_process, "Get jitter (local, absolute)", 0.0, 0.0, 0.0001, 0.02, 1.3)
        jitter_RAP = parselmouth.praat.call(point_process, "Get jitter (rap)", 0.0, 0.0, 0.0001, 0.02, 1.3)
        jitter_PPQ5 = parselmouth.praat.call(point_process, "Get jitter (ppq5)", 0.0, 0.0, 0.0001, 0.02, 1.3)
        jitter_DDP = parselmouth.praat.call(point_process, "Get jitter (ddp)", 0.0, 0.0, 0.0001, 0.02, 1.3)

        shimmer_local = parselmouth.praat.call([sound, point_process], "Get shimmer (local)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
        shimmer_APQ3 = parselmouth.praat.call([sound, point_process], "Get shimmer (apq3)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
        shimmer_DDA = parselmouth.praat.call([sound, point_process], "Get shimmer (dda)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)

        hnr = sound.to_harmonicity()
        mean_HNR = parselmouth.praat.call(hnr, "Get mean", 0, 0)

        return {
            'mean_pitch': np.mean(pitch_values),
            'median_pitch': np.median(pitch_values),
            'pitch_standard_deviation': np.std(pitch_values),
            'min_pitch': np.min(pitch_values),
            'max_pitch': np.max(pitch_values),
            'intensity_mean': np.mean(intensity_values),
            'intensity_std': np.std(intensity_values),
            'formant_mean': np.mean(formant_values),
            'formant_std': np.std(formant_values),
            'jitter_local': jitter_local,
            'jitter_local_absolute_microseconds': jitter_local_absolute * 1e6,
            'jitter_RAP': jitter_RAP,
            'jitter_PPQ5': jitter_PPQ5,
            'jitter_DDP': jitter_DDP,
            'shimmer_local': shimmer_local,
            'shimmer_APQ3': shimmer_APQ3,
            'shimmer_DDA': shimmer_DDA,
            'mean_HNR_dB': mean_HNR
        }
    except parselmouth.PraatError as e:
        print(f"Error processing {audio_path}: {e}")
        return {
            'mean_pitch': None,
            'median_pitch': None,
            'pitch_standard_deviation': None,
            'min_pitch': None,
            'max_pitch': None,
            'intensity_mean': None,
            'intensity_std': None,
            'formant_mean': None,
            'formant_std': None,
            'jitter_local': None,
            'jitter_local_absolute_microseconds': None,
            'jitter_RAP': None,
            'jitter_PPQ5': None,
            'jitter_DDP': None,
            'shimmer_local': None,
            'shimmer_APQ3': None,
            'shimmer_DDA': None,
            'mean_HNR_dB': None
        }

results = []

for file in audio_files:
    file_path = os.path.join(audio_dir, file)
    features = extract_features(file_path)
    if features:
        features['filename'] = file
        results.append(features)

results_df = pd.DataFrame(results)

results_df.to_csv('/home/user/results_batch_0.csv', index=False)
