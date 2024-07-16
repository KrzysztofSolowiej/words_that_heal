# Script for creating batch txt files.

import os

audio_dir = '/home/user/audio_files'

audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]

batch_size = 500

for i in range(0, len(audio_files), batch_size):
    batch_files = audio_files[i:i + batch_size]
    batch_file_path = os.path.join(audio_dir, f'batch_{i // batch_size}.txt')
    with open(batch_file_path, 'w') as f:
        for file in batch_files:
            f.write(file + '\n')