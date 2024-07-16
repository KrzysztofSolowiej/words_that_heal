# Script for converting amr, m4a and aac audio files to wav files using ffmpeg.

import os
import subprocess

def read_batch_file(batch_file):
    with open(batch_file, 'r') as file:
        files_to_convert = file.read().splitlines()
    return files_to_convert

def convert_audio_files(input_dir, output_dir, files_to_convert):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in files_to_convert:
        if filename.endswith('.amr') or filename.endswith('.m4a') or filename.endswith('.aac'):
            input_file = os.path.join(input_dir, filename)
            if os.path.isfile(input_file):
                output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.wav')
                
                command = ['ffmpeg', '-i', input_file, output_file]
                subprocess.run(command, check=True)
                print(f"Converted {input_file} to {output_file}")
            else:
                print(f"File {filename} listed in the batch file does not exist in the input directory.")

if __name__ == '__main__':
    input_directory = '/home/user/audio_files'
    output_directory = '/home/user/output_files'
    batch_file = '/home/user/audio_files/batch_0.txt'
    
    files_to_convert = read_batch_file(batch_file)
    convert_audio_files(input_directory, output_directory, files_to_convert)

