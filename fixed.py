# Import the libraries
import os
import librosa
import soundfile as sf
import sounddevice as sd
import scipy.io.wavfile as wav

# Define the folder paths
dataset_raw_path = "Celsiav2/dataset_clean"
dataset_clean_path = "Celsiav2/dataset_raw"

# Define the minimum and maximum duration of each audio slice in seconds
min_duration = 2
max_duration = 10

# Define the sound quality options
sound_quality = "medium" # Choose from "low", "medium", "uncompressed" or "sounddevice"
if sound_quality == "low":
    format = "OGG"
    subtype = "VORBIS"
elif sound_quality == "medium":
    format = "FLAC"
    subtype = None
elif sound_quality == "high":
    format = "WAV"
    subtype = None
elif sound_quality == "original":
    format = None # Use NumPy arrays and scipy to save as WAV files
    subtype = None
else:
    raise ValueError("Invalid sound quality option")

# Create the clean folder if it does not exist
if not os.path.exists(dataset_clean_path):
    os.makedirs(dataset_clean_path)

# Loop through the files in the raw folder
for file in os.listdir(dataset_raw_path):
    # Check if the file is a wav or mp3 file
    if file.endswith(".wav") or file.endswith(".mp3"):
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
                # Save the slice to the clean folder with a new name and format
                new_name = file[:-4] + "_slice_" + str(i+1)
                if format is None:
                    # Use scipy to save as WAV files with NumPy arrays
                    wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, slice)
                else:
                    # Use soundfile to save as other formats with subtypes
                    sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), slice, sr, format=format, subtype=subtype)
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
                        # Save the smaller slice to the clean folder with a new name and format
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1)
                        if format is None:
                            # Use scipy to save as WAV files with NumPy arrays
                            wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, small_slice)
                        else:
                            # Use soundfile to save as other formats with subtypes
                            sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), small_slice, sr, format=format, subtype=subtype)
                    elif small_duration > max_duration:
                        # Make a longest split that fits into the range and delete the rest of the slice
                        longest_slice = small_slice[:int(max_duration*sr)]
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1)
                        if format is None:
                            # Use scipy to save as WAV files with NumPy arrays
                            wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, longest_slice)
                        else:
                            # Use soundfile to save as other formats with subtypes
                            sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), longest_slice, sr, format=format, subtype=subtype)
                        break
