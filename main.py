# Import the libraries
import os
import librosa
import soundfile as sf

# Define the folder paths
'''put this program in one drectory above the folders you store the audios will be the best for checking files'''
dataset_raw_path = ""
dataset_clean_path = ""

# Define the minimum and maximum duration of each audio slice in seconds
'''
If the audio is greater than [max_duration] seconds:
(eg: x_split.wav = 11 seconds, and max_duration=10, min_duration=5)
The program will slice that audio into 10 seconds(max), and since the other
duration is 1 second < 5 second, the second split will be deleted
'''

min_duration = 2
max_duration = 10

# Create the clean folder if it does not exist
if not os.path.exists(dataset_clean_path):
    os.makedirs(dataset_clean_path)

# Loop through the files in the raw folder
for file in os.listdir(dataset_raw_path):
    # Check if the file is a wav file
    if file.endswith(".wav"):
        # Load the audio file
        audio, sr = librosa.load(os.path.join(dataset_raw_path, file))
        # Detect the silence intervals
        intervals = librosa.effects.split(audio, top_db=30)
        # Loop through the intervals
        for i, (start, end) in enumerate(intervals):
            # Extract the slice of audio
            slice = audio[start:end]
            # Calculate the duration of the slice in seconds
            duration = (end - start) / sr
            # Check if the duration is within the range
            if min_duration <= duration <= max_duration:
                # Save the slice to the clean folder with a new name
                new_name = file[:-4] + "_slice_" + str(i+1) + ".wav"
                sf.write(os.path.join(dataset_clean_path, new_name), slice, sr)
            elif duration < min_duration:
                # Skip the slice if it is too short
                continue
            else:
                # Split the slice into smaller slices of equal length
                num_slices = int(duration / max_duration) + 1
                slice_length = int(len(slice) / num_slices)
                for j in range(num_slices):
                    # Extract the smaller slice of audio
                    small_slice = slice[j*slice_length:(j+1)*slice_length]
                    # Calculate the duration of the smaller slice in seconds
                    small_duration = len(small_slice) / sr
                    # Check if the smaller slice fits into the range
                    if min_duration <= small_duration <= max_duration:
                        # Save the smaller slice to the clean folder with a new name
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1) + ".wav"
                        sf.write(os.path.join(dataset_clean_path, new_name), small_slice, sr)
                    elif small_duration > max_duration:
                        # Make a longest split that fits into the range and delete the rest of the slice
                        longest_slice = small_slice[:int(max_duration*sr)]
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1) + ".wav"
                        sf.write(os.path.join(dataset_clean_path, new_name), longest_slice, sr)
                        break
