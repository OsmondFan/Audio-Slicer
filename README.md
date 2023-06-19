# Audio Slicer

This program is used to slice audio files based on the silences of each audio file inside a folder called "dataset_raw" and save all the slices of audios of each of the audio in the original folder into a new folder called "dataset_clean".

## Requirements

- Python 3.7 or higher
- pip install librosa
- pip install soundfile

## Usage

- Put your audio files in the "dataset_raw" folder. Make sure they are in wav format.
- Run the program with `python audio_slicer.py`.
- The sliced audio files will be saved in the "dataset_clean" folder with new names indicating the original file name and the slice number.
- You can change the minimum and maximum duration of each audio slice in seconds by modifying the `min_duration` and `max_duration` variables in the code.

## Example

If you have an audio file called "audio1.wav" in the "dataset_raw" folder that is 30 seconds long and has three silences, the program will split it into four slices and save them in the "dataset_clean" folder as follows:

- audio1_slice_1.wav
- audio1_slice_2.wav
- audio1_slice_3.wav
- audio1_slice_4.wav

If any of the slices is shorter than 2 seconds or longer than 10 seconds, the program will either skip it or split it further into smaller slices that fit into the range.
